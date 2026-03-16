#!/usr/bin/env python3
"""
Fix list formatting in translated what-is-the-sdk.md files.

The conversion produced:
    - **Bold text**\

    Description paragraph (not indented)

But it should be:
    - **Bold text**\
      Description paragraph (indented, part of list item)
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
I18N_DIR = PROJECT_ROOT / "i18n"

LOCALES = [
    "ar", "de", "es", "es-419", "fa", "fr", "it", "ja", "ko",
    "nl", "pl", "pt-BR", "ru", "th", "tr", "zh-CN", "zh-TW",
]


def fix_list_items(content: str) -> str:
    """Fix list items where bold heading has \\ + blank line + unindented description."""
    lines = content.split('\n')
    result = []
    i = 0
    while i < len(lines):
        # Pattern: "- **text**\" followed by blank line followed by unindented text
        if (re.match(r'^- \*\*.*\*\*\\$', lines[i])
                and i + 2 < len(lines)
                and lines[i + 1].strip() == ''
                and lines[i + 2].strip() != ''
                and not lines[i + 2].startswith('- ')
                and not lines[i + 2].startswith('#')):
            # Keep the list item heading line
            result.append(lines[i])
            # Skip the blank line
            i += 1
            # Indent the description lines (until next blank line or list item)
            i += 1
            while i < len(lines) and lines[i].strip() != '' and not lines[i].startswith('- ') and not lines[i].startswith('#'):
                result.append('  ' + lines[i])
                i += 1
        else:
            result.append(lines[i])
            i += 1
    return '\n'.join(result)


def main():
    total_fixed = 0
    for locale in LOCALES:
        filepath = (
            I18N_DIR / locale / "docusaurus-plugin-content-docs" / "current"
            / "sdk" / "what-is-the-sdk.md"
        )
        if not filepath.exists():
            print(f"  SKIP {locale}: file does not exist")
            continue

        content = filepath.read_text(encoding="utf-8")
        fixed = fix_list_items(content)
        if fixed != content:
            filepath.write_text(fixed, encoding="utf-8")
            print(f"  FIXED {locale}")
            total_fixed += 1
        else:
            print(f"  OK    {locale} (no changes needed)")

    print(f"\nFixed {total_fixed} files")


if __name__ == "__main__":
    main()
