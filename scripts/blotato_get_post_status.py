#!/usr/bin/env python3
"""
Check status of a Blotato post submission.

Usage:
    python scripts/blotato_get_post_status.py <submission_id>
"""

import sys
import json
from blotato_client import BlotatoClient


def main():
    if len(sys.argv) < 2:
        print("Usage: blotato_get_post_status.py <submission_id>")
        sys.exit(1)

    submission_id = sys.argv[1]
    client = BlotatoClient()

    try:
        result = client.get_post_status(submission_id)
        print(json.dumps(result, indent=2))

        status = result.get("status", "unknown")
        if status == "published":
            url = result.get("publicUrl") or result.get("postUrl")
            if url:
                print(f"\n✅ Live: {url}")
        elif status == "scheduled":
            print(f"\n📅 Scheduled for: {result.get('scheduledTime')}")
        elif status == "failed":
            print(f"\n❌ Failed: {result.get('errorMessage', 'unknown error')}")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()