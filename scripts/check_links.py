#!/usr/bin/env python3
"""Check external URLs in English docs for dead links."""

import re
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

DOCS_DIR = Path(__file__).parent.parent / "docs"
DOC_EXTENSIONS = (".md", ".mdx")

# URLs to skip (templates with placeholders, localhost, etc.)
SKIP_PATTERNS = [
    "<",  # URLs with placeholder variables like <DOMAIN_NAME>
    "localhost",
    "127.0.0.1",
    "1.1.1.1",
    "example.com",
]


def extract_urls(text: str) -> list[str]:
    """Extract all http/https URLs from markdown text."""
    urls = set()
    # Markdown links [text](url)
    for m in re.finditer(r'\[(?:[^\]\\]|\\.)*\]\((https?://[^)]+)\)', text):
        urls.add(m.group(1))
    # Auto-links <url>
    for m in re.finditer(r'<(https?://[^>]+)>', text):
        urls.add(m.group(1))
    return sorted(urls)


def should_skip(url: str) -> bool:
    for pattern in SKIP_PATTERNS:
        if pattern in url:
            return True
    return False


def find_urls_in_docs() -> dict[str, list[str]]:
    """Return {url: [files]} mapping for all external URLs in docs."""
    url_files: dict[str, list[str]] = {}
    for ext in DOC_EXTENSIONS:
        for f in DOCS_DIR.rglob(f"*{ext}"):
            text = f.read_text(encoding="utf-8")
            rel = str(f.relative_to(DOCS_DIR.parent))
            for url in extract_urls(text):
                if not should_skip(url):
                    url_files.setdefault(url, []).append(rel)
    return url_files


def check_url(url: str) -> tuple[str, int | str]:
    """Check a URL with curl and return (url, status_code_or_error)."""
    try:
        result = subprocess.run(
            [
                "curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}",
                "-L",  # follow redirects
                "--max-time", "15",
                "-A", "Mozilla/5.0 (link checker)",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=20,
        )
        code = int(result.stdout.strip())
        return url, code
    except Exception as e:
        return url, str(e)


def main():
    url_files = find_urls_in_docs()
    urls = sorted(url_files.keys())
    print(f"Checking {len(urls)} unique external URLs...\n")

    dead = []
    ok = 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(check_url, url): url for url in urls}
        for future in as_completed(futures):
            url, result = future.result()
            if isinstance(result, int) and 200 <= result < 400:
                ok += 1
            else:
                files = url_files[url]
                dead.append((url, result, files))
                print(f"  DEAD [{result}] {url}")
                for f in files:
                    print(f"    in {f}")

    print(f"\n{ok} OK, {len(dead)} dead")
    if dead:
        sys.exit(1)
    else:
        print("PASSED: All external links are alive")
        sys.exit(0)


if __name__ == "__main__":
    main()
