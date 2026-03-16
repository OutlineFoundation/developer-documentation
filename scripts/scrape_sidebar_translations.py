#!/usr/bin/env python3
"""Scrape sidebar and page translations from the old Google Developers site.

Uses curl to fetch developers.google.com/outline pages with ?hl= locale
parameters and extracts translated sidebar category names and page content.

Usage:
    python3 scripts/scrape_sidebar_translations.py
"""

import json
import re
import subprocess
import sys
from html import unescape

LOCALES = [
    "ar", "de", "es", "es-419", "fa", "fr", "it", "ja",
    "ko", "nl", "pl", "pt-BR", "ru", "th", "tr", "zh-CN", "zh-TW",
]

# Pages to fetch for sidebar extraction (VPN and SDK sections)
SIDEBAR_URLS = {
    "vpn": "https://developers.google.com/outline/docs/guides/vpn/why-outline?hl={locale}",
    "sdk": "https://developers.google.com/outline/docs/guides/sdk/what-is-the-sdk?hl={locale}",
}

# The command-line-debugging page
CMD_DEBUG_URL = "https://developers.google.com/outline/docs/guides/sdk/command-line-debugging?hl={locale}"


def fetch_page(url: str) -> str:
    """Fetch a URL using curl and return its content."""
    result = subprocess.run(
        ["curl", "-sL", "--max-time", "30", url],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr}")
    return result.stdout


def extract_sidebar_items(html: str) -> list[str]:
    """Extract sidebar navigation category labels from the HTML."""
    items = re.findall(
        r'<span[^>]*class="[^"]*devsite-nav-title[^"]*"[^>]*>\s*(.*?)\s*</span>',
        html,
        re.DOTALL,
    )
    cleaned = []
    for item in items:
        text = unescape(re.sub(r"<[^>]+>", "", item).strip())
        if text:
            cleaned.append(text)
    return cleaned


def extract_page_title(html: str) -> str | None:
    """Extract the page title (h1) from the HTML."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    if m:
        return unescape(re.sub(r"<[^>]+>", "", m.group(1)).strip())
    return None


def extract_page_body(html: str) -> str | None:
    """Extract the main article content from the HTML."""
    m = re.search(
        r'<div[^>]*class="[^"]*devsite-article-body[^"]*"[^>]*>(.*?)</div>\s*</article>',
        html,
        re.DOTALL,
    )
    if m:
        return m.group(1)
    return None


def extract_tab_labels(html: str) -> list[str]:
    """Extract tab labels (Guides, Reference, Support) from the page."""
    # Look for the upper tabs navigation
    tabs = re.findall(
        r'<tab[^>]*>\s*<a[^>]*>\s*(.*?)\s*</a>\s*</tab>',
        html,
        re.DOTALL,
    )
    if not tabs:
        tabs = re.findall(
            r'class="devsite-upper-tab-name"[^>]*>(.*?)</',
            html,
            re.DOTALL,
        )
    return [unescape(re.sub(r"<[^>]+>", "", t).strip()) for t in tabs if t.strip()]


def main():
    # English reference first
    print("=== Fetching English reference ===")
    en_sidebar_items = {}
    en_tabs = []
    for section, url_template in SIDEBAR_URLS.items():
        url = url_template.format(locale="en")
        print(f"  Fetching {section}: {url}")
        html = fetch_page(url)
        items = extract_sidebar_items(html)
        en_sidebar_items[section] = items
        print(f"    Sidebar items: {items}")
        tabs = extract_tab_labels(html)
        if tabs:
            en_tabs = tabs
            print(f"    Tab labels: {tabs}")

    # English command-line-debugging
    url = CMD_DEBUG_URL.format(locale="en")
    print(f"  Fetching command-line-debugging: {url}")
    html = fetch_page(url)
    en_title = extract_page_title(html)
    print(f"    Title: {en_title}")

    # Now fetch all locales
    results: dict[str, dict[str, str]] = {locale: {} for locale in LOCALES}
    cmd_debug_titles: dict[str, str] = {}

    for locale in LOCALES:
        print(f"\n=== {locale} ===")
        for section, url_template in SIDEBAR_URLS.items():
            url = url_template.format(locale=locale)
            print(f"  Fetching {section}...")
            try:
                html = fetch_page(url)
                items = extract_sidebar_items(html)
                print(f"    Sidebar: {items}")
                tabs = extract_tab_labels(html)
                if tabs:
                    print(f"    Tabs: {tabs}")
                    # Map tabs by position to English tabs
                    for i, en_tab in enumerate(en_tabs):
                        if i < len(tabs):
                            results[locale][en_tab] = tabs[i]

                # Map translated items to English by position
                en_items = en_sidebar_items.get(section, [])
                for i, en_item in enumerate(en_items):
                    if i < len(items):
                        results[locale][en_item] = items[i]
            except Exception as e:
                print(f"    ERROR: {e}")

        # Command-line debugging page
        url = CMD_DEBUG_URL.format(locale=locale)
        print(f"  Fetching command-line-debugging...")
        try:
            html = fetch_page(url)
            title = extract_page_title(html)
            if title:
                cmd_debug_titles[locale] = title
                print(f"    Title: {title}")
        except Exception as e:
            print(f"    ERROR: {e}")

    # Output as Python dicts
    print("\n\n" + "=" * 70)
    print("SCRAPED_SIDEBAR_TRANSLATIONS = {")
    for locale in LOCALES:
        entries = results[locale]
        if entries:
            print(f'    "{locale}": {{')
            for k, v in sorted(entries.items()):
                print(f'        "{k}": "{v}",')
            print("    },")
    print("}")

    print(f"\nCMD_DEBUG_TITLES = {{")
    for locale in LOCALES:
        if locale in cmd_debug_titles:
            print(f'    "{locale}": "{cmd_debug_titles[locale]}",')
    print("}")


if __name__ == "__main__":
    main()
