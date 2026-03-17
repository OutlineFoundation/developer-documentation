#!/usr/bin/env python3
"""Convert translated use-sdk-in-go.md files to .mdx with Tabs.

Renames each locale's use-sdk-in-go.md to .mdx, adds Tabs/TabItem imports,
and converts known ### heading groups into <Tabs> blocks.

Tab groups:
  Step 1: Linux / Mac / Windows  (anchors: #linux, #mac, #windows)
  Step 4: Linux & Mac / Windows  (anchors: #linux-mac, #windows_1)

Note: In both groups, the LAST tab (Windows) has trailing content that
belongs AFTER the tabs, not inside the tab. This script splits the last
tab's content at the first code block boundary.
"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
I18N_BASE = PROJECT_ROOT / "i18n"

LOCALES = [
    "ar", "de", "es", "es-419", "fa", "fr", "it", "ja", "ko",
    "nl", "pl", "pt-BR", "ru", "th", "tr", "zh-CN", "zh-TW",
]

DOC_REL_PATH = "docusaurus-plugin-content-docs/current/sdk/use-sdk-in-go"

MDX_IMPORTS = (
    "\n"
    "import Tabs from '@theme/Tabs';\n"
    "import TabItem from '@theme/TabItem';\n"
)

# Tab groups defined by their anchor IDs.
TAB_GROUPS = [
    {
        "groupId": "os",
        "members": [
            {"anchor": "linux",   "value": "linux",   "label": "Linux"},
            {"anchor": "mac",     "value": "mac",     "label": "Mac"},
            {"anchor": "windows", "value": "windows", "label": "Windows"},
        ],
    },
    {
        "groupId": "os",
        "members": [
            {"anchor": "linux-mac",  "value": "linux",   "label": "Linux & Mac"},
            {"anchor": "windows_1",  "value": "windows", "label": "Windows"},
        ],
    },
]

# Build lookup: anchor -> (group_index, member_index)
ANCHOR_LOOKUP: dict[str, tuple[int, int]] = {}
for _gi, _group in enumerate(TAB_GROUPS):
    for _mi, _member in enumerate(_group["members"]):
        ANCHOR_LOOKUP[_member["anchor"]] = (_gi, _mi)

HEADING_RE = re.compile(r"^###\s+.+?\{#(.+?)\}\s*$")


def find_headings(lines: list[str]) -> list[tuple[int, str, int, int]]:
    """Find all ### headings with known anchor IDs."""
    result = []
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line.rstrip("\n"))
        if m:
            anchor = m.group(1)
            if anchor in ANCHOR_LOOKUP:
                gi, mi = ANCHOR_LOOKUP[anchor]
                result.append((i, anchor, gi, mi))
    return result


def find_content_end(lines: list[str], start: int, group_anchors: set[str]) -> int:
    """Find where a tab's content ends."""
    for i in range(start, len(lines)):
        stripped = lines[i].rstrip("\n")
        if stripped.startswith("## "):
            return i
        m = HEADING_RE.match(stripped)
        if m and m.group(1) not in group_anchors:
            return i
        if stripped.startswith("### ") and not m and i > start:
            return i
    return len(lines)


def split_at_first_code_block(content: str) -> tuple[str, str]:
    """Split content after the first complete code block.

    Returns (tab_content, trailing_content). If no code block is found
    or there's no trailing content, trailing_content is empty.
    """
    content_lines = content.split("\n")
    in_code = False
    code_end = -1

    for idx, line in enumerate(content_lines):
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
            else:
                in_code = False
                code_end = idx
                break

    if code_end == -1:
        return content, ""

    trailing = "\n".join(content_lines[code_end + 1 :]).strip("\n")
    if not trailing.strip():
        return content, ""

    tab_part = "\n".join(content_lines[: code_end + 1]).strip("\n")
    return tab_part, trailing


def convert_content(text: str) -> str:
    """Convert a .md file's content to .mdx with Tabs."""
    lines = text.split("\n")
    headings = find_headings(lines)

    if not headings:
        return add_imports(text)

    replacements: list[tuple[int, int, str]] = []
    i = 0
    while i < len(headings):
        line_idx, anchor, gi, mi = headings[i]
        group = TAB_GROUPS[gi]
        group_anchors = {m["anchor"] for m in group["members"]}

        group_headings = [headings[i]]
        j = i + 1
        while j < len(headings) and headings[j][2] == gi:
            group_headings.append(headings[j])
            j += 1

        tab_contents: list[tuple[dict, str]] = []
        trailing_after_tabs = ""

        for k, (h_line, h_anchor, _, _) in enumerate(group_headings):
            content_start = h_line + 1
            if k + 1 < len(group_headings):
                content_end = group_headings[k + 1][0]
            else:
                content_end = find_content_end(lines, h_line + 1, group_anchors)

            member = next(m for m in group["members"] if m["anchor"] == h_anchor)
            content = "\n".join(lines[content_start:content_end]).strip("\n")

            # For the LAST tab in the group, split off trailing content
            is_last = k == len(group_headings) - 1
            if is_last:
                content, trailing_after_tabs = split_at_first_code_block(content)

            tab_contents.append((member, content))

        last_content_end = find_content_end(
            lines, group_headings[-1][0] + 1, group_anchors
        )

        tabs_lines = [f'<Tabs groupId="{group["groupId"]}">']
        for member, content in tab_contents:
            tabs_lines.append(
                f'<TabItem value="{member["value"]}" label="{member["label"]}">'
            )
            tabs_lines.append("")
            tabs_lines.append(content)
            tabs_lines.append("")
            tabs_lines.append("</TabItem>")
        tabs_lines.append("</Tabs>")

        # Append trailing content after </Tabs>
        if trailing_after_tabs:
            tabs_lines.append("")
            tabs_lines.append(trailing_after_tabs)

        group_start = group_headings[0][0]
        replacements.append((group_start, last_content_end, "\n".join(tabs_lines)))

        i = j

    for start, end, new_text in reversed(replacements):
        lines[start:end] = new_text.split("\n")

    result = "\n".join(lines)
    return add_imports(result)


def add_imports(text: str) -> str:
    """Insert MDX import lines after the frontmatter block."""
    first = text.find("---")
    if first == -1:
        return MDX_IMPORTS + "\n" + text
    second = text.find("---", first + 3)
    if second == -1:
        return MDX_IMPORTS + "\n" + text
    insert_pos = second + 3
    return text[:insert_pos] + "\n" + MDX_IMPORTS + text[insert_pos:]


def main():
    print("Converting translated use-sdk-in-go files to MDX with Tabs")
    print(f"Locales: {len(LOCALES)}")
    print()

    for locale in LOCALES:
        md_path = I18N_BASE / locale / f"{DOC_REL_PATH}.md"
        mdx_path = I18N_BASE / locale / f"{DOC_REL_PATH}.mdx"

        if not md_path.exists():
            print(f"  SKIP {locale}: {md_path.name} not found")
            continue

        text = md_path.read_text(encoding="utf-8")
        heading_count = len(find_headings(text.split("\n")))
        converted = convert_content(text)

        mdx_path.write_text(converted, encoding="utf-8")
        md_path.unlink()

        print(f"  OK {locale}: {heading_count} headings converted -> {mdx_path.name}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
