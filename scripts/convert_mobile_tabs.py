#!/usr/bin/env python3
"""Convert translated mobile-app-integration.md files to .mdx with Tabs.

Renames each locale's mobile-app-integration.md to .mdx, adds Tabs/TabItem
imports, and converts known ### heading groups into <Tabs> blocks.

The translated files use a consistent pattern of `### Heading {#anchor_id}`
with well-known anchor IDs that identify platform or library tabs.
"""

import re
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
I18N_BASE = PROJECT_ROOT / "i18n"

LOCALES = [
    "ar", "de", "es", "es-419", "fa", "fr", "it", "ja", "ko",
    "nl", "pl", "pt-BR", "ru", "th", "tr", "zh-CN", "zh-TW",
]

DOC_REL_PATH = "docusaurus-plugin-content-docs/current/sdk/mobile-app-integration"

MDX_IMPORTS = (
    "\n"
    "import Tabs from '@theme/Tabs';\n"
    "import TabItem from '@theme/TabItem';\n"
)

# Tab groups defined by their anchor IDs (consistent across all locales).
TAB_GROUPS = [
    {
        "groupId": "platform",
        "members": [
            {"anchor": "android",   "value": "android", "label": "Android"},
            {"anchor": "ios",       "value": "ios",     "label": "iOS"},
        ],
    },
    {
        "groupId": "platform",
        "members": [
            {"anchor": "android_1", "value": "android", "label": "Android"},
            {"anchor": "ios_1",     "value": "ios",     "label": "iOS"},
        ],
    },
    {
        "groupId": "platform",
        "members": [
            {"anchor": "android_2", "value": "android", "label": "Android"},
            {"anchor": "ios_2",     "value": "ios",     "label": "iOS"},
        ],
    },
    {
        "groupId": "http-client",
        "members": [
            {"anchor": "dartflutter-httpclient", "value": "dart",           "label": "Dart/Flutter HttpClient"},
            {"anchor": "okhttp-android",         "value": "okhttp",         "label": "OkHttp (Android)"},
            {"anchor": "jvm-java,-kotlin",       "value": "jvm",            "label": "JVM (Java, Kotlin)"},
            {"anchor": "android-web-view",       "value": "android-webview","label": "Android Web View"},
            {"anchor": "ios-web-view",           "value": "ios-webview",    "label": "iOS Web View"},
        ],
    },
]

# Build lookup: anchor -> (group_index, member_index)
ANCHOR_LOOKUP: dict[str, tuple[int, int]] = {}
for _gi, _group in enumerate(TAB_GROUPS):
    for _mi, _member in enumerate(_group["members"]):
        ANCHOR_LOOKUP[_member["anchor"]] = (_gi, _mi)

# All known anchors across all groups
ALL_ANCHORS = set(ANCHOR_LOOKUP.keys())

HEADING_RE = re.compile(r"^###\s+.+?\{#(.+?)\}\s*$")


def find_headings(lines: list[str]) -> list[tuple[int, str, int, int]]:
    """Find all ### headings with known anchor IDs.

    Returns list of (line_index, anchor, group_index, member_index).
    """
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
    """Find where a tab's content ends.

    Scans from `start` until hitting a ## heading, a ### heading outside the
    current group, or end of file.
    """
    for i in range(start, len(lines)):
        stripped = lines[i].rstrip("\n")
        if stripped.startswith("## "):
            return i
        m = HEADING_RE.match(stripped)
        if m and m.group(1) not in group_anchors:
            return i
        # Also stop at ### headings without anchors
        if stripped.startswith("### ") and not m and i > start:
            return i
    return len(lines)


def convert_content(text: str) -> str:
    """Convert a .md file's content to .mdx with Tabs."""
    lines = text.split("\n")
    headings = find_headings(lines)

    if not headings:
        # No known headings found; just add imports after frontmatter
        return add_imports(text)

    # Process heading groups and build replacements (start_line, end_line, new_text)
    replacements: list[tuple[int, int, str]] = []
    i = 0
    while i < len(headings):
        line_idx, anchor, gi, mi = headings[i]
        group = TAB_GROUPS[gi]
        group_anchors = {m["anchor"] for m in group["members"]}

        # Collect consecutive headings belonging to this group
        group_headings = [headings[i]]
        j = i + 1
        while j < len(headings) and headings[j][2] == gi:
            group_headings.append(headings[j])
            j += 1

        # Determine content range for each tab
        tab_contents: list[tuple[dict, str]] = []
        for k, (h_line, h_anchor, _, _) in enumerate(group_headings):
            content_start = h_line + 1
            if k + 1 < len(group_headings):
                content_end = group_headings[k + 1][0]
            else:
                content_end = find_content_end(lines, h_line + 1, group_anchors)

            member = next(m for m in group["members"] if m["anchor"] == h_anchor)
            content = "\n".join(lines[content_start:content_end]).strip("\n")
            tab_contents.append((member, content))

        # Build the <Tabs> block
        last_content_end = (
            find_content_end(lines, group_headings[-1][0] + 1, group_anchors)
            if len(group_headings) > 0
            else group_headings[-1][0] + 1
        )

        tabs_lines = [f'<Tabs groupId="{group["groupId"]}">']
        for member, content in tab_contents:
            tabs_lines.append(f'<TabItem value="{member["value"]}" label="{member["label"]}">')
            tabs_lines.append("")
            tabs_lines.append(content)
            tabs_lines.append("")
            tabs_lines.append("</TabItem>")
        tabs_lines.append("</Tabs>")

        group_start = group_headings[0][0]
        replacements.append((group_start, last_content_end, "\n".join(tabs_lines)))

        i = j

    # Apply replacements in reverse to preserve line numbers
    for start, end, new_text in reversed(replacements):
        lines[start:end] = new_text.split("\n")

    result = "\n".join(lines)
    return add_imports(result)


def add_imports(text: str) -> str:
    """Insert MDX import lines after the frontmatter block."""
    # Find the second '---' that closes frontmatter
    first = text.find("---")
    if first == -1:
        return MDX_IMPORTS + "\n" + text
    second = text.find("---", first + 3)
    if second == -1:
        return MDX_IMPORTS + "\n" + text
    insert_pos = second + 3
    return text[:insert_pos] + "\n" + MDX_IMPORTS + text[insert_pos:]


def main():
    print("Converting translated mobile-app-integration files to MDX with Tabs")
    print(f"Locales: {len(LOCALES)}")
    print()

    for locale in LOCALES:
        md_path = I18N_BASE / locale / f"{DOC_REL_PATH}.md"
        mdx_path = I18N_BASE / locale / f"{DOC_REL_PATH}.mdx"

        if not md_path.exists():
            print(f"  SKIP {locale}: {md_path.name} not found")
            continue

        text = md_path.read_text(encoding="utf-8")

        # Count known headings before conversion
        heading_count = len(find_headings(text.split("\n")))

        converted = convert_content(text)

        mdx_path.write_text(converted, encoding="utf-8")
        md_path.unlink()

        print(f"  OK {locale}: {heading_count} headings converted -> {mdx_path.name}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
