#!/usr/bin/env python3
"""
Debug: Compare markdown extraction vs HTML placeholder counts.
Tests extraction that handles multi-line links, escaped brackets,
code block stripping, and h2-section-based code block alignment.
"""

import re
from html.parser import HTMLParser
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ENGLISH_HTML_DIR = PROJECT_ROOT / "old-site" / "i18n" / "consolidated" / "en" / "docs"
ENGLISH_MD_DIR = PROJECT_ROOT / "old-site" / "docs"


class PlaceholderExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.code_placeholders = []
        self.link_placeholders = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for key, val in attrs:
                if key.startswith('l10n-placeholder'):
                    try:
                        self.link_placeholders.append(int(val))
                    except ValueError:
                        pass

    def handle_comment(self, data):
        match = re.match(r'\s*notranslate l10n-placeholder:\s*l10n-placeholder(\d+)', data)
        if match:
            self.code_placeholders.append(int(match.group(1)))


def extract_code_blocks_from_md(md_text: str) -> list[str]:
    """Extract fenced code blocks, handling indentation."""
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
                if indent > 0 and len(lines[i]) > indent and lines[i][:indent].strip() == '':
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
            result.append('[CODE_BLOCK]')
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


def _get_h2_code_counts_html(html_text: str) -> list[tuple[str, int]]:
    result = []
    current = ("", 0)
    for m in re.finditer(r'<h2[^>]*>(.*?)</h2>|<devsite-code>', html_text, re.DOTALL):
        if m.group(0).startswith('<h2'):
            result.append(current)
            heading = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            current = (heading, 0)
        else:
            current = (current[0], current[1] + 1)
    result.append(current)
    return result


def _get_h2_code_counts_md(md_text: str) -> list[tuple[str, int]]:
    result = []
    current = ("", 0)
    in_code = False
    fence = None
    for line in md_text.split('\n'):
        stripped = line.lstrip()
        fence_match = re.match(r'^(`{3,})', stripped)
        if fence_match:
            if not in_code:
                in_code = True
                fence = fence_match.group(1)
                current = (current[0], current[1] + 1)
            elif stripped.startswith(fence) and stripped.strip() == fence:
                in_code = False
                fence = None
            continue
        if in_code:
            continue
        h2_match = re.match(r'^##\s+(.+)$', line)
        if h2_match:
            result.append(current)
            current = (h2_match.group(1).strip(), 0)
    result.append(current)
    return result


def _normalize_heading(text: str) -> str:
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return ' '.join(text.lower().split())


def build_code_block_list(md_text: str, html_path: Path) -> list[str]:
    """Build code block list aligned with HTML placeholder numbering."""
    all_blocks = extract_code_blocks_from_md(md_text)

    if not html_path.exists():
        return all_blocks

    html_text = html_path.read_text(encoding='utf-8')
    html_count = len(re.findall(r'<devsite-code>', html_text))

    if len(all_blocks) == html_count:
        return all_blocks

    if len(all_blocks) < html_count:
        return all_blocks

    html_h2 = _get_h2_code_counts_html(html_text)
    md_h2 = _get_h2_code_counts_md(md_text)

    html_lookup = {}
    for heading, count in html_h2:
        key = _normalize_heading(heading)
        html_lookup[key] = count

    selected = []
    block_idx = 0
    for heading, md_count in md_h2:
        key = _normalize_heading(heading)
        html_section_count = html_lookup.get(key, 0)
        take = min(md_count, html_section_count)
        for i in range(take):
            selected.append(all_blocks[block_idx + i])
        block_idx += md_count

    if len(selected) == html_count:
        return selected
    return all_blocks[:html_count]


def extract_links_from_md(md_text: str) -> list[str]:
    """Extract all link URLs from markdown in document order.

    Works on full text after stripping code blocks.
    Handles multi-line links and escaped brackets.
    """
    text = strip_code_blocks(md_text)

    all_matches = []

    # Standard links [text](url) — handles escaped brackets in text
    for m in re.finditer(r'(?<!!)\[((?:[^\]\\]|\\.)*)\]\(([^)]+)\)', text):
        link_text = m.group(1)
        if link_text.startswith('^'):
            continue
        all_matches.append((m.start(), m.group(2)))

    # Auto-links <url>
    for m in re.finditer(r'<(https?://[^>]+)>', text):
        all_matches.append((m.start(), m.group(1)))

    # Footnote references [^N] and definitions [^N]:
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


FILES = [
    "concepts", "why-outline", "download-links",
    "guides/service-providers/server-setup-manager",
    "guides/service-providers/server-setup-advanced",
    "guides/service-providers/share-access",
    "guides/service-providers/share-management-access",
    "guides/service-providers/dynamic-access-keys",
    "guides/service-providers/config",
    "guides/service-providers/metrics",
    "guides/service-providers/caddy",
    "guides/service-providers/floating-ips",
    "guides/service-providers/prefixing",
    "guides/service-providers/websockets",
    "reference/config",
    "guides/sdk/what-is-the-sdk",
    "guides/sdk/concepts",
    "guides/sdk/mobile-app-integration",
    "guides/sdk/use-sdk-in-go",
    "reference/smart-dialer-config",
]


def analyze(name: str):
    html_file = ENGLISH_HTML_DIR / f"{name}.md.html"
    md_file = ENGLISH_MD_DIR / f"{name}.md"

    if not html_file.exists() or not md_file.exists():
        print(f"  SKIP: {name}")
        return

    parser = PlaceholderExtractor()
    parser.feed(html_file.read_text(encoding="utf-8"))

    md_text = md_file.read_text(encoding="utf-8")
    md_code = build_code_block_list(md_text, html_file)
    md_links = extract_links_from_md(md_text)

    html_code = sorted(parser.code_placeholders)
    html_links = sorted(parser.link_placeholders)

    code_ok = "OK" if len(md_code) == len(html_code) else "MISMATCH"
    link_ok = "OK" if len(md_links) == len(html_links) else "MISMATCH"

    print(f"  {name}")
    print(f"    Code: MD={len(md_code):2d}  HTML={len(html_code):2d}  {code_ok}")
    print(f"    Links: MD={len(md_links):2d}  HTML={len(html_links):2d}  {link_ok}")
    if code_ok == "MISMATCH":
        print(f"      HTML code placeholders: {html_code}")
    if link_ok == "MISMATCH":
        print(f"      HTML link placeholders: {html_links}")
        print(f"      MD links found:")
        for i, url in enumerate(md_links):
            print(f"        [{i}] {url}")


def main():
    print("Comparing MD extraction vs HTML placeholder counts:\n")
    for name in FILES:
        analyze(name)


if __name__ == "__main__":
    main()
