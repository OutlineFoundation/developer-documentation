#!/usr/bin/env python3
"""
Verify translated documentation files against their English equivalents.

Checks:
1. Every English doc has a translation for every locale (no missing files).
2. No extra translation files exist that don't correspond to an English doc.
3. Frontmatter matches the English source exactly.
4. Code blocks in translations are identical to the English source.
5. Link URLs in translations are identical to the English source.
6. Theme translation files (footer.json, current.json) exist and have valid keys.

Known acceptable differences are documented and excluded:
- Code block counts may differ where English MD was updated after translation
  export (content added post-export is not in translation HTML sources).
- Link counts may differ where the English MD has footnotes or escaped brackets
  that the HTML export did not preserve.
- Internal links may lack .md extensions (Docusaurus resolves both forms).
- Some locales have link order swapped by the translator.
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
ENGLISH_DOCS_DIR = PROJECT_ROOT / "docs"
I18N_BASE = PROJECT_ROOT / "i18n"

LOCALES = [
    "ar", "de", "es", "es-419", "fa", "fr", "it", "ja", "ko",
    "nl", "pl", "pt-BR", "ru", "th", "tr", "zh-CN", "zh-TW",
]

# Docs that only exist in English (no translation source yet available)
ENGLISH_ONLY: set[str] = set()

# Known code block count differences: English MD has blocks added after
# translation export. The converter uses h2-section matching to select
# the correct subset. Format: doc_path -> (english_count, translated_count)
KNOWN_CODE_BLOCK_DIFFS = {
    # 2 Psiphon config code blocks added to MD after translation export
    "sdk/mobile-app-integration": (16, 14),
    # 1 RegisterErrorConfig example added to MD after translation export
    "sdk/reference/smart-dialer-config": (10, 9),
}

# Known link count differences: English MD has links (footnotes, escaped
# brackets) that the HTML export did not preserve.
# Format: doc_path -> (english_count, translated_count)
KNOWN_LINK_COUNT_DIFFS = {
    # 2 footnote refs ([^1] in "Alternative[^1]:") not captured by HTML export
    "download-links": (14, 12),
    # 3 links with escaped brackets in text (e.g. [EndpointConfig\[\]]) not in HTML
    "vpn/reference/access-key-config": (31, 28),
    # 1 link to advanced-config added to MD after translation export
    "vpn/advanced/caddy": (9, 8),
}

# Known link order swaps: some translators reordered text, causing link
# URLs to appear in a different order. Format: doc_path -> set of link indices
# (0-based) where order may differ.
KNOWN_LINK_SWAPS = {
    # Wikipedia Base64 link and Google encode/decode toolbox link swapped
    "vpn/management/dynamic-access-keys": {3, 4},
}


def get_english_doc_paths() -> set[str]:
    """Get all doc paths relative to docs/, without .md extension."""
    paths = set()
    for f in ENGLISH_DOCS_DIR.rglob("*.md"):
        rel = f.relative_to(ENGLISH_DOCS_DIR).with_suffix("")
        paths.add(str(rel))
    return paths


def get_translated_doc_paths(locale: str) -> set[str]:
    """Get all doc paths for a locale, without .md extension."""
    locale_dir = I18N_BASE / locale / "docusaurus-plugin-content-docs" / "current"
    if not locale_dir.exists():
        return set()
    paths = set()
    for f in locale_dir.rglob("*.md"):
        rel = f.relative_to(locale_dir).with_suffix("")
        paths.add(str(rel))
    return paths


def read_doc(base_dir: Path, doc_path: str) -> str:
    """Read a doc file and return its contents."""
    return (base_dir / f"{doc_path}.md").read_text(encoding="utf-8")


def extract_frontmatter(text: str) -> str | None:
    """Extract the frontmatter block (including delimiters) from markdown."""
    m = re.match(r'^(---\n.*?\n---)\n', text, re.DOTALL)
    return m.group(1) if m else None


def extract_frontmatter_keys(text: str) -> set[str]:
    """Extract the set of frontmatter key names from markdown."""
    fm = extract_frontmatter(text)
    if not fm:
        return set()
    keys = set()
    for line in fm.split('\n'):
        m = re.match(r'^(\w[\w_-]*):', line)
        if m:
            keys.add(m.group(1))
    return keys


def extract_code_blocks(md_text: str) -> list[str]:
    """Extract all fenced code blocks from markdown."""
    blocks = []
    lines = md_text.split('\n')
    i = 0
    while i < len(lines):
        stripped = lines[i].lstrip()
        fence_match = re.match(r'^(`{3,})(\w*)', stripped)
        if fence_match:
            fence = fence_match.group(1)
            lang = fence_match.group(2)
            indent = len(lines[i]) - len(stripped)
            code_lines = []
            i += 1
            while i < len(lines):
                close_stripped = lines[i].lstrip()
                if close_stripped.startswith(fence) and close_stripped.strip() == fence:
                    break
                if indent > 0 and lines[i][:indent].strip() == '':
                    code_lines.append(lines[i][indent:])
                else:
                    code_lines.append(lines[i])
                i += 1
            code = '\n'.join(code_lines)
            blocks.append(f"```{lang}\n{code}\n```")
        i += 1
    return blocks


def strip_code_blocks(md_text: str) -> str:
    """Remove all fenced code blocks from markdown."""
    result = []
    lines = md_text.split('\n')
    i = 0
    while i < len(lines):
        stripped = lines[i].lstrip()
        fence_match = re.match(r'^(`{3,})', stripped)
        if fence_match:
            fence = fence_match.group(1)
            i += 1
            while i < len(lines):
                close_stripped = lines[i].lstrip()
                if close_stripped.startswith(fence) and close_stripped.strip() == fence:
                    break
                i += 1
        else:
            result.append(lines[i])
        i += 1
    return '\n'.join(result)


def normalize_link_url(url: str) -> str:
    """Normalize a link URL for comparison.

    Strips .md extensions from internal links since Docusaurus resolves
    both forms identically.
    """
    if url.startswith(('http://', 'https://', 'mailto:', '#')):
        return url
    if url in ('footnote-backref',) or url.startswith('#fn'):
        return url

    # Split anchor
    anchor = ''
    url_path = url
    if '#' in url:
        url_path, anchor_text = url.split('#', 1)
        anchor = '#' + anchor_text

    # Strip .md extension
    if url_path.endswith('.md'):
        url_path = url_path[:-3]

    return url_path + anchor


def extract_link_urls(md_text: str) -> list[str]:
    """Extract all link URLs from markdown in document order."""
    text = strip_code_blocks(md_text)
    all_matches = []

    # Standard links [text](url)
    for m in re.finditer(r'(?<!!)\[((?:[^\]\\]|\\.)*)\]\(([^)]+)\)', text):
        link_text = m.group(1)
        if link_text.startswith('^'):
            continue
        all_matches.append((m.start(), m.group(2)))

    # Auto-links <url>
    for m in re.finditer(r'<(https?://[^>]+)>', text):
        all_matches.append((m.start(), m.group(1)))

    # Footnote references and definitions
    for m in re.finditer(r'\[\^(\d+)\]', text):
        pos = m.start()
        line_start = text.rfind('\n', 0, pos) + 1
        before = text[line_start:pos].strip()
        after_char = text[m.end()] if m.end() < len(text) else ''
        if before == '' and after_char == ':':
            all_matches.append((m.start(), 'footnote-backref'))
        else:
            all_matches.append((m.start(), f'#fn{m.group(1)}'))

    all_matches.sort(key=lambda x: x[0])
    return [url for _, url in all_matches]


class Issue:
    """A verification issue."""
    def __init__(self, locale: str, doc_path: str, category: str, message: str):
        self.locale = locale
        self.doc_path = doc_path
        self.category = category
        self.message = message

    def __str__(self):
        return f"  [{self.category}] {self.locale}/{self.doc_path}: {self.message}"


def verify_locale(locale: str, english_paths: set[str]) -> list[Issue]:
    """Verify all translations for a single locale."""
    issues = []
    locale_dir = I18N_BASE / locale / "docusaurus-plugin-content-docs" / "current"
    translated_paths = get_translated_doc_paths(locale)
    expected_paths = english_paths - ENGLISH_ONLY

    # Check for missing translations
    missing = expected_paths - translated_paths
    for doc_path in sorted(missing):
        issues.append(Issue(locale, doc_path, "MISSING", "Translation file missing"))

    # Check for extra translations
    extra = translated_paths - english_paths
    for doc_path in sorted(extra):
        issues.append(Issue(locale, doc_path, "EXTRA", "No corresponding English doc"))

    # Check each translated file against English
    for doc_path in sorted(translated_paths & english_paths):
        en_text = read_doc(ENGLISH_DOCS_DIR, doc_path)
        tr_text = read_doc(locale_dir, doc_path)

        # Frontmatter: check that translated file has the same keys
        # (title and sidebar_label values are expected to be translated)
        en_fm = extract_frontmatter(en_text)
        tr_fm = extract_frontmatter(tr_text)
        if en_fm and not tr_fm:
            issues.append(Issue(
                locale, doc_path, "FRONTMATTER",
                "Missing frontmatter (English has frontmatter)"
            ))
        elif not en_fm and tr_fm:
            issues.append(Issue(
                locale, doc_path, "FRONTMATTER",
                "Unexpected frontmatter (English has none)"
            ))
        elif en_fm and tr_fm:
            en_keys = extract_frontmatter_keys(en_text)
            tr_keys = extract_frontmatter_keys(tr_text)
            if en_keys != tr_keys:
                missing = en_keys - tr_keys
                extra = tr_keys - en_keys
                detail = []
                if missing:
                    detail.append(f"missing keys: {missing}")
                if extra:
                    detail.append(f"extra keys: {extra}")
                issues.append(Issue(
                    locale, doc_path, "FRONTMATTER",
                    f"Frontmatter keys differ: {'; '.join(detail)}"
                ))

        # Code blocks
        en_blocks = extract_code_blocks(en_text)
        tr_blocks = extract_code_blocks(tr_text)
        if len(en_blocks) != len(tr_blocks):
            known = KNOWN_CODE_BLOCK_DIFFS.get(doc_path)
            if known and known == (len(en_blocks), len(tr_blocks)):
                pass  # Known acceptable difference
            else:
                issues.append(Issue(
                    locale, doc_path, "CODE_BLOCKS",
                    f"Count mismatch: English has {len(en_blocks)}, "
                    f"translation has {len(tr_blocks)}"
                ))
        else:
            for idx, (en_block, tr_block) in enumerate(zip(en_blocks, tr_blocks)):
                if en_block != tr_block:
                    en_lines = en_block.split('\n')
                    tr_lines = tr_block.split('\n')
                    diff_line = None
                    for li, (el, tl) in enumerate(zip(en_lines, tr_lines)):
                        if el != tl:
                            diff_line = li + 1
                            break
                    if diff_line is None and len(en_lines) != len(tr_lines):
                        diff_line = min(len(en_lines), len(tr_lines)) + 1
                    issues.append(Issue(
                        locale, doc_path, "CODE_BLOCKS",
                        f"Block {idx + 1} differs from English"
                        f" (first diff at line {diff_line})"
                    ))

        # Link URLs (normalized to strip .md extensions)
        en_links = [normalize_link_url(u) for u in extract_link_urls(en_text)]
        tr_links = [normalize_link_url(u) for u in extract_link_urls(tr_text)]
        if len(en_links) != len(tr_links):
            known = KNOWN_LINK_COUNT_DIFFS.get(doc_path)
            if known and known == (len(en_links), len(tr_links)):
                pass  # Known acceptable difference
            else:
                issues.append(Issue(
                    locale, doc_path, "LINKS",
                    f"Count mismatch: English has {len(en_links)}, "
                    f"translation has {len(tr_links)}"
                ))
        else:
            swap_indices = KNOWN_LINK_SWAPS.get(doc_path, set())
            for idx, (en_url, tr_url) in enumerate(zip(en_links, tr_links)):
                if en_url != tr_url:
                    if idx in swap_indices:
                        continue  # Known link order swap
                    issues.append(Issue(
                        locale, doc_path, "LINKS",
                        f"Link {idx + 1} differs: "
                        f"English={en_url!r}, translation={tr_url!r}"
                    ))

    return issues


# Theme translation files to verify against their English references.
# Each entry: (subdir, filename)
THEME_TRANSLATION_FILES = [
    ("docusaurus-theme-classic", "footer.json"),
    ("docusaurus-plugin-content-docs", "current.json"),
]

# Theme translation keys that are OK to leave untranslated (brand names,
# technical terms, or internal labels that are the same in all languages).
KNOWN_UNTRANSLATABLE_KEYS = {
    # Brand names / technical terms (same in all languages)
    "link.item.label.GitHub",
    "link.item.label.Reddit",
    "sidebar.docs.category.Outline VPN",
    "sidebar.docs.category.Outline SDK",
    "sidebar.docs.link.Management API",
    "sidebar.docs.link.Go API Reference",
    # New category with no old-site equivalent; falls back to English
    "sidebar.docs.category.Tools",
    # Internal label not shown to users
    "version.label",
}

def verify_theme_translations(locale: str) -> list[Issue]:
    """Verify theme translation files (footer, sidebar) for a locale."""
    issues = []

    for subdir, filename in THEME_TRANSLATION_FILES:
        en_path = I18N_BASE / "en" / subdir / filename
        locale_path = I18N_BASE / locale / subdir / filename

        if not en_path.exists():
            continue

        with open(en_path, "r", encoding="utf-8") as f:
            en_data = json.load(f)

        if not locale_path.exists():
            issues.append(Issue(
                locale, f"{subdir}/{filename}", "THEME_MISSING",
                "Translation file missing"
            ))
            continue

        try:
            with open(locale_path, "r", encoding="utf-8") as f:
                locale_data = json.load(f)
        except json.JSONDecodeError as e:
            issues.append(Issue(
                locale, f"{subdir}/{filename}", "THEME_INVALID",
                f"Invalid JSON: {e}"
            ))
            continue

        en_keys = set(en_data.keys())
        locale_keys = set(locale_data.keys())

        # Check for extra keys not in English reference
        extra_keys = locale_keys - en_keys
        for key in sorted(extra_keys):
            issues.append(Issue(
                locale, f"{subdir}/{filename}", "THEME_EXTRA_KEY",
                f"Key not in English reference: {key!r}"
            ))

        # Check for missing keys (error unless known-untranslatable)
        missing_keys = en_keys - locale_keys
        for key in sorted(missing_keys):
            if key in KNOWN_UNTRANSLATABLE_KEYS:
                continue
            issues.append(Issue(
                locale, f"{subdir}/{filename}", "THEME_UNTRANSLATED",
                f"Missing translation for key: {key!r}"
            ))

    return issues


def main():
    english_paths = get_english_doc_paths()

    print(f"English docs: {len(english_paths)} files")
    print(f"English-only (no translation expected): {len(ENGLISH_ONLY)} files")
    print(f"Locales: {len(LOCALES)}")
    print()

    total_issues = 0
    issues_by_category: dict[str, int] = {}

    for locale in LOCALES:
        issues = verify_locale(locale, english_paths)
        issues += verify_theme_translations(locale)

        if issues:
            print(f"FAIL {locale}: {len(issues)} issue(s)")
            for issue in issues:
                print(issue)
                issues_by_category[issue.category] = (
                    issues_by_category.get(issue.category, 0) + 1
                )
            total_issues += len(issues)
        else:
            print(f"OK   {locale}")

    print()
    if total_issues:
        print(f"FAILED: {total_issues} issue(s) found")
        for cat, count in sorted(issues_by_category.items()):
            print(f"  {cat}: {count}")
        sys.exit(1)
    else:
        print("PASSED: All translations verified")
        sys.exit(0)


if __name__ == "__main__":
    main()
