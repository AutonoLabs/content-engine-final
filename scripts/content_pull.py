#!/usr/bin/env python3
"""
Pull content from URLs (articles, YouTube, etc.) for research/content input.

Uses fallback chain: playwright → blotato source → curl+BeautifulSoup → ask user.

Usage:
    python scripts/content_pull.py --url "https://..." --type article
    python scripts/content_pull.py --url "https://youtube.com/..." --type youtube
    python scripts/content_pull.py --url "https://..." --type perplexity-query --query "..."
"""

import argparse
import os
import sys
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def try_playwright(url: str) -> Optional[str]:
    """Try Playwright for SPA-heavy sites."""
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            content = page.content()
            browser.close()
            return content
    except ImportError:
        print("⚠️  Playwright not installed (pip install playwright; playwright install chromium)")
        return None
    except Exception as e:
        print(f"⚠️  Playwright failed: {e}")
        return None


def try_blotato_source(url: str, source_type: str = "article") -> Optional[str]:
    """Try Blotato source extraction (handles YouTube, articles, etc.)."""
    blotato_key = os.getenv("BLOTATO_API_KEY")
    if not blotato_key:
        return None

    try:
        response = requests.post(
            "https://api.blotato.com/v1/sources",
            headers={"Authorization": f"Bearer {blotato_key}"},
            json={"sourceType": source_type, "url": url},
            timeout=60
        )
        response.raise_for_status()
        result = response.json()

        # Poll for completion
        source_id = result.get("id")
        for _ in range(40):  # up to 40 * 5s = 200s
            status_response = requests.get(
                f"https://api.blotato.com/v1/sources/{source_id}/status",
                headers={"Authorization": f"Bearer {blotato_key}"},
                timeout=30
            )
            status_response.raise_for_status()
            status = status_response.json()

            if status.get("status") == "completed":
                return status.get("content", "")
            elif status.get("status") == "failed":
                print(f"⚠️  Blotato source extraction failed: {status.get('errorMessage')}")
                return None

            import time
            time.sleep(5)

        print("⚠️  Blotato source extraction timed out")
        return None

    except Exception as e:
        print(f"⚠️  Blotato source failed: {e}")
        return None


def try_curl_bs4(url: str) -> Optional[str]:
    """Try simple curl + BeautifulSoup fallback."""
    try:
        from bs4 import BeautifulSoup
        response = requests.get(url, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)"
        })
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Strip scripts/styles
        for tag in soup(["script", "style"]):
            tag.decompose()

        # Get text
        text = soup.get_text(separator="\n", strip=True)
        return text
    except ImportError:
        print("⚠️  BeautifulSoup not installed (pip install beautifulsoup4)")
        return None
    except Exception as e:
        print(f"⚠️  curl+BS4 failed: {e}")
        return None


def extract_content(url: str, source_type: str) -> str:
    """Fallback chain: playwright → blotato → curl → ask user."""
    print(f"Pulling {source_type} from {url}\n")

    # Try Playwright (best for SPAs)
    print("→ Trying Playwright...")
    content = try_playwright(url)
    if content:
        print(f"✅ Got {len(content)} chars from Playwright\n")
        return content

    # Try Blotato source (best for YouTube, Twitter, TikTok)
    if source_type in ("article", "youtube", "twitter", "tiktok", "pdf"):
        print("→ Trying Blotato source extraction...")
        content = try_blotato_source(url, source_type)
        if content:
            print(f"✅ Got {len(content)} chars from Blotato\n")
            return content

    # Try curl + BS4 (simple HTML)
    print("→ Trying curl + BeautifulSoup...")
    content = try_curl_bs4(url)
    if content:
        print(f"✅ Got {len(content)} chars from curl+BS4\n")
        return content

    # All failed
    print("❌ All extraction methods failed.")
    print("Please paste the content manually or provide an alternative URL.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Pull content from URL")
    parser.add_argument("--url", required=True, help="URL to extract from")
    parser.add_argument("--type", default="article",
                        choices=["article", "youtube", "twitter", "tiktok", "pdf",
                                 "perplexity-query", "audio"],
                        help="Source type")
    parser.add_argument("--query", help="Query for perplexity-query type")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--max-chars", type=int, default=20000,
                        help="Max chars to output (truncate longer)")

    args = parser.parse_args()

    if args.type == "perplexity-query" and not args.query:
        print("❌ --type perplexity-query requires --query", file=sys.stderr)
        sys.exit(1)

    url = args.url
    if args.type == "perplexity-query":
        url = args.query

    content = extract_content(url, args.type)

    # Truncate if needed
    if len(content) > args.max_chars:
        content = content[:args.max_chars] + f"\n\n[truncated from {len(content)} chars]"

    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w") as f:
            f.write(content)
        print(f"✅ Saved to {args.output}")
    else:
        print(content)


if __name__ == "__main__":
    main()