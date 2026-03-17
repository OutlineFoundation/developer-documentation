#!/usr/bin/env python3
"""Fix trailing content that was incorrectly placed inside the last TabItem.

In the use-sdk-in-go.mdx translations, text after the last code block in each
tab group's final TabItem was incorrectly included inside the tab. This script
moves that trailing content to after the </Tabs> block.

Specifically:
  Step 1: "verify installation" text + `go version` block after the winget block
  Step 4: "distribute and run" text + `./splitfetch` block after the build block
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

DOC_REL_PATH = "docusaurus-plugin-content-docs/current/sdk/use-sdk-in-go.mdx"


def fix_trailing_content(text: str) -> str:
    """Move trailing content from inside last TabItem to after </Tabs>.

    Finds patterns where a TabItem contains a code block followed by
    non-trivial text before </TabItem>, and moves the trailing text
    to after </Tabs>.
    """
    # Pattern: inside the last TabItem before </Tabs>, find content after
    # the first code block that should be outside the tabs.
    #
    # We look for:
    #   ```<lang>\n...\n```\n\n<trailing text>\n\n</TabItem>\n</Tabs>
    #
    # And rewrite to:
    #   ```<lang>\n...\n```\n\n</TabItem>\n</Tabs>\n\n<trailing text>

    # Match a TabItem that contains: code block, then trailing text, then close
    pattern = re.compile(
        r'(<TabItem[^>]*>)'           # Opening TabItem tag
        r'\n\n'
        r'(```\w*\n.*?\n```)'         # First code block (the actual tab content)
        r'\n\n'
        r'(.+?)'                      # Trailing content (non-empty, non-greedy)
        r'\n\n'
        r'</TabItem>'                 # Close TabItem
        r'\n'
        r'</Tabs>',                   # Close Tabs
        re.DOTALL
    )

    def replacer(m):
        tab_open = m.group(1)
        code_block = m.group(2)
        trailing = m.group(3)

        # Only fix if trailing content has substantial text (not just whitespace)
        if trailing.strip():
            return (
                f'{tab_open}\n\n'
                f'{code_block}\n\n'
                f'</TabItem>\n'
                f'</Tabs>\n\n'
                f'{trailing}'
            )
        return m.group(0)

    result = pattern.sub(replacer, text)
    return result


def main():
    print("Fixing trailing content in use-sdk-in-go.mdx translations")
    print()

    for locale in LOCALES:
        path = I18N_BASE / locale / DOC_REL_PATH
        if not path.exists():
            print(f"  SKIP {locale}: not found")
            continue

        original = path.read_text(encoding="utf-8")
        fixed = fix_trailing_content(original)

        if fixed != original:
            path.write_text(fixed, encoding="utf-8")
            print(f"  FIXED {locale}")
        else:
            print(f"  OK {locale}: no trailing content found")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
