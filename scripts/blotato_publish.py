#!/usr/bin/env python3
"""
Publish a post via Blotato.

Usage:
    python scripts/blotato_publish.py \
        --account-id <id> \
        --platform linkedin \
        --text "Caption here" \
        --media-url "https://..."

    # With platform-specific fields:
    python scripts/blotato_publish.py \
        --account-id <id> \
        --platform tiktok \
        --text "..." \
        --privacy-level PUBLIC_TO_EVERYONE \
        --is-ai-generated true

    # Schedule for later:
    python scripts/blotato_publish.py \
        --account-id <id> \
        --platform x \
        --text "..." \
        --schedule "2026-07-15T14:00:00Z"
"""

import argparse
import sys
from blotato_client import BlotatoClient


def main():
    parser = argparse.ArgumentParser(description="Publish via Blotato")
    parser.add_argument("--account-id", required=True, help="Blotato account ID")
    parser.add_argument("--platform", required=True,
                        choices=["twitter", "facebook", "instagram", "linkedin",
                                 "tiktok", "pinterest", "threads", "bluesky", "youtube"])
    parser.add_argument("--text", required=True, help="Post text")
    parser.add_argument("--media-url", action="append", help="Media URL (can repeat for carousels)")
    parser.add_argument("--schedule", help="ISO 8601 timestamp for scheduling")

    # Platform-specific optional fields
    parser.add_argument("--page-id", help="FB/LinkedIn page ID")
    parser.add_argument("--privacy-level", help="TikTok privacyLevel")
    parser.add_argument("--board-id", help="Pinterest boardId")
    parser.add_argument("--title", help="YouTube/Pinterest/TikTok title")
    parser.add_argument("--privacy-status", help="YouTube privacyStatus")
    parser.add_argument("--is-ai-generated", action="store_true", help="TikTok/YT flag")

    args = parser.parse_args()

    client = BlotatoClient()

    media_urls = args.media_url or []

    # Build platform-specific kwargs
    platform_kwargs = {}
    if args.page_id:
        platform_kwargs["pageId"] = args.page_id
    if args.privacy_level:
        platform_kwargs["privacyLevel"] = args.privacy_level
    if args.board_id:
        platform_kwargs["boardId"] = args.board_id
    if args.title:
        platform_kwargs["title"] = args.title
    if args.privacy_status:
        platform_kwargs["privacyStatus"] = args.privacy_status
    if args.is_ai_generated:
        platform_kwargs["isAiGenerated"] = True

    # TikTok requires many boolean flags
    if args.platform == "tiktok":
        platform_kwargs.setdefault("disabledComments", False)
        platform_kwargs.setdefault("disabledDuet", False)
        platform_kwargs.setdefault("disabledStitch", False)
        platform_kwargs.setdefault("isBrandedContent", False)
        platform_kwargs.setdefault("isYourBrand", False)

    # YouTube requires some fields
    if args.platform == "youtube":
        platform_kwargs.setdefault("shouldNotifySubscribers", True)

    try:
        if args.schedule:
            result = client.schedule_post(
                account_id=args.account_id,
                platform=args.platform,
                text=args.text,
                scheduled_time=args.schedule,
                media_urls=media_urls,
                **platform_kwargs
            )
            print(f"✅ Scheduled: {result.get('postSubmissionId', result)}")
        else:
            result = client.create_post(
                account_id=args.account_id,
                platform=args.platform,
                text=args.text,
                media_urls=media_urls,
                **platform_kwargs
            )
            submission_id = result.get("postSubmissionId", "unknown")
            print(f"✅ Published (submission: {submission_id})")
            print(f"   Check status: python scripts/blotato_get_post_status.py {submission_id}")
            return submission_id

    except Exception as e:
        print(f"❌ Failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()