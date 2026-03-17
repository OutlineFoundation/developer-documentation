#!/usr/bin/env python3
"""Extract landing page translations from ARB files in git history.

Reads ARB files from commit d002433 and writes landingpage.json files
for each locale under i18n/{locale}/landingpage.json.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
I18N_BASE = PROJECT_ROOT / "i18n"

COMMIT = "d002433"
ARB_BASE_PATH = "old-site/i18n/raw/2024-12-21_project_4198229"

LOCALES = [
    "ar", "de", "en", "es", "es-419", "fa", "fr", "it", "ja", "ko",
    "nl", "pl", "pt-BR", "ru", "th", "tr", "zh-CN", "zh-TW",
]

# Map ARB string IDs to landingpage.json keys
STRING_ID_MAP = {
    "4714933795543261808": "hero.title",
    "15382119321615313379": "hero.subtitle",
    "5741185159326847292": "vpn.title",
    "5298310139302477817": "vpn.description",
    "14568915982959444301": "sdk.title",
    "16175847523331289419": "sdk.description",
    "16307006558545484432": "sdk.button",
    "5390667592179359516": "vpn.button",
}


def read_arb_from_git(locale: str) -> dict:
    """Read and parse an ARB file from git history."""
    git_path = f"{ARB_BASE_PATH}/{locale}/outline/_index.yaml.arb"
    result = subprocess.run(
        ["git", "show", f"{COMMIT}:{git_path}"],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    if result.returncode != 0:
        print(f"  WARNING: Could not read ARB for {locale}: {result.stderr.strip()}")
        return {}
    return json.loads(result.stdout)


def extract_translations(arb_data: dict) -> dict:
    """Extract landing page strings from ARB data.

    ARB keys are Python-dict-like strings containing a 'string_id' field.
    We match on string_id to find the translations we need.
    """
    translations = {}
    for key, value in arb_data.items():
        if key.startswith("@@"):
            continue
        # Extract string_id from the key
        m = re.search(r"'string_id':\s*'(\d+)'", key)
        if not m:
            continue
        string_id = m.group(1)
        if string_id in STRING_ID_MAP:
            translation_key = STRING_ID_MAP[string_id]
            # Strip trailing whitespace/newlines from values
            translations[translation_key] = value.strip()
    return translations


def main():
    print(f"Extracting landing page translations from git commit {COMMIT}")
    print(f"Locales: {len(LOCALES)}")
    print()

    for locale in LOCALES:
        arb_data = read_arb_from_git(locale)
        if not arb_data:
            print(f"  SKIP {locale}: no ARB data")
            continue

        translations = extract_translations(arb_data)
        missing = set(STRING_ID_MAP.values()) - set(translations.keys())
        if missing:
            print(f"  WARNING {locale}: missing keys: {missing}")

        out_path = I18N_BASE / locale / "landingpage.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
            f.write("\n")

        print(f"  OK {locale}: {len(translations)} strings -> {out_path.relative_to(PROJECT_ROOT)}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
