# Yapper Launch Day — 2026-07-10 Publish Log

## Publish attempts

| Platform | Time (ET) | Media | Caption | Notes |
|---|---|---|---|---|
| LinkedIn v1 | n/a (published) | NONE (text-only) | "Today we are launching Yapper." | **VIOLATES no-text-only rule** — published immediately; manual deletion required. |
| Twitter/X | n/a (published) | NONE (text-only) | Launch caption | **VIOLATES no-text-only rule** — published immediately; manual deletion required. |
| LinkedIn v2 | 3:00 PM | wingback chair + lavender walls + mint mug + cream rotary | Launch manifesto caption | Media-backed retry. |
| Instagram Reel | 3:30 PM | 8s reel: older woman in mint cardigan inside ink-plum phone booth, holding cream rotary | "Every resident deserves a daily check-in." | Ending had dial dots but no wordmark; replacement required before reuse. |

## Issues encountered

1. **`mcp__blotato__blotato_create_post` rejecting strings as `accountId`/`pageId`** — the MCP server kept coercing our string args to numbers, returning `-32602 Invalid arguments`. Fix: bypass MCP and call `https://backend.blotato.com/v2/posts` directly with curl. New envelope schema:
   ```json
   {"post": {"accountId": "LINKEDIN_ACCOUNT_ID", "target": {"targetType": "linkedin", "pageId": "YAPPER_PAGE_ID"}, "content": {"platform": "linkedin", "text": "...", "mediaUrls": ["PUBLIC_MEDIA_URL"]}, "scheduledTime": "FUTURE_ISO_8601_TIME"}}
   ```
2. **`scheduledTime` ignored on first attempt** — when scheduledTime is in the past or too close to now, Blotato publishes immediately. LinkedIn v1 and X both published instantly before we noticed. Always verify with `blotato_get_post_status` after creating.
3. **Reel ending card missing Yapper wordmark** — the dial dots + mint accent dot render correctly but no "yapper.care" or "Yapper" text. Awaiting Rafael re-render with wordmark.
4. **TikTok not connected in Blotato** — accountId empty array for platform=tiktok.

## Verified launch facts (per `verified-facts.md`)

- "Loneliness is a public health crisis" — Surgeon General (Murthy, 2023) ✅
- "Compared to smoking 15 cigarettes a day" — Holt-Lunstad et al. (2010/2015 meta-analyses on social isolation) ✅
- "Happier Residents. Smarter care." — brand tagline ✅
- "yapper.care is NOT a medical device" — load-bearing disclaimer ✅

## Publication follow-up

Record final public URLs only after platform publication is confirmed. Do not store signed upload URLs or internal submission identifiers here.

