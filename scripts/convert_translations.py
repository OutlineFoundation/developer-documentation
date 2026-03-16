#!/usr/bin/env python3
"""
Convert .md.html translation files from Google's translation tool
into Markdown files suitable for Docusaurus i18n.

The .md.html files are HTML with two placeholder patterns:
- Code blocks: <devsite-code><!-- notranslate l10n-placeholder: l10n-placeholderN --></devsite-code>
  Code content is NOT in the translated file; pulled from English source.
- Links: <a l10n-placeholderN="N">translated text</a>
  Link URLs (hrefs) are NOT in the translated file; pulled from English source.

Numbering: code blocks are numbered 1-K (in order), links (K+1)-(K+M) (in order).
"""

import os
import posixpath
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# --- Configuration ---

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONSOLIDATED_DIR = PROJECT_ROOT / "old-site" / "i18n" / "consolidated"
ENGLISH_DOCS_DIR = PROJECT_ROOT / "docs"
OUTPUT_BASE = PROJECT_ROOT / "i18n"

LOCALES = [
    "ar", "de", "es", "es-419", "fa", "fr", "it", "ja", "ko",
    "nl", "pl", "pt-BR", "ru", "th", "tr", "zh-CN", "zh-TW",
]

# Mapping from old translation paths to new Docusaurus doc paths.
FILE_MAPPING = {
    "concepts": "concepts",
    "why-outline": "why-outline",
    "download-links": "download-links",
    "guides/service-providers/server-setup-manager": "vpn/getting-started/server-setup-manager",
    "guides/service-providers/server-setup-advanced": "vpn/getting-started/server-setup-advanced",
    "guides/service-providers/share-access": "vpn/getting-started/share-access",
    "guides/service-providers/share-management-access": "vpn/management/share-management-access",
    "guides/service-providers/dynamic-access-keys": "vpn/management/dynamic-access-keys",
    "guides/service-providers/config": "vpn/management/config",
    "guides/service-providers/metrics": "vpn/management/metrics",
    "guides/service-providers/caddy": "vpn/advanced/caddy",
    "guides/service-providers/floating-ips": "vpn/advanced/floating-ips",
    "guides/service-providers/prefixing": "vpn/advanced/prefixing",
    "guides/service-providers/websockets": "vpn/advanced/websockets",
    "reference/config": "vpn/reference/access-key-config",
    "guides/sdk/what-is-the-sdk": "sdk/what-is-the-sdk",
    "guides/sdk/concepts": "sdk/concepts",
    "guides/sdk/mobile-app-integration": "sdk/mobile-app-integration",
    "guides/sdk/use-sdk-in-go": "sdk/use-sdk-in-go",
    "reference/smart-dialer-config": "sdk/reference/smart-dialer-config",
}

# Reverse mapping: new doc path -> old source path
ENGLISH_SOURCE_MAPPING = {v: k for k, v in FILE_MAPPING.items()}


# --- English source extraction ---

def extract_code_blocks(md_text: str) -> list[str]:
    """Extract all fenced code blocks from markdown, handling indentation.

    Parses line-by-line to handle code blocks at any indentation level,
    including inside list items.
    """
    blocks = []
    lines = md_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        # Check for fenced code block opening
        fence_match = re.match(r'^(`{3,})(\w*)', stripped)
        if fence_match:
            fence = fence_match.group(1)
            lang = fence_match.group(2)
            # Find the indentation level of the fence
            indent = len(line) - len(stripped)
            # Collect code lines until closing fence
            code_lines = []
            i += 1
            while i < len(lines):
                close_stripped = lines[i].lstrip()
                # Closing fence must start with same or fewer backticks
                if close_stripped.startswith(fence) and close_stripped.strip() == fence:
                    break
                # Remove the indentation prefix if present
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
    """Remove all fenced code blocks from markdown, leaving a placeholder marker."""
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
    """Get (h2_heading_text, code_placeholder_count) per section from HTML."""
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
    """Get (h2_heading_text, code_block_count) per section from MD."""
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
    """Normalize heading text for comparison."""
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return ' '.join(text.lower().split())


def build_code_block_list(english_md: str, english_html_path: Path) -> list[str]:
    """Build code block list aligned with HTML placeholder numbering.

    When the MD has more code blocks than the HTML has placeholders (due to
    content added to MD after translation export), uses h2-heading-based
    section matching to identify which blocks to keep.
    """
    all_blocks = extract_code_blocks(english_md)

    if not english_html_path.exists():
        return all_blocks

    html_text = english_html_path.read_text(encoding='utf-8')
    html_count = len(re.findall(r'<devsite-code>', html_text))

    if len(all_blocks) == html_count:
        return all_blocks

    if len(all_blocks) < html_count:
        return all_blocks

    # MD has more blocks than HTML. Match by h2 sections.
    html_h2 = _get_h2_code_counts_html(html_text)
    md_h2 = _get_h2_code_counts_md(english_md)

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

    # Fallback: take first N blocks
    return all_blocks[:html_count]


def extract_link_urls(md_text: str) -> list[str]:
    """Extract all link URLs from markdown in document order.

    Works on full text (not line-by-line) after stripping code blocks,
    to handle multi-line links. Handles escaped brackets in link text.
    """
    text = strip_code_blocks(md_text)

    all_matches = []

    # Standard links [text](url) not preceded by !
    # Text can span lines and contain escaped brackets (\[ \])
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
            # Footnote definition at line start → backref link
            all_matches.append((m.start(), 'footnote-backref'))
        else:
            # Footnote reference
            all_matches.append((m.start(), f'#fn{m.group(1)}'))

    all_matches.sort(key=lambda x: x[0])
    return [url for _, url in all_matches]


# Manual overrides for links that don't match any FILE_MAPPING entry
# (e.g. broken links in the original source that were fixed manually)
LINK_OVERRIDES = {
    "guides/service-providers/advanced-config": "vpn/management/config",
}


def remap_internal_links(link_urls: list[str], old_path: str, new_path: str) -> list[str]:
    """Remap internal doc links from old to new path structure.

    Links extracted from the old English MD use old directory paths.
    This remaps them to the new Docusaurus directory structure.
    """
    old_dir = posixpath.dirname(old_path)
    new_dir = posixpath.dirname(new_path)
    return [_remap_link(url, old_dir, new_dir) for url in link_urls]


def _remap_link(url: str, old_dir: str, new_dir: str) -> str:
    """Remap a single internal link from old to new path."""
    # Skip external, anchor-only, and special links
    if (url.startswith(('http://', 'https://', 'mailto:', '#')) or
            url in ('footnote-backref',) or url.startswith('#fn')):
        return url

    # Split anchor
    anchor = ''
    url_path = url
    if '#' in url:
        url_path, anchor_text = url.split('#', 1)
        anchor = '#' + anchor_text

    # Strip .md extension for matching
    has_md = url_path.endswith('.md')
    clean_path = url_path[:-3] if has_md else url_path

    # Resolve to absolute path relative to docs root
    if old_dir:
        resolved = posixpath.normpath(posixpath.join(old_dir, clean_path))
    else:
        resolved = posixpath.normpath(clean_path)

    # Look up in FILE_MAPPING, then LINK_OVERRIDES
    new_target = FILE_MAPPING.get(resolved) or LINK_OVERRIDES.get(resolved)
    if new_target:
        if new_dir:
            relative = posixpath.relpath(new_target, new_dir)
        else:
            relative = new_target
        return relative + anchor

    return url


def get_frontmatter(doc_path: str) -> str:
    """Read the frontmatter from the English Docusaurus doc."""
    english_doc = ENGLISH_DOCS_DIR / f"{doc_path}.md"
    if not english_doc.exists():
        print(f"  WARNING: English doc not found: {english_doc}")
        return ""
    content = english_doc.read_text(encoding="utf-8")
    fm_match = re.match(r'^---\n(.*?\n)---\n', content, re.DOTALL)
    if fm_match:
        return f"---\n{fm_match.group(1)}---\n"
    return ""


def get_english_source(old_path: str) -> str:
    """Read the original English markdown source file."""
    source_file = PROJECT_ROOT / "old-site" / "docs" / f"{old_path}.md"
    if not source_file.exists():
        print(f"  WARNING: English source not found: {source_file}")
        return ""
    return source_file.read_text(encoding="utf-8")


def count_html_placeholders(html_file: Path) -> tuple[int, int]:
    """Count code and link placeholders in an HTML file."""
    if not html_file.exists():
        return 0, 0
    html = html_file.read_text(encoding="utf-8")
    code_count = len(re.findall(r'notranslate l10n-placeholder:\s*l10n-placeholder\d+', html))
    link_count = len(re.findall(r'l10n-placeholder\d+="(\d+)"', html))
    return code_count, link_count


# --- HTML to Markdown converter ---

class HTMLToMarkdownConverter(HTMLParser):
    """Convert devsite HTML to Markdown, resolving placeholders."""

    def __init__(self, code_blocks: list[str], link_urls: list[str], num_code_blocks: int):
        super().__init__()
        self.code_blocks = code_blocks
        self.link_urls = link_urls
        self.num_code_blocks = num_code_blocks
        self.output = []
        self.list_stack = []
        self.in_link = False
        self.link_placeholder_num = None
        self.link_text_parts = []
        self.in_code = False
        self.code_text_parts = []
        self.in_aside = False
        self.aside_class = ""
        self.aside_parts = []
        self.in_footnotes = False
        self.in_footnote_li = False
        self.footnote_id = None
        self.footnote_parts = []
        self.skip_content = False
        self.in_var = False
        self.li_just_started = False
        self.heading_id = None

    def _emit(self, text: str):
        if self.skip_content:
            return
        if self.in_footnotes and self.in_footnote_li:
            self.footnote_parts.append(text)
        elif self.in_aside:
            self.aside_parts.append(text)
        elif self.in_link:
            self.link_text_parts.append(text)
        elif self.in_code:
            self.code_text_parts.append(text)
        else:
            self.output.append(text)

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        tag_lower = tag.lower()

        if tag_lower in ('html', 'head', 'meta'):
            self.skip_content = True
            return
        if tag_lower == 'body':
            self.skip_content = False
            return
        if tag_lower == 'devsite-code':
            self.skip_content = True
            return

        if tag_lower == 'div' and attrs_dict.get('class') == 'footnotes':
            self.in_footnotes = True
            return
        if tag_lower == 'div':
            return

        if tag_lower == 'li' and self.in_footnotes:
            fn_id = attrs_dict.get('id', '')
            if fn_id.startswith('fn'):
                self.in_footnote_li = True
                self.footnote_id = fn_id.replace('fn', '')
                self.footnote_parts = []
            return

        if tag_lower == 'aside':
            self.in_aside = True
            self.aside_class = attrs_dict.get('class', 'note')
            self.aside_parts = []
            return

        if tag_lower == 'sup':
            return

        if tag_lower in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag_lower[1])
            self._emit(f"\n\n{'#' * level} ")
            self.heading_id = attrs_dict.get('id')
            return

        if tag_lower == 'p':
            if self.li_just_started:
                self.li_just_started = False
            else:
                self._emit("\n\n")
            return

        if tag_lower == 'ul':
            self.list_stack.append(('ul', 0))
            return
        if tag_lower == 'ol':
            self.list_stack.append(('ol', 0))
            return
        if tag_lower == 'li' and not self.in_footnotes:
            if self.list_stack:
                list_type, count = self.list_stack[-1]
                indent = "    " * (len(self.list_stack) - 1)
                if list_type == 'ul':
                    self._emit(f"\n{indent}- ")
                else:
                    count += 1
                    self.list_stack[-1] = (list_type, count)
                    self._emit(f"\n{indent}{count}. ")
            self.li_just_started = True
            return

        if tag_lower in ('strong', 'b'):
            self._emit("**")
            return
        if tag_lower in ('em', 'i'):
            self._emit("*")
            return

        if tag_lower == 'code':
            self.in_code = True
            self.code_text_parts = []
            return
        if tag_lower == 'var':
            self.in_var = True
            self.in_code = True
            self.code_text_parts = []
            return

        if tag_lower == 'img':
            alt = attrs_dict.get('alt', '')
            src = attrs_dict.get('src', '')
            # Fix image paths
            if '/static/outline/images/' in src:
                src = src.replace('/static/outline/images/', '/images/')
            elif src.startswith('../../../images/'):
                src = src.replace('../../../images/', '/images/')
            self._emit(f"\n\n![{alt}]({src})\n")
            return

        if tag_lower == 'a':
            placeholder_num = None
            for key, val in attrs:
                if key.startswith('l10n-placeholder'):
                    try:
                        placeholder_num = int(val)
                    except ValueError:
                        pass
            if attrs_dict.get('rev') == 'footnote':
                return
            if attrs_dict.get('rel') == 'footnote':
                return

            self.in_link = True
            self.link_placeholder_num = placeholder_num
            self.link_text_parts = []
            return

        if tag_lower == 'br':
            self._emit("\\\n")
            return
        if tag_lower == 'hr':
            return
        if tag_lower == 'span':
            return

    def handle_endtag(self, tag):
        tag_lower = tag.lower()

        if tag_lower == 'head':
            self.skip_content = False
            return
        if tag_lower in ('html', 'body', 'meta'):
            return
        if tag_lower == 'devsite-code':
            self.skip_content = False
            return

        if tag_lower == 'div':
            if self.in_footnotes:
                self.in_footnotes = False
            return

        if tag_lower == 'aside':
            aside_text = ''.join(self.aside_parts).strip()
            aside_type = "tip" if self.aside_class == "special" else "note"
            # Remove leading label since admonition title handles it
            aside_text = re.sub(
                r'^\*\*(?:Important|Importante|Note|Nota|Hinweis|Wichtig|'
                r'Remarque|Importante|Ważne|Uwaga|Примечание|Важно|'
                r'注意|注|重要|중요|참고|ملاحظة|مهم|หมายเหตุ|สำคัญ|'
                r'Önemli|Not|Belangrijk|Opmerking)[:\uff1a]?\*\*\s*',
                '', aside_text
            )
            if aside_type == "tip":
                self._emit(f"\n\n:::warning\n{aside_text}\n:::\n")
            else:
                self._emit(f"\n\n:::note\n{aside_text}\n:::\n")
            self.in_aside = False
            return

        if tag_lower == 'li' and self.in_footnotes and self.in_footnote_li:
            fn_text = ''.join(self.footnote_parts).strip()
            fn_text = fn_text.rstrip(' ↩')
            self._emit(f"\n\n[^{self.footnote_id}]: {fn_text}")
            self.in_footnote_li = False
            return

        if tag_lower == 'sup':
            return

        if tag_lower in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            if self.heading_id:
                self._emit(f" {{#{self.heading_id}}}")
                self.heading_id = None
            self._emit("\n")
            return

        if tag_lower in ('ul', 'ol'):
            if self.list_stack:
                self.list_stack.pop()
            if not self.list_stack:
                self._emit("\n")
            return

        if tag_lower in ('strong', 'b'):
            self._emit("**")
            return
        if tag_lower in ('em', 'i'):
            self._emit("*")
            return

        if tag_lower == 'code' and not self.in_var:
            code_text = ''.join(self.code_text_parts)
            self.in_code = False
            self._emit(f"`{code_text}`")
            return
        if tag_lower == 'var' or (tag_lower == 'code' and self.in_var):
            code_text = ''.join(self.code_text_parts)
            self.in_code = False
            self.in_var = False
            self._emit(f"`{code_text}`")
            return

        if tag_lower == 'a':
            if not self.in_link:
                return
            link_text = ''.join(self.link_text_parts).strip()
            url = ""
            if self.link_placeholder_num is not None:
                link_idx = self.link_placeholder_num - self.num_code_blocks - 1
                if 0 <= link_idx < len(self.link_urls):
                    url = self.link_urls[link_idx]
                else:
                    # Fallback: use the link text if it looks like a URL
                    if link_text.startswith('http') or link_text.startswith('#'):
                        url = link_text
                    else:
                        url = "#"

            # Reset link state BEFORE emitting so output goes to main buffer
            self.in_link = False
            self.link_placeholder_num = None

            # Footnote reference links (just a number)
            if link_text and re.match(r'^\d+$', link_text) and url.startswith('#fn'):
                self._emit(f"[^{link_text}]")
            elif url == "footnote-backref":
                pass  # Skip back-references
            elif link_text == url or link_text == url.rstrip('/'):
                self._emit(f"<{url}>")
            else:
                self._emit(f"[{link_text}]({url})")
            return

        if tag_lower in ('p', 'li', 'span', 'hr', 'ol'):
            return

    def handle_data(self, data):
        if self.skip_content:
            return
        if self.in_code:
            self.code_text_parts.append(data)
            return
        self._emit(data)

    def handle_comment(self, data):
        data = data.strip()
        match = re.match(r'notranslate l10n-placeholder:\s*l10n-placeholder(\d+)', data)
        if match:
            placeholder_num = int(match.group(1))
            code_idx = placeholder_num - 1
            # Write directly to output (not _emit) since this comment is inside
            # <devsite-code> which sets skip_content=True
            if 0 <= code_idx < len(self.code_blocks):
                self.output.append(f"\n\n{self.code_blocks[code_idx]}\n")
            else:
                self.output.append(f"\n\n```\n[Code block {placeholder_num} not found]\n```\n")

    def handle_entityref(self, name):
        entities = {
            'amp': '&', 'lt': '<', 'gt': '>', 'quot': '"',
            'apos': "'", 'nbsp': ' ',
        }
        self._emit(entities.get(name, f'&{name};'))

    def handle_charref(self, name):
        try:
            if name.startswith('x'):
                char = chr(int(name[1:], 16))
            else:
                char = chr(int(name))
            self._emit(char)
        except (ValueError, OverflowError):
            self._emit(f'&#{name};')

    def get_markdown(self) -> str:
        text = ''.join(self.output)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()
        return text


def convert_html_to_markdown(html_content: str, code_blocks: list[str],
                              link_urls: list[str], num_code_blocks: int) -> str:
    converter = HTMLToMarkdownConverter(code_blocks, link_urls, num_code_blocks)
    converter.feed(html_content)
    return converter.get_markdown()


# --- Main conversion logic ---

def process_file(locale: str, old_path: str, new_path: str, verbose: bool = False) -> bool:
    """Process a single translation file. Returns True on success."""
    html_file = CONSOLIDATED_DIR / locale / "docs" / f"{old_path}.md.html"
    if not html_file.exists():
        if verbose:
            print(f"    SKIP: {html_file.name} not found")
        return False

    html_content = html_file.read_text(encoding="utf-8")

    # Get the original English markdown
    english_old_path = ENGLISH_SOURCE_MAPPING.get(new_path)
    if not english_old_path:
        print(f"    ERROR: No English source mapping for {new_path}")
        return False

    english_md = get_english_source(english_old_path)
    if not english_md:
        return False

    en_html_file = CONSOLIDATED_DIR / "en" / "docs" / f"{old_path}.md.html"
    code_blocks = build_code_block_list(english_md, en_html_file)
    link_urls = extract_link_urls(english_md)
    link_urls = remap_internal_links(link_urls, old_path, new_path)

    # Cross-check against HTML placeholder counts
    html_code_count, html_link_count = count_html_placeholders(en_html_file)

    if len(code_blocks) != html_code_count and verbose:
        print(f"    WARN [{old_path}]: code blocks={len(code_blocks)} vs HTML={html_code_count}")
    if len(link_urls) != html_link_count and verbose:
        print(f"    WARN [{old_path}]: links={len(link_urls)} vs HTML={html_link_count}")

    # Convert HTML to Markdown
    markdown = convert_html_to_markdown(
        html_content, code_blocks, link_urls, len(code_blocks)
    )

    # Get frontmatter
    frontmatter = get_frontmatter(new_path)

    full_content = f"{frontmatter}\n{markdown}\n"

    # Write output
    output_file = (OUTPUT_BASE / locale / "docusaurus-plugin-content-docs"
                   / "current" / f"{new_path}.md")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(full_content, encoding="utf-8")
    return True


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print(f"Converting translations from: {CONSOLIDATED_DIR}")
    print(f"English docs at: {ENGLISH_DOCS_DIR}")
    print(f"Output to: {OUTPUT_BASE}")
    print()

    total_success = 0
    total_skip = 0

    for locale in LOCALES:
        print(f"Processing locale: {locale}")
        locale_success = 0

        for old_path, new_path in FILE_MAPPING.items():
            result = process_file(locale, old_path, new_path, verbose)
            if result:
                locale_success += 1
                total_success += 1
            else:
                total_skip += 1

        print(f"  Converted {locale_success}/{len(FILE_MAPPING)} files")

    print(f"\nDone! Converted {total_success} files, skipped {total_skip}")
    print(f"Output directory: {OUTPUT_BASE}")


if __name__ == "__main__":
    main()
