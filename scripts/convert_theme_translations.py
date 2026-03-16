#!/usr/bin/env python3
"""Convert old-site ARB translation files to Docusaurus theme JSON format.

Reads footer and sidebar translations from Google's ARB (Application Resource
Bundle) export files and generates:
  - i18n/{locale}/docusaurus-theme-classic/footer.json
  - i18n/{locale}/docusaurus-plugin-content-docs/current.json

Usage:
    python3 scripts/convert_theme_translations.py
"""

import json
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "old-site" / "i18n" / "raw"
I18N_DIR = PROJECT_ROOT / "i18n"

# Ordered from oldest to newest so later exports override earlier ones.
EXPORT_DIRS = sorted(RAW_DIR.iterdir()) if RAW_DIR.exists() else []

LOCALES = [
    "ar", "de", "es", "es-419", "fa", "fr", "it", "ja",
    "ko", "nl", "pl", "pt-BR", "ru", "th", "tr", "zh-CN", "zh-TW",
]

# ---------------------------------------------------------------------------
# Manual translations for strings NOT in ARB exports but present on the old
# live site (scraped from developers.google.com/outline?hl={locale}).
# ---------------------------------------------------------------------------
MANUAL_FOOTER_TRANSLATIONS: dict[str, dict[str, str]] = {
    "ar": {"Product Info": "معلومات المنتج", "Terms of Service": "بنود الخدمة"},
    "de": {"Product Info": "Produktinfo", "Terms of Service": "Nutzungsbedingungen"},
    "es": {"Product Info": "Información del producto", "Terms of Service": "Términos del Servicio"},
    "es-419": {"Product Info": "Información sobre el producto", "Terms of Service": "Condiciones del Servicio"},
    "fa": {"Product Info": "اطلاعات محصول", "Terms of Service": "شرایط خدمات"},
    "fr": {"Product Info": "Infos produits", "Terms of Service": "Conditions d'utilisation"},
    "it": {"Product Info": "Informazioni sul prodotto", "Terms of Service": "Termini di servizio"},
    "ja": {"Product Info": "サービス情報", "Terms of Service": "利用規約",
           "Get Help": "ヘルプとサポート", "Help Center": "ヘルプセンター",
           "Branding Guidelines": "ブランド設定のガイドライン", "Contact Us": "お問い合わせ",
           "Download Outline": "Outline をダウンロード", "Data Collection Policy": "データ収集ポリシー"},
    "ko": {"Product Info": "제품 정보", "Terms of Service": "서비스 약관",
           "Get Help": "도움 받기", "Help Center": "고객센터",
           "Branding Guidelines": "브랜드 가이드라인", "Contact Us": "문의하기",
           "Download Outline": "Outline 다운로드", "Data Collection Policy": "데이터 수집 정책"},
    "nl": {"Product Info": "Productgegevens", "Terms of Service": "Servicevoorwaarden"},
    "pl": {"Product Info": "Informacje o produkcie", "Terms of Service": "Warunki usługi",
           "Help Center": "Centrum pomocy"},
    "pt-BR": {"Product Info": "Informações do produto", "Terms of Service": "Termos de Serviço"},
    "ru": {"Product Info": "Информация о продукте", "Terms of Service": "Условия использования"},
    "th": {"Product Info": "ข้อมูลผลิตภัณฑ์", "Terms of Service": "ข้อกำหนดในการให้บริการ"},
    "tr": {"Product Info": "Ürün Bilgileri", "Terms of Service": "Hizmet Şartları"},
    "zh-CN": {"Product Info": "商品信息", "Terms of Service": "服务条款",
              "Help Center": "帮助中心", "Branding Guidelines": "品牌推广指南",
              "Contact Us": "联系我们", "Download Outline": "下载 Outline",
              "Data Collection Policy": "数据收集政策"},
    "zh-TW": {"Product Info": "產品資訊", "Terms of Service": "服務條款",
              "Help Center": "說明中心", "Contact Us": "聯絡我們",
              "Download Outline": "下載 Outline", "Data Collection Policy": "資料收集政策",
              "Branding Guidelines": "品牌宣傳指南"},
}

# Mapping from manual translation English labels to Docusaurus footer.json keys.
MANUAL_KEY_MAP = {
    "Product Info": ("link.title.Product Info",
                     "The title of the footer links column with title=Product Info in the footer"),
    "Terms of Service": ("link.item.label.Terms of Service",
                         "The label of footer link with label=Terms of Service linking to "
                         "https://s3.amazonaws.com/outline-vpn/static_downloads/Outline-Terms-of-Service.html"),
    "Get Help": ("link.title.Get Help",
                 "The title of the footer links column with title=Get Help in the footer"),
    "Help Center": ("link.item.label.Help Center",
                    "The label of footer link with label=Help Center linking to https://support.getoutline.org/"),
    "Branding Guidelines": ("link.item.label.Branding Guidelines",
                            "The label of footer link with label=Branding Guidelines linking to "
                            "https://support.google.com/outline/answer/15331625"),
    "Contact Us": ("link.item.label.Contact Us",
                   "The label of footer link with label=Contact Us linking to "
                   "https://support.getoutline.org/s/contactsupport"),
    "Download Outline": ("link.item.label.Download Outline",
                         "The label of footer link with label=Download Outline linking to https://getoutline.org/"),
    "Data Collection Policy": ("link.item.label.Data Collection Policy",
                               "The label of footer link with label=Data Collection Policy linking to "
                               "https://support.google.com/outline/answer/14915905"),
}

# ---------------------------------------------------------------------------
# String ID → Docusaurus key mappings (from ARB export files)
# ---------------------------------------------------------------------------

# Footer: string_id → Docusaurus footer.json key
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
        "description": "The label of footer link with label=GitHub linking to https://github.com/Jigsaw-Code/?q=outline",
    },
    "15008440364347205577": {
        "key": "link.item.label.Reddit",
        "description": "The label of footer link with label=Reddit linking to https://www.reddit.com/r/outlinevpn/",
    },
    "8548374559130688749": {
        "key": "link.item.label.Branding Guidelines",
        "description": "The label of footer link with label=Branding Guidelines linking to https://support.google.com/outline/answer/15331625",
    },
    "7914285668778184041": {
        "key": "link.item.label.Contact Us",
        "description": "The label of footer link with label=Contact Us linking to https://support.getoutline.org/s/contactsupport",
    },
    "13178819200241644670": {
        "key": "link.title.Get Help",
        "description": "The title of the footer links column with title=Get Help in the footer",
    },
}

# Sidebar: string_id → list of Docusaurus current.json keys
# Some strings map to multiple keys (e.g. "Discover" used in both VPN and SDK).
SIDEBAR_STRING_MAP = {
    "11174858347861414780": {
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
        "english": "Discover",
    },
    "9561751990802477681": {
        "keys": [
            {
                "key": "sidebar.docs.category.Outline SDK",
                "description": "The label for category 'Outline SDK' in sidebar 'docs'",
            },
        ],
        "english": "Outline SDK",
    },
    "14283651073967336439": {
        "keys": [
            {
                "key": "sidebar.docs.category.Integrate",
                "description": "The label for category 'Integrate' in sidebar 'docs'",
            },
        ],
        "english": "Integrate",
    },
    "24655670123343332": {
        "keys": [
            {
                "key": "sidebar.docs.category.Advanced Deployments",
                "description": "The label for category 'Advanced Deployments' in sidebar 'docs'",
            },
        ],
        "english": "Advanced deployments",
    },
    "5165348390719945618": {
        "keys": [
            {
                "key": "sidebar.docs.category.Resilience Against Blocking",
                "description": "The label for category 'Resilience Against Blocking' in sidebar 'docs'",
            },
        ],
        "english": "Increase resilience against blocking",
    },
    "973379579395422503": {
        "keys": [
            {
                "key": "sidebar.docs.link.Management API",
                "description": "The label for link 'Management API' in sidebar 'docs', linking to 'https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/src/shadowbox/server/api.yml'",
            },
        ],
        "english": "Management API",
    },
}


def parse_arb_file(path: Path) -> dict[str, str]:
    """Parse an ARB file and return {string_id: translated_value}."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = {}
    for key, value in data.items():
        if key.startswith("@@"):
            continue
        # Extract string_id from the key metadata
        match = re.search(r"'string_id':\s*'(\d+)'", key)
        if match:
            string_id = match.group(1)
            result[string_id] = value
    return result


def collect_translations(arb_filename: str) -> dict[str, dict[str, str]]:
    """Collect translations across all exports for a given ARB file.

    Returns {locale: {string_id: translated_value}}.
    Later exports override earlier ones.
    """
    all_translations: dict[str, dict[str, str]] = {loc: {} for loc in LOCALES}

    for export_dir in EXPORT_DIRS:
        for locale in LOCALES:
            arb_path = export_dir / locale / "outline" / arb_filename
            if arb_path.exists():
                translations = parse_arb_file(arb_path)
                all_translations[locale].update(translations)

    return all_translations


def generate_footer_json(locale: str, translations: dict[str, str]) -> dict | None:
    """Generate the Docusaurus footer.json content for a locale."""
    result = {}

    # From ARB exports
    for string_id, mapping in FOOTER_STRING_MAP.items():
        if string_id in translations:
            value = translations[string_id]
            result[mapping["key"]] = {
                "message": value,
                "description": mapping["description"],
            }

    # From manual translations (scraped from old site, fills gaps in ARB exports)
    manual = MANUAL_FOOTER_TRANSLATIONS.get(locale, {})
    for en_label, translated in manual.items():
        key_info = MANUAL_KEY_MAP.get(en_label)
        if key_info:
            docusaurus_key, description = key_info
            # Only add if not already set by ARB data
            if docusaurus_key not in result:
                result[docusaurus_key] = {
                    "message": translated,
                    "description": description,
                }

    return result if result else None


def generate_current_json(locale: str, translations: dict[str, str]) -> dict | None:
    """Generate sidebar category translations for current.json."""
    result = {}

    for string_id, mapping in SIDEBAR_STRING_MAP.items():
        if string_id in translations:
            value = translations[string_id]
            for key_info in mapping["keys"]:
                result[key_info["key"]] = {
                    "message": value,
                    "description": key_info["description"],
                }

    return result if result else None


def write_json_file(path: Path, data: dict):
    """Write a JSON file, creating directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def merge_json(existing_path: Path, new_data: dict) -> dict:
    """Merge new translations into an existing JSON file."""
    existing = {}
    if existing_path.exists():
        with open(existing_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    existing.update(new_data)
    return existing


def main():
    print("Collecting footer translations from ARB files...")
    footer_translations = collect_translations("_footer.yaml.arb")

    print("Collecting sidebar translations from ARB files...")
    book_translations = collect_translations("_book.yaml.arb")

    footer_count = 0
    sidebar_count = 0

    for locale in LOCALES:
        # Footer
        footer_data = generate_footer_json(locale, footer_translations[locale])
        if footer_data:
            footer_path = I18N_DIR / locale / "docusaurus-theme-classic" / "footer.json"
            merged = merge_json(footer_path, footer_data)
            write_json_file(footer_path, merged)
            footer_count += 1
            print(f"  {locale}: footer.json - {len(footer_data)} translations")

        # Sidebar categories
        current_data = generate_current_json(locale, book_translations[locale])
        if current_data:
            current_path = I18N_DIR / locale / "docusaurus-plugin-content-docs" / "current.json"
            merged = merge_json(current_path, current_data)
            write_json_file(current_path, merged)
            sidebar_count += 1
            print(f"  {locale}: current.json - {len(current_data)} translations")

    print(f"\nDone! Generated footer.json for {footer_count} locales, "
          f"current.json for {sidebar_count} locales.")

    # Report what's NOT translated
    print("\nFooter strings without old translations (will show in English):")
    print("  - 'Product Info' (section title) — not in translation exports")
    print("  - 'Terms of Service' — not in translation exports")
    print("\nSidebar categories without old translations:")
    print("  - 'Outline VPN' — old site used 'Outline'")
    print("  - 'Get Started' — new category, not in old site")
    print("  - 'Manage & Scale' — old site used 'Manage and scale your server'")
    print("  - 'Reference' — not in translation exports")
    print("  - 'Tools' — not in translation exports")
    print("  - 'Go API Reference' — not in translation exports")


if __name__ == "__main__":
    main()
