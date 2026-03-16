#!/usr/bin/env python3
"""Scrape command-line-debugging translations from the old Google Developers site.

Fetches developers.google.com/outline/docs/guides/sdk/command-line-debugging
for each locale and converts the translated HTML to Markdown, keeping code
blocks and link URLs from the English source.

Usage:
    python3 scripts/scrape_command_line_debugging.py
"""

import re
import subprocess
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENGLISH_DOCS_DIR = PROJECT_ROOT / "docs"
OUTPUT_BASE = PROJECT_ROOT / "i18n"

LOCALES = [
    "ar", "de", "es", "es-419", "fa", "fr", "it", "ja",
    "ko", "nl", "pl", "pt-BR", "ru", "th", "tr", "zh-CN", "zh-TW",
]

DOC_PATH = "sdk/command-line-debugging"
URL_TEMPLATE = (
    "https://developers.google.com/outline/docs/guides/sdk/"
    "command-line-debugging?hl={locale}"
)


def fetch_page(url: str) -> str:
    """Fetch a URL using curl."""
    result = subprocess.run(
        ["curl", "-sL", "--max-time", "30", url],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr}")
    return result.stdout


def extract_article_body(html: str) -> str | None:
    """Extract the devsite-article-body content from the full page HTML."""
    # The article body is inside <div class="devsite-article-body ...">
    m = re.search(
        r'<div[^>]*class="[^"]*devsite-article-body[^"]*"[^>]*>(.*)',
        html,
        re.DOTALL,
    )
    if not m:
        return None

    body = m.group(1)
    # Find the matching closing tag (simple depth tracking)
    depth = 1
    pos = 0
    while depth > 0 and pos < len(body):
        open_m = re.search(r'<div\b', body[pos:])
        close_m = re.search(r'</div>', body[pos:])
        if close_m is None:
            break
        if open_m and open_m.start() < close_m.start():
            depth += 1
            pos += open_m.end()
        else:
            depth -= 1
            if depth == 0:
                return body[:pos + close_m.start()]
            pos += close_m.end()

    return body


def extract_code_blocks_from_md(md_text: str) -> list[str]:
    """Extract fenced code blocks from English markdown."""
    blocks = []
    lines = md_text.split('\n')
    i = 0
    while i < len(lines):
        stripped = lines[i].lstrip()
        fence_match = re.match(r'^(`{3,})(\w*)', stripped)
        if fence_match:
            fence = fence_match.group(1)
            lang = fence_match.group(2)
            code_lines = []
            i += 1
            while i < len(lines):
                close_stripped = lines[i].lstrip()
                if close_stripped.startswith(fence) and close_stripped.strip() == fence:
                    break
                code_lines.append(lines[i])
                i += 1
            code = '\n'.join(code_lines)
            blocks.append(f"```{lang}\n{code}\n```")
        i += 1
    return blocks


def extract_link_urls_from_md(md_text: str) -> list[str]:
    """Extract link URLs from English markdown (excluding code blocks)."""
    # Strip code blocks first
    result_lines = []
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
            result_lines.append(lines[i])
        i += 1
    text = '\n'.join(result_lines)

    urls = []
    for m in re.finditer(r'(?<!!)\[(?:[^\]\\]|\\.)*\]\(([^)]+)\)', text):
        urls.append(m.group(1))
    return urls


class LiveSiteHTMLConverter(HTMLParser):
    """Convert live site article HTML to Markdown.

    Uses English code blocks (by position) and English link URLs (by position).
    """

    def __init__(self, en_code_blocks: list[str], en_link_urls: list[str]):
        super().__init__()
        self.en_code_blocks = en_code_blocks
        self.en_link_urls = en_link_urls
        self.code_block_idx = 0
        self.link_idx = 0
        self.output: list[str] = []
        self.in_pre = False
        self.in_code_block = False
        self.in_inline_code = False
        self.inline_code_parts: list[str] = []
        self.in_link = False
        self.link_text_parts: list[str] = []
        self.link_href = ""
        self.list_stack: list[tuple[str, int]] = []
        self.skip_content = False
        self.li_just_started = False
        self.in_aside = False
        self.aside_parts: list[str] = []
        self.aside_class = ""

    def _emit(self, text: str):
        if self.skip_content or self.in_code_block:
            return
        if self.in_aside:
            self.aside_parts.append(text)
        elif self.in_link:
            self.link_text_parts.append(text)
        elif self.in_inline_code:
            self.inline_code_parts.append(text)
        else:
            self.output.append(text)

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        tag = tag.lower()

        if tag == 'pre':
            self.in_pre = True
            self.in_code_block = True
            self.skip_content = True
            return

        if tag == 'devsite-code':
            self.in_code_block = True
            self.skip_content = True
            return

        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag[1])
            self._emit(f"\n\n{'#' * level} ")
            return

        if tag == 'p':
            if self.li_just_started:
                self.li_just_started = False
            else:
                self._emit("\n\n")
            return

        if tag == 'aside':
            self.in_aside = True
            self.aside_class = attrs_dict.get('class', 'note')
            self.aside_parts = []
            return

        if tag == 'ul':
            self.list_stack.append(('ul', 0))
            return
        if tag == 'ol':
            self.list_stack.append(('ol', 0))
            return
        if tag == 'li':
            if self.list_stack:
                list_type, count = self.list_stack[-1]
                indent = "    " * (len(self.list_stack) - 1)
                if list_type == 'ul':
                    self._emit(f"\n{indent}* ")
                else:
                    count += 1
                    self.list_stack[-1] = (list_type, count)
                    self._emit(f"\n{indent}{count}. ")
            self.li_just_started = True
            return

        if tag in ('strong', 'b'):
            self._emit("**")
            return
        if tag in ('em', 'i'):
            self._emit("*")
            return

        if tag == 'code' and not self.in_pre:
            self.in_inline_code = True
            self.inline_code_parts = []
            return

        if tag == 'a':
            href = attrs_dict.get('href', '')
            self.in_link = True
            self.link_href = href
            self.link_text_parts = []
            return

        if tag == 'br':
            self._emit("\\\n")
            return

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag == 'pre':
            self.in_pre = False
            self.in_code_block = False
            self.skip_content = False
            # Emit English code block
            if self.code_block_idx < len(self.en_code_blocks):
                self._emit(f"\n\n{self.en_code_blocks[self.code_block_idx]}\n")
                self.code_block_idx += 1
            return

        if tag == 'devsite-code':
            self.in_code_block = False
            self.skip_content = False
            return

        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self._emit("\n")
            return

        if tag == 'aside':
            aside_text = ''.join(self.aside_parts).strip()
            # Remove leading labels
            aside_text = re.sub(
                r'^\*\*(?:Important|Importante|Note|Nota|Hinweis|Wichtig|'
                r'Remarque|Ważne|Uwaga|Примечание|Важно|'
                r'注意|注|重要|중요|참고|ملاحظة|مهم|หมายเหตุ|สำคัญ|'
                r'Önemli|Not|Belangrijk|Opmerking)[:\uff1a]?\*\*\s*',
                '', aside_text
            )
            aside_type = "tip" if "special" in self.aside_class else "note"
            if aside_type == "tip":
                self._emit(f"\n\n:::warning\n{aside_text}\n:::\n")
            else:
                self._emit(f"\n\n:::note\n{aside_text}\n:::\n")
            self.in_aside = False
            return

        if tag in ('ul', 'ol'):
            if self.list_stack:
                self.list_stack.pop()
            if not self.list_stack:
                self._emit("\n")
            return

        if tag in ('strong', 'b'):
            self._emit("**")
            return
        if tag in ('em', 'i'):
            self._emit("*")
            return

        if tag == 'code' and self.in_inline_code:
            code_text = ''.join(self.inline_code_parts)
            self.in_inline_code = False
            self._emit(f"`{code_text}`")
            return

        if tag == 'a' and self.in_link:
            link_text = ''.join(self.link_text_parts).strip()
            # Use English link URL if available
            if self.link_idx < len(self.en_link_urls):
                url = self.en_link_urls[self.link_idx]
                self.link_idx += 1
            else:
                url = self.link_href
            self.in_link = False
            self._emit(f"[{link_text}]({url})")
            return

    def handle_data(self, data):
        if self.skip_content or self.in_code_block:
            return
        if self.in_inline_code:
            self.inline_code_parts.append(data)
            return
        self._emit(data)

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

    def handle_comment(self, data):
        # Handle devsite-code placeholders
        data = data.strip()
        match = re.match(
            r'notranslate l10n-placeholder:\s*l10n-placeholder(\d+)', data
        )
        if match:
            if self.code_block_idx < len(self.en_code_blocks):
                self.output.append(
                    f"\n\n{self.en_code_blocks[self.code_block_idx]}\n"
                )
                self.code_block_idx += 1

    def get_markdown(self) -> str:
        text = ''.join(self.output)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


def get_frontmatter() -> str:
    """Get frontmatter from the English doc."""
    en_doc = ENGLISH_DOCS_DIR / f"{DOC_PATH}.md"
    content = en_doc.read_text(encoding="utf-8")
    fm_match = re.match(r'^(---\n.*?\n---\n)', content, re.DOTALL)
    return fm_match.group(1) if fm_match else ""


def main():
    # Read English source
    en_doc = ENGLISH_DOCS_DIR / f"{DOC_PATH}.md"
    en_md = en_doc.read_text(encoding="utf-8")

    # Strip frontmatter for extraction
    en_body = re.sub(r'^---\n.*?\n---\n', '', en_md, count=1, flags=re.DOTALL)

    en_code_blocks = extract_code_blocks_from_md(en_body)
    en_link_urls = extract_link_urls_from_md(en_body)
    frontmatter = get_frontmatter()

    print(f"English source: {len(en_code_blocks)} code blocks, "
          f"{len(en_link_urls)} links")

    success = 0
    for locale in LOCALES:
        url = URL_TEMPLATE.format(locale=locale)
        print(f"\n{locale}: Fetching {url}")

        try:
            html = fetch_page(url)
        except Exception as e:
            print(f"  ERROR fetching: {e}")
            continue

        article = extract_article_body(html)
        if not article:
            print(f"  ERROR: Could not extract article body")
            continue

        converter = LiveSiteHTMLConverter(en_code_blocks, en_link_urls)
        converter.feed(article)
        markdown = converter.get_markdown()

        if not markdown.strip():
            print(f"  ERROR: Empty markdown output")
            continue

        full_content = f"{frontmatter}\n{markdown}\n"

        output_file = (
            OUTPUT_BASE / locale / "docusaurus-plugin-content-docs"
            / "current" / f"{DOC_PATH}.md"
        )
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(full_content, encoding="utf-8")

        print(f"  OK: {len(markdown)} chars, "
              f"code blocks used: {converter.code_block_idx}/{len(en_code_blocks)}, "
              f"links used: {converter.link_idx}/{len(en_link_urls)}")
        success += 1

    print(f"\nDone! Converted {success}/{len(LOCALES)} locales")


if __name__ == "__main__":
    main()
