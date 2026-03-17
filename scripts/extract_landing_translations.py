#!/usr/bin/env python3
"""Extract landing page translations from ARB files in git history.

Reads ARB files from commit d002433 and merges homepage.* keys into
each locale's i18n/{locale}/code.json (the standard Docusaurus format
used by the <Translate> component).
"""

import json
import re
import subprocess
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

# Map ARB string IDs to Docusaurus code.json keys (homepage.* namespace).
STRING_ID_MAP = {
    "4714933795543261808":  "homepage.hero.title",
    "15382119321615313379": "homepage.hero.subtitle",
    "5741185159326847292":  "homepage.vpn.title",
    "5298310139302477817":  "homepage.vpn.description",
    "14568915982959444301": "homepage.sdk.title",
    "16175847523331289419": "homepage.sdk.description",
    "16307006558545484432": "homepage.sdk.button",
    "5390667592179359516":  "homepage.vpn.button",
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
        m = re.search(r"'string_id':\s*'(\d+)'", key)
        if not m:
            continue
        string_id = m.group(1)
        if string_id in STRING_ID_MAP:
            translation_key = STRING_ID_MAP[string_id]
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

        # Read existing code.json if present, merge in homepage keys.
        code_path = I18N_BASE / locale / "code.json"
        code_path.parent.mkdir(parents=True, exist_ok=True)
        existing = {}
        if code_path.exists():
            existing = json.loads(code_path.read_text(encoding="utf-8"))

        # Remove any old homepage.* keys, then add fresh ones.
        existing = {k: v for k, v in existing.items() if not k.startswith("homepage.")}
        for key, message in sorted(translations.items()):
            existing[key] = {"message": message}

        with open(code_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
            f.write("\n")

        print(f"  OK {locale}: {len(translations)} strings -> {code_path.relative_to(PROJECT_ROOT)}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
