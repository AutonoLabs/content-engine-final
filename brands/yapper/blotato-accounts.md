# Blotato Accounts — [Brand Name]

> Connected account IDs for each platform. Required to publish via `scripts/blotato_publish.py`.

---

## Accounts

| Platform | Account ID | Username | Display Name | Connected Date | Status |
|---|---|---|---|---|---|
| LinkedIn | `abc123` | @brand-handle | Brand Name | 2026-07-08 | ✅ active |
| X (Twitter) | `xyz789` | @brand_x | Brand on X | 2026-07-08 | ✅ active |
| Instagram | `55570` | @brand.ig | Brand IG | 2026-07-08 | ✅ active |
| TikTok | `tiktok-id` | @brand.tiktok | Brand TikTok | 2026-07-08 | ⏳ pending |
| YouTube | `41192` | BrandChannel | Brand YT | 2026-07-08 | ✅ active |
| Threads | `threads-id` | @brand.threads | Brand Threads | 2026-07-08 | ⏳ pending |
| Facebook | `fb-id` | Brand Page | Brand FB | 2026-07-08 | ✅ active |
| Pinterest | `pin-id` | BrandPins | Brand Pin | 2026-07-08 | ❌ not connected |
| Bluesky | `bsky-id` | brand.bsky | Brand Bsky | 2026-07-08 | ❌ not connected |

---

## Subaccounts

For platforms with page/subaccount hierarchy (Facebook Pages, LinkedIn Company Pages, YouTube Playlists):

| Platform | Type | ID | Name |
|---|---|---|---|
| Facebook | Page | `page-id-1` | Brand Page Name |
| LinkedIn | Company Page | `linkedin-page-id` | Brand LinkedIn |
| YouTube | Playlist | `playlist-id-1` | Brand Playlist 1 |
| YouTube | Playlist | `playlist-id-2` | Brand Playlist 2 |

---

## Connection instructions

For each platform not yet connected:

### TikTok

1. Login to Blotato dashboard
2. Settings → Connected Accounts → TikTok
3. Click "Connect"
4. OAuth flow with TikTok Business account
5. Verify connection in `scripts/blotato_list_accounts.py`

### Threads

1. Login to Blotato dashboard
2. Settings → Connected Accounts → Threads
3. OAuth with Threads account
4. Verify

### Pinterest

1. Login to Blotato
2. Connect Pinterest Business account
3. Run `scripts/blotato_list_pinterest_boards.py <account-id>` to get boardIds
4. Document boardIds in this file

---

## Testing connections

After connecting any account, test publish:

```bash
# Dry-run by checking account is reachable
python scripts/blotato_list_accounts.py --platform <platform>

# Test publish (use a throwaway draft)
python scripts/blotato_publish.py \
  --account-id <id> \
  --platform <platform> \
  --text "Test post — please ignore"
```

---

## Notes

- Account IDs are sensitive. Don't share this file publicly.
- If an account is disconnected, re-link and update ID.
- For multi-brand workspaces, prefix account IDs with brand name in Blotato dashboard.

---

**Last updated:** [YYYY-MM-DD]