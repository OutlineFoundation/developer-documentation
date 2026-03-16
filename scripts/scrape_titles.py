#!/usr/bin/env python3
"""
Scrape translated page titles from the old developers.google.com/outline site
and update the frontmatter (title and sidebar_label) in the translated Docusaurus
markdown files.

Usage:
    python scripts/scrape_titles.py [--dry-run]

With --dry-run, prints what would change without modifying files.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
I18N_DIR = PROJECT_ROOT / "i18n"
ENGLISH_DOCS_DIR = PROJECT_ROOT / "docs"

LOCALES = [
    "ar", "de", "es", "es-419", "fa", "fr", "it", "ja", "ko",
    "nl", "pl", "pt-BR", "ru", "th", "tr", "zh-CN", "zh-TW",
]

# Mapping: new Docusaurus doc path -> old site URL path (relative to /outline/docs/)
# The old site URL is: https://developers.google.com/outline/docs/{old_path}?hl={locale}
DOC_TO_OLD_URL = {
    "concepts": "concepts",
    "why-outline": "why-outline",
    "download-links": "download-links",
    "vpn/getting-started/server-setup-manager": "guides/service-providers/server-setup-manager",
    "vpn/getting-started/server-setup-advanced": "guides/service-providers/server-setup-advanced",
    "vpn/getting-started/share-access": "guides/service-providers/share-access",
    "vpn/management/share-management-access": "guides/service-providers/share-management-access",
    "vpn/management/dynamic-access-keys": "guides/service-providers/dynamic-access-keys",
    "vpn/management/config": "guides/service-providers/config",
    "vpn/management/metrics": "guides/service-providers/metrics",
    "vpn/advanced/caddy": "guides/service-providers/caddy",
    "vpn/advanced/floating-ips": "guides/service-providers/floating-ips",
    "vpn/advanced/prefixing": "guides/service-providers/prefixing",
    "vpn/advanced/websockets": "guides/service-providers/websockets",
    "vpn/reference/access-key-config": "reference/config",
    "sdk/what-is-the-sdk": "guides/sdk/what-is-the-sdk",
    "sdk/concepts": "guides/sdk/concepts",
    "sdk/mobile-app-integration": "guides/sdk/mobile-app-integration",
    "sdk/use-sdk-in-go": "guides/sdk/use-sdk-in-go",
    "sdk/reference/smart-dialer-config": "reference/smart-dialer-config",
    "sdk/command-line-debugging": "guides/sdk/command-line-debugging",
}

# The English title (from frontmatter) for each doc — used to decide
# if a scraped title is actually translated or just echoed back in English.
ENGLISH_TITLES: dict[str, str] = {}


def get_english_title(doc_path: str) -> str:
    """Read the English title from the source markdown frontmatter."""
    if doc_path in ENGLISH_TITLES:
        return ENGLISH_TITLES[doc_path]
    md_file = ENGLISH_DOCS_DIR / f"{doc_path}.md"
    if not md_file.exists():
        return ""
    content = md_file.read_text(encoding="utf-8")
    m = re.search(r'^title:\s*"([^"]+)"', content, re.MULTILINE)
    if m:
        ENGLISH_TITLES[doc_path] = m.group(1)
        return m.group(1)
    m = re.search(r"^title:\s*'([^']+)'", content, re.MULTILINE)
    if m:
        ENGLISH_TITLES[doc_path] = m.group(1)
        return m.group(1)
    m = re.search(r'^title:\s*(.+)', content, re.MULTILINE)
    if m:
        ENGLISH_TITLES[doc_path] = m.group(1).strip()
        return m.group(1).strip()
    return ""


def get_english_sidebar_label(doc_path: str) -> str:
    """Read the English sidebar_label from the source markdown frontmatter."""
    md_file = ENGLISH_DOCS_DIR / f"{doc_path}.md"
    if not md_file.exists():
        return ""
    content = md_file.read_text(encoding="utf-8")
    m = re.search(r'^sidebar_label:\s*"([^"]+)"', content, re.MULTILINE)
    if m:
        return m.group(1)
    m = re.search(r"^sidebar_label:\s*'([^']+)'", content, re.MULTILINE)
    if m:
        return m.group(1)
    m = re.search(r'^sidebar_label:\s*(.+)', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ""


def fetch_title(old_url_path: str, locale: str) -> str | None:
    """Fetch the translated page title from the old site."""
    url = f"https://developers.google.com/outline/docs/{old_url_path}?hl={locale}"
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "--max-time", "15", url],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0:
            return None
        html = result.stdout
        # Extract title: "Translated Title  |  Outline  |  Google for Developers"
        m = re.search(r'<title>([^<]+)</title>', html)
        if not m:
            return None
        raw_title = m.group(1)
        # Clean up HTML entities first
        raw_title = raw_title.replace('&nbsp;', ' ').replace('&amp;', '&')
        raw_title = raw_title.replace('&lt;', '<').replace('&gt;', '>')
        raw_title = raw_title.replace('&quot;', '"')
        # The title format is: "Page Title  |  Outline  |  Google for Developers"
        # or sometimes: "Page Title  |  Google for Developers" (without Outline)
        parts = raw_title.split('|')
        if not parts:
            return None
        title = parts[0].strip()
        if not title:
            return None
        return title
    except (subprocess.TimeoutExpired, Exception) as e:
        print(f"  Error fetching {url}: {e}", file=sys.stderr)
        return None


def update_frontmatter(file_path: Path, new_title: str, new_sidebar_label: str) -> bool:
    """Update title and sidebar_label in markdown frontmatter. Returns True if changed."""
    content = file_path.read_text(encoding="utf-8")
    original = content

    # Update title
    content = re.sub(
        r'^(title:\s*)"[^"]*"',
        f'\\1"{new_title}"',
        content,
        count=1,
        flags=re.MULTILINE,
    )

    # Update sidebar_label
    content = re.sub(
        r'^(sidebar_label:\s*)"[^"]*"',
        f'\\1"{new_sidebar_label}"',
        content,
        count=1,
        flags=re.MULTILINE,
    )

    if content != original:
        file_path.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    dry_run = "--dry-run" in sys.argv

    # First, collect all English titles and sidebar labels
    for doc_path in DOC_TO_OLD_URL:
        get_english_title(doc_path)

    # Track results
    total_updated = 0
    total_skipped = 0
    total_errors = 0
    missing_translations = []

    for locale in LOCALES:
        print(f"\n{'='*60}")
        print(f"Locale: {locale}")
        print(f"{'='*60}")

        locale_updated = 0

        for doc_path, old_url_path in DOC_TO_OLD_URL.items():
            translated_file = (
                I18N_DIR / locale / "docusaurus-plugin-content-docs" / "current"
                / f"{doc_path}.md"
            )

            if not translated_file.exists():
                print(f"  SKIP {doc_path}: translated file does not exist")
                total_skipped += 1
                continue

            en_title = get_english_title(doc_path)
            en_sidebar_label = get_english_sidebar_label(doc_path)

            # Fetch translated title
            translated_title = fetch_title(old_url_path, locale)

            if translated_title is None:
                print(f"  ERROR {doc_path}: could not fetch title")
                total_errors += 1
                missing_translations.append((locale, doc_path))
                continue

            if translated_title == en_title or translated_title == en_sidebar_label:
                print(f"  SAME {doc_path}: \"{translated_title}\" (same as English)")
                total_skipped += 1
                continue

            # Determine sidebar_label: use translated title unless it's very long
            # The old site's page title maps to our title; for sidebar_label we may
            # want a shorter version. But since the old site didn't have separate
            # sidebar labels vs titles (the sidebar used the page title), we'll use
            # the scraped title for sidebar_label too.
            new_sidebar_label = translated_title
            new_title = translated_title

            if dry_run:
                print(f"  WOULD UPDATE {doc_path}:")
                print(f"    title: \"{en_title}\" -> \"{new_title}\"")
                print(f"    sidebar_label: \"{en_sidebar_label}\" -> \"{new_sidebar_label}\"")
            else:
                changed = update_frontmatter(translated_file, new_title, new_sidebar_label)
                if changed:
                    print(f"  UPDATED {doc_path}: \"{new_title}\"")
                    locale_updated += 1
                    total_updated += 1
                else:
                    print(f"  UNCHANGED {doc_path}")

        print(f"  -> {locale_updated} files updated for {locale}")

    print(f"\n{'='*60}")
    print(f"Summary")
    print(f"{'='*60}")
    print(f"Total updated: {total_updated}")
    print(f"Total skipped (same as English): {total_skipped}")
    print(f"Total errors: {total_errors}")

    if missing_translations:
        print(f"\nMissing translations:")
        for locale, doc_path in missing_translations:
            print(f"  {locale}: {doc_path}")

    if dry_run:
        print(f"\n(Dry run — no files were modified)")


if __name__ == "__main__":
    main()
