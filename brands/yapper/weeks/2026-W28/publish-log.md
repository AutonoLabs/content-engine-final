# Yapper Launch Day — 2026-07-10 Publish Log

## Scheduled posts (via Blotato backend API directly — MCP kept coercing strings→numbers)

| Platform | Submission ID | Time (ET) | Media | Caption | Notes |
|---|---|---|---|---|---|
| LinkedIn v1 | c73a54cb-6765-4d9e-a3fd-98562fb34477 | n/a (published) | NONE (text-only) | "Today we are launching Yapper." | **VIOLATES no-text-only rule** — published immediately. Delete manually. |
| Twitter/X | f8fee56a-24bc-48db-91d4-08b525597ce2 | n/a (published) | NONE (text-only) | Launch caption | **VIOLATES no-text-only rule** — published immediately. Delete manually. |
| LinkedIn v2 | 654b4f83-4144-465e-9e7c-63dea4b94528 | Today 3:00 PM ET | wingback chair + lavender walls + mint mug + cream rotary | Launch manifesto caption | Public URL: https://database.blotato.io/storage/v1/object/public/public_media/42c0980a-3ba1-4276-a25c-10e7135c3a72/16596f70-79e9-4099-af22-6b8db7cac94b.jpg |
| Instagram Reel | a1a6bfb2-b6e1-4c04-86d1-20835d79fbe7 | Today 3:30 PM ET | 8s reel: senior woman in mint cardigan inside ink-plum phone booth, holding cream rotary; ending has 12 lavender dial dots + mint accent dot (NO wordmark yet) | "Every resident deserves a daily check-in." | Public URL: https://database.blotato.io/storage/v1/object/public/public_media/42c0980a-3ba1-4276-a25c-10e7135c3a72/2661b720-961b-4f68-9ecf-fa9d83202741.mp4 |

## Issues encountered

1. **`mcp__blotato__blotato_create_post` rejecting strings as `accountId`/`pageId`** — the MCP server kept coercing our string args to numbers, returning `-32602 Invalid arguments`. Fix: bypass MCP and call `https://backend.blotato.com/v2/posts` directly with curl. New envelope schema:
   ```json
   {"post": {"accountId": "26225", "target": {"targetType": "linkedin", "pageId": "107116534"}, "content": {"platform": "linkedin", "text": "...", "mediaUrls": ["..."]}, "scheduledTime": "2026-07-10T15:00:00-04:00"}}
   ```
2. **`scheduledTime` ignored on first attempt** — when scheduledTime is in the past or too close to now, Blotato publishes immediately. LinkedIn v1 and X both published instantly before we noticed. Always verify with `blotato_get_post_status` after creating.
3. **Reel ending card missing Yapper wordmark** — the dial dots + mint accent dot render correctly but no "yapper.care" or "Yapper" text. Awaiting Rafael re-render with wordmark.
4. **TikTok not connected in Blotato** — accountId empty array for platform=tiktok.

## Verified launch facts (per `verified-facts.md`)

- "Loneliness is a public health crisis" — Surgeon General (Murthy, 2023) ✅
- "Compared to smoking 15 cigarettes a day" — Holt-Lunstad et al. (2010/2015 meta-analyses on social isolation) ✅
- "Happier Residents. Smarter care." — brand tagline ✅
- "yapper.care is NOT a medical device" — load-bearing disclaimer ✅

## Where to find these posts after publish

- LinkedIn v2: https://www.linkedin.com/feed/update/... (URL returned by `blotato_get_post_status`)
- Instagram Reel: TBD

