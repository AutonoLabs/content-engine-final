#!/usr/bin/env python3
"""
Pull engagement data from Blotato + update performance-log.md.

Usage:
    python scripts/performance_pull.py --brand allsquared --days 7
    python scripts/performance_pull.py --brand allsquared --post-url "https://..."
"""

import argparse
import os
import sys
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


def fetch_engagement(post_url: str, platform: str, blotato_key: str) -> dict:
    """Fetch engagement metrics from Blotato."""
    # Blotato provides analytics endpoints per platform
    # This is a wrapper — actual API may vary
    response = requests.get(
        "https://api.blotato.com/v1/analytics/post",
        headers={"Authorization": f"Bearer {blotato_key}"},
        params={"url": post_url, "platform": platform},
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def update_performance_log(brand: str, days: int):
    """Pull last N days of posts + engagement, update performance-log.md."""
    blotato_key = os.getenv("BLOTATO_API_KEY")
    if not blotato_key:
        print("❌ BLOTATO_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    # Fetch recent posts
    since = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
    response = requests.get(
        "https://api.blotato.com/v1/posts",
        headers={"Authorization": f"Bearer {blotato_key}"},
        params={"since": since, "limit": 100},
        timeout=30
    )
    response.raise_for_status()
    posts_data = response.json()
    if isinstance(posts_data, list):
        posts = posts_data
    elif isinstance(posts_data, dict):
        posts = posts_data.get("posts", [])
    else:
        posts = []

    if not posts:
        print(f"No posts found in last {days} days for brand '{brand}'")
        return

    # Filter by brand (assuming brand is in caption metadata or post metadata)
    # This depends on how you tag brand — placeholder logic
    print(f"Found {len(posts)} posts in last {days} days")

    log_path = f"brands/{brand}/performance-log.md"
    if not os.path.exists(log_path):
        print(f"❌ {log_path} doesn't exist. Create from brands/performance-log.template.md first.")
        sys.exit(1)

    # Read existing log
    with open(log_path) as f:
        log = f.read()

    # Append new entries
    new_entries = []
    for post in posts:
        if post.get("state", {}).get("type") != "published":
            continue

        post_url = post.get("publicUrl") or post.get("postUrl")
        if not post_url:
            continue

        engagement = fetch_engagement(post_url, post.get("platform"), blotato_key)

        entry = f"""
### {post.get('postTime', 'unknown')} — {post.get('platform')} — {post.get('text', '')[:50]}...

- **Post URL:** {post_url}
- **Post age:** {days} days
- **Impressions / reach:** {engagement.get('impressions', 'N/A')}
- **Likes / reactions:** {engagement.get('likes', 'N/A')}
- **Comments:** {engagement.get('comments', 'N/A')}
- **Shares / reposts:** {engagement.get('shares', 'N/A')}
- **Engagement rate:** {engagement.get('engagementRate', 'N/A')}
- **Notes:** [add observations]
"""
        new_entries.append(entry)

    # Append to log
    with open(log_path, "a") as f:
        f.write(f"\n## Pulled {datetime.utcnow().isoformat()}\n")
        for entry in new_entries:
            f.write(entry)

    print(f"✅ Updated {log_path} with {len(new_entries)} new entries")


def main():
    parser = argparse.ArgumentParser(description="Pull engagement + update performance log")
    parser.add_argument("--brand", required=True, help="Brand name")
    parser.add_argument("--days", type=int, default=7, help="Days to look back")
    parser.add_argument("--post-url", help="Pull single post instead")

    args = parser.parse_args()

    if args.post_url:
        # Single post mode
        blotato_key = os.getenv("BLOTATO_API_KEY")
        if not blotato_key:
            print("❌ BLOTATO_API_KEY not found", file=sys.stderr)
            sys.exit(1)
        engagement = fetch_engagement(args.post_url, "unknown", blotato_key)
        import json
        print(json.dumps(engagement, indent=2))
    else:
        # Bulk mode
        update_performance_log(args.brand, args.days)


if __name__ == "__main__":
    main()