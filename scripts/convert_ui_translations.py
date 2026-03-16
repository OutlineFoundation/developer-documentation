#!/usr/bin/env python3
"""Convert footer and sidebar translations from old ARB files to Docusaurus i18n JSON format.

Reads Google's ARB (Application Resource Bundle) translation exports and generates:
- i18n/{locale}/docusaurus-theme-classic/footer.json
- i18n/{locale}/docusaurus-plugin-content-docs/current.json
"""

import json
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD_SITE_RAW = os.path.join(PROJECT_ROOT, "old-site", "i18n", "raw")
I18N_DIR = os.path.join(PROJECT_ROOT, "i18n")

LOCALES = [
    "ar", "de", "es", "es-419", "fa", "fr", "it", "ja",
    "ko", "nl", "pl", "pt-BR", "ru", "th", "tr", "zh-CN", "zh-TW",
]

# Footer: string_id -> Docusaurus footer.json key
FOOTER_STRING_MAP = {
    "11712707079961707559": {
        "key": "link.item.label.Download Outline",
        "description": "The label of footer link with label=Download Outline linking to https://getoutline.org/",
    },
    "1456459139838371626": {
        "key": "link.item.label.Data Collection Policy",
        "description": "The label of footer link with label=Data Collection Policy linking to https://support.google.com/outline/answer/14915905",
    },
    "272161972865017920": {
        "key": "link.item.label.Help Center",
        "description": "The label of footer link with label=Help Center linking to https://support.getoutline.org/",
    },
    "431604438871611837": {
        "key": "link.item.label.GitHub",
        "description": "The label of footer link with label=GitHub linking to https://github.com/OutlineFoundation/?q=outline",
    },
    "15008440364347205577": {
        "key": "link.item.label.Reddit",
        "description": "The label of footer link with label=Reddit linking to https://www.reddit.com/r/outlinevpn/",
    },
}

# Sidebar: string_id -> Docusaurus current.json key
# Only include strings that match current sidebar category names
SIDEBAR_STRING_MAP = {
    "9561751990802477681": {
        "key": "sidebar.docs.category.Outline SDK",
        "description": "The label for category 'Outline SDK' in sidebar 'docs'",
    },
    "11174858347861414780": {
        # "Discover" maps to both vpn-discover and sdk-discover
        "keys": [
            {
                "key": "sidebar.docs.category.vpn-discover",
                "description": "The label for category 'Discover' in sidebar 'docs'",
            },
            {
                "key": "sidebar.docs.category.sdk-discover",
                "description": "The label for category 'Discover' in sidebar 'docs'",
            },
        ],
    },
    "14283651073967336439": {
        "key": "sidebar.docs.category.Integrate",
        "description": "The label for category 'Integrate' in sidebar 'docs'",
    },
    "24655670123343332": {
        "key": "sidebar.docs.category.Advanced Deployments",
        "description": "The label for category 'Advanced Deployments' in sidebar 'docs'",
    },
    "5165348390719945618": {
        "key": "sidebar.docs.category.Resilience Against Blocking",
        "description": "The label for category 'Resilience Against Blocking' in sidebar 'docs'",
    },
}


def parse_arb_file(filepath):
    """Parse an ARB file and return a dict of string_id -> translated value."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = {}
    for key, value in data.items():
        if key.startswith("@@"):
            continue
        # Extract string_id from the key metadata
        match = re.search(r"'string_id':\s*'(\d+)'", key)
        if match:
            string_id = match.group(1)
            result[string_id] = value.strip()
    return result


def load_footer_translations(locale):
    """Load footer translations for a locale, preferring the latest export."""
    translations = {}

    # Load from 2024-12-21 first (base), then overlay 2025-01-06 (update)
    for export_dir in ["2024-12-21_project_4198229", "2025-01-06_project_4199184"]:
        arb_path = os.path.join(OLD_SITE_RAW, export_dir, locale, "outline", "_footer.yaml.arb")
        if os.path.exists(arb_path):
            translations.update(parse_arb_file(arb_path))

    return translations


def load_sidebar_translations(locale):
    """Load sidebar/book translations for a locale from the latest export."""
    translations = {}

    # Use the latest _book.yaml.arb export
    for export_dir in ["2025-02-23_project_4390670", "2025-06-23_project_4452804"]:
        arb_path = os.path.join(OLD_SITE_RAW, export_dir, locale, "outline", "_book.yaml.arb")
        if os.path.exists(arb_path):
            translations.update(parse_arb_file(arb_path))

    return translations


def generate_footer_json(locale):
    """Generate the Docusaurus footer.json for a locale."""
    translations = load_footer_translations(locale)
    footer = {}

    for string_id, mapping in FOOTER_STRING_MAP.items():
        if string_id in translations:
            translated = translations[string_id]
            footer[mapping["key"]] = {
                "message": translated,
                "description": mapping["description"],
            }

    return footer


def generate_current_json(locale):
    """Generate sidebar category entries for current.json."""
    translations = load_sidebar_translations(locale)
    current = {}

    for string_id, mapping in SIDEBAR_STRING_MAP.items():
        if string_id in translations:
            translated = translations[string_id]
            if "keys" in mapping:
                # One translation maps to multiple Docusaurus keys
                for entry in mapping["keys"]:
                    current[entry["key"]] = {
                        "message": translated,
                        "description": entry["description"],
                    }
            else:
                current[mapping["key"]] = {
                    "message": translated,
                    "description": mapping["description"],
                }

    return current


def write_json_file(filepath, data):
    """Write a JSON file, creating directories as needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    total_footer = 0
    total_sidebar = 0

    for locale in LOCALES:
        # Footer translations
        footer_data = generate_footer_json(locale)
        if footer_data:
            footer_path = os.path.join(
                I18N_DIR, locale, "docusaurus-theme-classic", "footer.json"
            )
            # Merge with existing file if present
            if os.path.exists(footer_path):
                with open(footer_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                existing.update(footer_data)
                footer_data = existing

            write_json_file(footer_path, footer_data)
            total_footer += len(footer_data)
            print(f"  {locale}: footer.json - {len(footer_data)} translations")

        # Sidebar translations
        current_data = generate_current_json(locale)
        if current_data:
            current_path = os.path.join(
                I18N_DIR, locale, "docusaurus-plugin-content-docs", "current.json"
            )
            # Merge with existing file if present
            if os.path.exists(current_path):
                with open(current_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                existing.update(current_data)
                current_data = existing

            write_json_file(current_path, current_data)
            total_sidebar += len(current_data)
            print(f"  {locale}: current.json - {len(current_data)} translations")

    print(f"\nTotal: {total_footer} footer entries, {total_sidebar} sidebar entries across {len(LOCALES)} locales")

    # Report what's missing
    print("\nNote: The following footer strings have no ARB translations:")
    print("  - 'Terms of Service' (link label)")
    print("  - 'Product' (section title)")
    print("  - 'Community' (section title)")
    print("\nNote: The following sidebar categories have no ARB translations:")
    print("  - 'Outline VPN'")
    print("  - 'Get Started'")
    print("  - 'Manage & Scale'")
    print("  - 'Reference'")
    print("  - 'Tools'")


if __name__ == "__main__":
    main()
