#!/usr/bin/env python3
"""
List all Blotato accounts with IDs + platform-specific required fields.

Usage:
    python scripts/blotato_list_accounts.py
    python scripts/blotato_list_accounts.py --platform instagram
    python scripts/blotato_list_accounts.py --json
"""

import argparse
import json
import sys
from blotato_client import BlotatoClient


PLATFORM_REQUIRED_FIELDS = {
    "twitter": [],
    "bluesky": [],
    "threads": [],
    "facebook": ["pageId (from subaccounts)"],
    "linkedin": ["pageId (for company pages, optional for personal)"],
    "instagram": [],
    "tiktok": ["privacyLevel", "disabledComments", "disabledDuet", "disabledStitch",
               "isBrandedContent", "isYourBrand", "isAiGenerated"],
    "pinterest": ["boardId"],
    "youtube": ["title", "privacyStatus", "shouldNotifySubscribers"]
}


def main():
    parser = argparse.ArgumentParser(description="List Blotato accounts")
    parser.add_argument("--platform", help="Filter by platform")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    client = BlotatoClient()
    accounts = client.list_accounts(platform=args.platform)

    if args.json:
        print(json.dumps(accounts, indent=2))
        return

    if not accounts:
        print("No accounts found.")
        sys.exit(1)

    print(f"\n=== {len(accounts)} account(s) ===\n")
    for acc in accounts:
        platform = acc.get("platform", "unknown")
        print(f"Platform: {platform}")
        print(f"  ID: {acc.get('id')}")
        print(f"  Display name: {acc.get('displayName', 'N/A')}")
        print(f"  Username: @{acc.get('username', 'N/A')}")

        if acc.get("subaccounts"):
            print(f"  Subaccounts:")
            for sub in acc["subaccounts"]:
                print(f"    - {sub.get('name')}: {sub.get('id')}")

        required = PLATFORM_REQUIRED_FIELDS.get(platform, [])
        if required:
            print(f"  Required fields for posting:")
            for field in required:
                print(f"    - {field}")

        print()


if __name__ == "__main__":
    main()