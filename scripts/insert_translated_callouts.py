#!/usr/bin/env python3
"""Extract translated callout text from old-site HTML and insert into i18n markdown.

The old Google CMS used <aside class="note|tip|caution|special"> for callouts.
During the HTML-to-Markdown conversion for i18n files, these were dropped.
This script extracts the translated text from the old-site HTML files and
inserts them as Docusaurus admonitions (:::note, :::tip, etc.) into the
current translated Markdown files at the correct positions.
"""

import re
from html import unescape
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
I18N_BASE = PROJECT_ROOT / "i18n"
OLD_SITE_I18N = PROJECT_ROOT / "old-site" / "i18n" / "consolidated"

LOCALES = [
    "ar", "de", "es", "es-419", "fa", "fr", "it", "ja", "ko",
    "nl", "pl", "pt-BR", "ru", "th", "tr", "zh-CN", "zh-TW",
]

DOC_BASE = "docusaurus-plugin-content-docs/current"

# Mapping from old-site HTML paths to current doc paths and their callout specs.
# Each spec defines:
#   old_html: path within old-site/i18n/consolidated/{locale}/
#   current_md: path within i18n/{locale}/docusaurus-plugin-content-docs/current/
#   callouts: list of callout insertion specs, each with:
#     aside_index: 0-based index of the <aside> in the HTML file
#     admonition: the Docusaurus admonition type (note, tip, caution, warning)
#     title: optional custom title (e.g., "Important" for :::warning[Important])
#     position: how to find the insertion point in the markdown:
#       "before_heading": insert before the heading with the given anchor
#       "after_heading": insert after the heading with the given anchor
#       "after_code_block": insert after the N-th code block in section
#       "end_of_file": insert at the end of the file
#     anchor: heading anchor ID (for heading-based positions)
#     section_anchor: anchor of the section containing the code block
#     code_block_index: 0-based index of the code block within the section
FILE_SPECS = [
    {
        "old_html": "docs/download-links.md.html",
        "current_md": "download-links.md",
        "callouts": [
            {
                "aside_index": 0,
                "admonition": "warning",
                "title": "Important",
                "position": "before_heading",
                "anchor": "outline_manager",
            },
        ],
    },
    {
        "old_html": "docs/guides/sdk/use-sdk-in-go.md.html",
        "current_md": "sdk/use-sdk-in-go.mdx",
        "callouts": [
            {
                "aside_index": 0,
                "admonition": "tip",
                "position": "after_code_block",
                "section_anchor": "step_2_create_the_splitfetch_application",
                "code_block_index": 0,
            },
        ],
    },
    {
        "old_html": "docs/guides/sdk/mobile-app-integration.md.html",
        "current_md": "sdk/mobile-app-integration.mdx",
        "callouts": [
            {
                "aside_index": 0,
                "admonition": "note",
                "position": "end_of_file",
            },
        ],
    },
    {
        "old_html": "docs/reference/smart-dialer-config.md.html",
        "current_md": "sdk/reference/smart-dialer-config.md",
        "callouts": [
            {
                "aside_index": 0,
                "admonition": "note",
                "position": "before_heading",
                "anchor": "how_to_use_the_smart_dialer",
            },
        ],
    },
    {
        "old_html": "docs/guides/service-providers/share-access.md.html",
        "current_md": "vpn/getting-started/share-access.md",
        "callouts": [
            {
                "aside_index": 0,
                "admonition": "tip",
                "position": "before_heading",
                "anchor": "user_invitation_process",
            },
        ],
    },
    {
        "old_html": "docs/guides/service-providers/caddy.md.html",
        "current_md": "vpn/advanced/caddy.md",
        "callouts": [
            {
                "aside_index": 0,
                "admonition": "warning",
                "title": "Important",
                "position": "after_code_block",
                "section_anchor": "step_4_configure_and_run_the_caddy_server_with_outline",
                "code_block_index": 0,
            },
            {
                "aside_index": 1,
                "admonition": "note",
                "position": "after_code_block",
                "section_anchor": "step_4_configure_and_run_the_caddy_server_with_outline",
                "code_block_index": 1,
            },
        ],
    },
    {
        "old_html": "docs/guides/service-providers/share-management-access.md.html",
        "current_md": "vpn/management/share-management-access.md",
        "callouts": [
            {
                "aside_index": 0,
                "admonition": "tip",
                "position": "before_heading",
                "anchor": "manual_installations",
            },
            {
                "aside_index": 1,
                "admonition": "caution",
                "position": "after_heading",
                "anchor": "manual_installations",
            },
            {
                "aside_index": 2,
                "admonition": "warning",
                "title": "Important",
                "position": "before_heading",
                "anchor": "3_share_the_access_config_securely",
            },
        ],
    },
    {
        "old_html": "docs/guides/service-providers/websockets.md.html",
        "current_md": "vpn/advanced/websockets.md",
        "callouts": [
            {
                "aside_index": 0,
                "admonition": "note",
                "position": "before_heading",
                "anchor": "step_1_configure_and_run_an_outline_server",
            },
            {
                "aside_index": 1,
                "admonition": "tip",
                "position": "after_code_block",
                "section_anchor": "step_1_configure_and_run_an_outline_server",
                "code_block_index": 0,
            },
            {
                "aside_index": 2,
                "admonition": "caution",
                "position": "after_heading",
                "anchor": "example_using_trycloudflare",
            },
        ],
    },
]


def extract_asides(html_text: str) -> list[str]:
    """Extract text content from <aside> elements in HTML.

    Returns a list of plain text strings (HTML tags converted to markdown).
    The <strong>Label:</strong> prefix is stripped.
    """
    # Find all <aside> elements
    aside_pattern = re.compile(
        r'<aside[^>]*>.*?</aside>',
        re.DOTALL,
    )
    asides = aside_pattern.findall(html_text)

    results = []
    for aside_html in asides:
        # Extract the content after <strong>Label:</strong><span>...</span>
        span_match = re.search(r'<span>\s*(.*?)\s*</span>', aside_html, re.DOTALL)
        if span_match:
            text = span_match.group(1)
        else:
            # Fallback: get everything after </strong>
            strong_match = re.search(r'</strong>\s*(.*?)\s*</aside>', aside_html, re.DOTALL)
            if strong_match:
                text = strong_match.group(1)
            else:
                continue

        # Convert HTML to markdown-friendly text
        text = convert_html_to_md(text)
        results.append(text)

    return results


def convert_html_to_md(html: str) -> str:
    """Convert simple HTML markup to Markdown."""
    # Replace <code>...</code> with `...`
    html = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', html)
    # Replace <strong>...</strong> with **...**
    html = re.sub(r'<strong>(.*?)</strong>', r'**\1**', html)
    # Replace <em>...</em> with *...*
    html = re.sub(r'<em>(.*?)</em>', r'*\1*', html)
    # Replace <a ...>text</a> with just text (links may have placeholder hrefs)
    html = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', html)
    # Replace <var ...>text</var> with `text`
    html = re.sub(r'<var[^>]*>(.*?)</var>', r'`\1`', html)
    # Remove any remaining HTML tags
    html = re.sub(r'<[^>]+>', '', html)
    # Unescape HTML entities
    html = unescape(html)
    # Normalize whitespace (but preserve intentional line structure)
    html = re.sub(r'\s+', ' ', html).strip()
    return html


def find_heading_line(lines: list[str], anchor: str) -> int | None:
    """Find the line index of a heading containing {#anchor}."""
    pattern = re.compile(rf'\{{#\s*{re.escape(anchor)}\s*\}}')
    for i, line in enumerate(lines):
        if pattern.search(line):
            return i
    return None


def find_code_block_end_in_section(
    lines: list[str], section_anchor: str, code_block_index: int
) -> int | None:
    """Find the line index of the closing ``` of the N-th code block in a section."""
    section_start = find_heading_line(lines, section_anchor)
    if section_start is None:
        return None

    # Find the end of this section (next heading of same or higher level)
    heading_match = re.match(r'^(#{1,6})\s', lines[section_start])
    if heading_match:
        section_level = len(heading_match.group(1))
    else:
        section_level = 2

    section_end = len(lines)
    for i in range(section_start + 1, len(lines)):
        heading_m = re.match(r'^(#{1,6})\s', lines[i])
        if heading_m and len(heading_m.group(1)) <= section_level:
            section_end = i
            break

    # Find code blocks within the section
    in_code = False
    block_count = 0
    for i in range(section_start + 1, section_end):
        stripped = lines[i].strip()
        if stripped.startswith("```"):
            if not in_code:
                in_code = True
            else:
                in_code = False
                if block_count == code_block_index:
                    return i
                block_count += 1

    return None


def build_admonition(admonition_type: str, text: str, title: str | None = None) -> str:
    """Build a Docusaurus admonition block."""
    if title:
        header = f":::{admonition_type}[{title}]"
    else:
        header = f":::{admonition_type}"

    return f"\n{header}\n{text}\n:::\n"


def insert_callouts(md_text: str, callout_specs: list[dict], aside_texts: list[str]) -> str:
    """Insert callout admonitions into markdown text at specified positions."""
    lines = md_text.split("\n")

    # Collect all insertions as (line_index, admonition_text) pairs
    # We insert BEFORE the given line index
    insertions: list[tuple[int, str]] = []

    for spec in callout_specs:
        aside_idx = spec["aside_index"]
        if aside_idx >= len(aside_texts):
            continue

        text = aside_texts[aside_idx]
        admonition_type = spec["admonition"]
        title = spec.get("title")
        admonition_block = build_admonition(admonition_type, text, title)

        position = spec["position"]

        if position == "before_heading":
            anchor = spec["anchor"]
            line_idx = find_heading_line(lines, anchor)
            if line_idx is not None:
                insertions.append((line_idx, admonition_block))

        elif position == "after_heading":
            anchor = spec["anchor"]
            line_idx = find_heading_line(lines, anchor)
            if line_idx is not None:
                # Insert after the heading line (and any blank line after it)
                insert_at = line_idx + 1
                while insert_at < len(lines) and lines[insert_at].strip() == "":
                    insert_at += 1
                insertions.append((insert_at, admonition_block))

        elif position == "after_code_block":
            section_anchor = spec["section_anchor"]
            code_block_index = spec["code_block_index"]
            code_end = find_code_block_end_in_section(
                lines, section_anchor, code_block_index
            )
            if code_end is not None:
                # Insert after the closing ``` line
                insertions.append((code_end + 1, admonition_block))

        elif position == "end_of_file":
            insertions.append((len(lines), admonition_block))

    if not insertions:
        return md_text

    # Sort insertions by line index (descending) to preserve indices
    insertions.sort(key=lambda x: x[0], reverse=True)

    for line_idx, admonition_text in insertions:
        admonition_lines = admonition_text.split("\n")
        lines[line_idx:line_idx] = admonition_lines

    return "\n".join(lines)


def main():
    print("Inserting translated callouts into i18n Markdown files")
    print(f"Locales: {len(LOCALES)}")
    print()

    total_inserted = 0
    total_skipped = 0

    for spec in FILE_SPECS:
        old_html_rel = spec["old_html"]
        current_md_rel = spec["current_md"]
        callout_specs = spec["callouts"]

        print(f"  File: {current_md_rel}")

        for locale in LOCALES:
            html_path = OLD_SITE_I18N / locale / old_html_rel
            md_path = I18N_BASE / locale / DOC_BASE / current_md_rel

            if not html_path.exists():
                print(f"    SKIP {locale}: HTML not found ({html_path.name})")
                total_skipped += 1
                continue

            if not md_path.exists():
                print(f"    SKIP {locale}: MD not found ({md_path.name})")
                total_skipped += 1
                continue

            # Read HTML and extract asides
            html_text = html_path.read_text(encoding="utf-8")
            aside_texts = extract_asides(html_text)

            if not aside_texts:
                print(f"    SKIP {locale}: no asides found in HTML")
                total_skipped += 1
                continue

            # Read current markdown
            md_text = md_path.read_text(encoding="utf-8")

            # Check if admonitions already exist (don't double-insert)
            if ":::" in md_text:
                print(f"    SKIP {locale}: admonitions already present")
                total_skipped += 1
                continue

            # Insert callouts
            new_md = insert_callouts(md_text, callout_specs, aside_texts)

            if new_md != md_text:
                md_path.write_text(new_md, encoding="utf-8")
                count = new_md.count(":::")  // 2  # each admonition has open + close
                print(f"    OK {locale}: {count} admonition(s) inserted")
                total_inserted += count
            else:
                print(f"    WARN {locale}: no changes made (insertion points not found)")
                total_skipped += 1

        print()

    print(f"Done. Inserted {total_inserted} total admonitions, skipped {total_skipped}.")


if __name__ == "__main__":
    main()
