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
7. Admonitions (:::note, :::tip, etc.) match between English and translations.
8. Heading structure (anchor IDs) matches between English and translations.
9. Content parity: translations aren't significantly shorter than English.

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

# Docs that only exist in English. If you add new documentation that does
# not yet have translations, add the doc path here so the verifier won't
# flag it as missing.
ENGLISH_ONLY: set[str] = set()

# Known code block count differences: English MD has blocks added after
# translation export. The converter uses h2-section matching to select
# the correct subset. Format: doc_path -> (english_count, translated_count)
KNOWN_CODE_BLOCK_DIFFS = {
    # 2 Psiphon config code blocks added to MD after translation export
    "sdk/mobile-app-integration": (16, 14),
    # 1 RegisterErrorConfig example added to MD after translation export
    "sdk/reference/smart-dialer-config": (10, 9),
    # 9 code blocks added to MD after translation export (expanded reference)
    "vpn/reference/access-key-config": (17, 8),
}

# Known code block content differences: counts match but the content of
# specific blocks differs because the English example was rewritten after
# translation export. Format: doc_path -> set of block indices (0-based)
# that are allowed to differ.
KNOWN_CODE_BLOCK_CONTENT_DIFFS = {
    # English example rewritten from Shadowsocks JSON to transport YAML
    # after translation export
    "vpn/advanced/prefixing": {0},
}

# Known link count differences: English MD has links (footnotes, escaped
# brackets) that the HTML export did not preserve.
# Format: doc_path -> (english_count, translated_count)
KNOWN_LINK_COUNT_DIFFS = {
    # 2 footnote refs ([^1] in "Alternative[^1]:") not captured by HTML export
    "download-links": (14, 12),
    # 11 links added to MD after translation export (expanded reference)
    "vpn/reference/access-key-config": (39, 28),
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

# Known heading count differences: English has headings added after
# translation export. Format: doc_path -> (english_count, translated_count)
KNOWN_HEADING_COUNT_DIFFS: dict[str, tuple[int, int]] = {}

# Known heading anchors that only exist in the English version (added
# post-translation-export). Format: doc_path -> set of anchor IDs.
KNOWN_ENGLISH_ONLY_ANCHORS: dict[str, set[str]] = {}

# Known admonition count differences: English has admonitions added after
# translation export. Format: doc_path -> (english_count, translated_count)
KNOWN_ADMONITION_DIFFS: dict[str, tuple[int, int]] = {}

# Threshold for content parity warnings. If the translation's non-code
# content is less than this fraction of the English content length, flag it.
# This catches cases where entire sections or paragraphs were dropped during
# translation export, while allowing for natural language length differences.
# CJK languages (ja, ko, zh-CN, zh-TW) use fewer characters, so they use
# a lower threshold.
CONTENT_PARITY_THRESHOLD = 0.40
CONTENT_PARITY_THRESHOLD_CJK = 0.20
CJK_LOCALES = {"ja", "ko", "zh-CN", "zh-TW"}

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
    "sidebar.vpnSidebar.link.Management API",
    "sidebar.sdkSidebar.link.Go API Reference",
    # New category with no old-site equivalent; falls back to English
    "sidebar.sdkSidebar.category.Tools",
    # Internal label not shown to users
    "version.label",
}

# File extensions to scan for docs (both .md and .mdx).
DOC_EXTENSIONS = (".md", ".mdx")


def get_english_doc_paths() -> set[str]:
    """Get all doc paths relative to docs/, without extension."""
    paths = set()
    for ext in DOC_EXTENSIONS:
        for f in ENGLISH_DOCS_DIR.rglob(f"*{ext}"):
            rel = f.relative_to(ENGLISH_DOCS_DIR).with_suffix("")
            paths.add(str(rel))
    return paths


def get_translated_doc_paths(locale: str) -> set[str]:
    """Get all doc paths for a locale, without extension."""
    locale_dir = I18N_BASE / locale / "docusaurus-plugin-content-docs" / "current"
    if not locale_dir.exists():
        return set()
    paths = set()
    for ext in DOC_EXTENSIONS:
        for f in locale_dir.rglob(f"*{ext}"):
            rel = f.relative_to(locale_dir).with_suffix("")
            paths.add(str(rel))
    return paths


def find_doc_file(base_dir: Path, doc_path: str) -> Path | None:
    """Find a doc file with either .md or .mdx extension."""
    for ext in DOC_EXTENSIONS:
        candidate = base_dir / f"{doc_path}{ext}"
        if candidate.exists():
            return candidate
    return None


def read_doc(base_dir: Path, doc_path: str) -> str:
    """Read a doc file and return its contents."""
    f = find_doc_file(base_dir, doc_path)
    if f is None:
        raise FileNotFoundError(f"No .md or .mdx file found for {doc_path}")
    return f.read_text(encoding="utf-8")


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


def strip_non_content(md_text: str) -> str:
    """Strip frontmatter, code blocks, admonition markers, and imports.

    Returns only the prose content for length comparison.
    """
    # Remove frontmatter
    text = re.sub(r'^---\n.*?\n---\n', '', md_text, flags=re.DOTALL)
    # Remove code blocks
    text = strip_code_blocks(text)
    # Remove import lines (MDX)
    text = re.sub(r'^import\s+.*$', '', text, flags=re.MULTILINE)
    # Remove admonition markers (:::note, :::tip, etc.) but keep content
    text = re.sub(r'^:::\w*(?:\[.*?\])?\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^:::\s*$', '', text, flags=re.MULTILINE)
    # Remove JSX/HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove heading markers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    # Remove anchor IDs {#...}
    text = re.sub(r'\{#[^}]+\}', '', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


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


def extract_admonitions(md_text: str) -> list[str]:
    """Extract admonition types from markdown (:::note, :::tip, etc.).

    Returns a sorted list of admonition types found (e.g., ["caution", "note", "tip"]).
    """
    types = []
    for m in re.finditer(r'^:::(note|tip|caution|warning|danger|important|info)(?:\[.*?\])?\s*$',
                         md_text, re.MULTILINE):
        types.append(m.group(1))
    return types


def extract_heading_anchors(md_text: str) -> list[str]:
    """Extract heading anchor IDs from markdown.

    Looks for patterns like `## Heading {#anchor_id}` and returns the list
    of anchor IDs in document order.
    """
    anchors = []
    for m in re.finditer(r'^#{1,6}\s+.*?\{#([^}]+)\}\s*$', md_text, re.MULTILINE):
        anchors.append(m.group(1))
    return anchors


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
                missing_k = en_keys - tr_keys
                extra_k = tr_keys - en_keys
                detail = []
                if missing_k:
                    detail.append(f"missing keys: {missing_k}")
                if extra_k:
                    detail.append(f"extra keys: {extra_k}")
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
            allowed_block_diffs = KNOWN_CODE_BLOCK_CONTENT_DIFFS.get(doc_path, set())
            for idx, (en_block, tr_block) in enumerate(zip(en_blocks, tr_blocks)):
                if en_block != tr_block:
                    if idx in allowed_block_diffs:
                        continue  # Known acceptable content difference
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

        # Admonitions: check that translation has same count and types
        en_admonitions = extract_admonitions(en_text)
        tr_admonitions = extract_admonitions(tr_text)
        if len(en_admonitions) != len(tr_admonitions):
            known = KNOWN_ADMONITION_DIFFS.get(doc_path)
            if known and known == (len(en_admonitions), len(tr_admonitions)):
                pass  # Known acceptable difference
            else:
                issues.append(Issue(
                    locale, doc_path, "ADMONITIONS",
                    f"Count mismatch: English has {len(en_admonitions)} "
                    f"({', '.join(en_admonitions)}), "
                    f"translation has {len(tr_admonitions)}"
                    f" ({', '.join(tr_admonitions) if tr_admonitions else 'none'})"
                ))
        elif en_admonitions != tr_admonitions:
            issues.append(Issue(
                locale, doc_path, "ADMONITIONS",
                f"Type mismatch: English has [{', '.join(en_admonitions)}], "
                f"translation has [{', '.join(tr_admonitions)}]"
            ))

        # Heading structure: check anchor IDs match
        en_anchors = extract_heading_anchors(en_text)
        tr_anchors = extract_heading_anchors(tr_text)
        if en_anchors and tr_anchors:
            # Translated files should have the same anchor IDs
            en_anchor_set = set(en_anchors)
            tr_anchor_set = set(tr_anchors)

            # Filter out known English-only anchors
            known_en_only = KNOWN_ENGLISH_ONLY_ANCHORS.get(doc_path, set())
            en_anchor_set -= known_en_only

            missing_anchors = en_anchor_set - tr_anchor_set
            extra_anchors = tr_anchor_set - en_anchor_set

            if missing_anchors:
                issues.append(Issue(
                    locale, doc_path, "HEADINGS",
                    f"Missing heading anchors: {sorted(missing_anchors)}"
                ))
            if extra_anchors:
                issues.append(Issue(
                    locale, doc_path, "HEADINGS",
                    f"Extra heading anchors: {sorted(extra_anchors)}"
                ))

        # Content parity: warn if translation is significantly shorter
        en_content = strip_non_content(en_text)
        tr_content = strip_non_content(tr_text)

        if len(en_content) > 100:  # Skip very short docs
            threshold = (
                CONTENT_PARITY_THRESHOLD_CJK
                if locale in CJK_LOCALES
                else CONTENT_PARITY_THRESHOLD
            )
            ratio = len(tr_content) / len(en_content)
            if ratio < threshold:
                issues.append(Issue(
                    locale, doc_path, "CONTENT_PARITY",
                    f"Translation content is {ratio:.0%} of English length "
                    f"({len(tr_content)} vs {len(en_content)} chars) — "
                    f"possible missing paragraphs"
                ))

    return issues


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
