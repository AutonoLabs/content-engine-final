# Publish Runbook

> Pre-publish checklist. Run this before every post goes live. Updated 2026-07-07 (added account-id verification, post-publish verification).

---

## Pre-publish checklist

For every post, verify:

### 1. Account verification
- [ ] Run `mcp_blotato_blotato_list_accounts` for the target platform
- [ ] Confirm accountId matches the brand + platform
- [ ] For linkedin company pages: confirm pageId is the right subaccount

### 2. Caption verification
- [ ] Caption passes anti-AI-feel rules (no banned words, no banned structures)
- [ ] First line is a hook from `docs/platform-hooks.md`
- [ ] Caption uses 1-2 narrative styles from `docs/narrative-styles.md`
- [ ] All stats are in `brands/<brand>/verified-facts.md`
- [ ] Length is within platform target (see anti-ai-feel.md length table)
- [ ] No fabrication (no made-up numbers, dates, customer counts)

### 3. Media verification
- [ ] File exists in `~/clawd/agents/autonio/inbox/media/week-<YYYY>-<W##>/`
- [ ] File uploaded to blotato storage (public URL confirmed)
- [ ] Visual hook lands in 0.5s on mobile
- [ ] No logos, no real faces, no text artifacts
- [ ] Aspect ratio correct for platform
- [ ] Image quality sufficient (not pixelated, not overly compressed)

### 4. Brand verification
- [ ] Voice profile alignment (does it sound like the brand's voice?)
- [ ] Tone consistent with platform (linkedin ≠ x ≠ tiktok)
- [ ] No off-brand claims (regulatory, legal, financial accuracy)
- [ ] No competitor mentions (unless deliberate comparison)

### 5. Timing verification
- [ ] Schedule time is within platform optimal windows (see below)

---

## Platform optimal posting times (UK audience)

| Platform | Best days | Best times (UK) |
|---|---|---|
| LinkedIn | Tue-Thu | 8-10am |
| X | Tue-Thu | 8-10am, 5-7pm |
| Instagram | Tue, Wed, Thu | 11am-1pm, 7-9pm |
| TikTok | Tue-Thu, Sun | 7-9am, 7-11pm |
| YouTube Shorts | Fri-Sun | 12-3pm, 7-10pm |
| Threads | Wed-Fri | 8-10am, 12-2pm |

Note: these are starting points. Track performance over time and adjust per brand.

---

## Account-id reference (autonobrain blotato, July 2026)

**LinkedIn (accountId 26225, Eli Bernstein personal):**
- 134824069 → AllSquared (company page)
- 105050825 → Autono Labs (company page)
- 106714782 → Moto Legal
- 107116534 → Yapper
- Other subaccounts available

**X / Twitter:**
- 20913 → capitELIst (eli personal)
- 55618 → YapperCare

**Instagram:**
- 55570 → yapper.care (only IG account, no AllSquared)

**YouTube:**
- 41192 → Yapper (only YT account, no AllSquared)

**Facebook:**
- Personal + 2 pages (not yet used)

**Threads:** Not connected. Need OAuth setup.

---

## Post-publish verification

After blotato returns success:

1. **Public URL returned:** Verify the URL is live
2. **Spot-check the post:** Open in incognito, check the caption + image render correctly
3. **Log to memory:** Insert into `~/.hermes/profiles/autonio/data/content-engine/memory.db`:
   - post_id, brand, platform, caption, media_url, scheduled_time, status
4. **Note any edits:** If the user edits after publish, save the edit to exemplars

---

## Common errors + fixes

### "Blotato API error. Try again in a moment."
- Usually transient. Wait 30s, retry once.
- If persistent, check accountId with `list_accounts`.

### "Maximum request body size exceeded" (vision_analyze)
- Image too large for vision model. Resize with `sips -Z 600` to under 1MB, retry.

### "Permission denied" on file move
- Check directory exists: `ls ~/clawd/agents/autonio/inbox/media/week-<YYYY>-<W##>/`
- Create if missing: `mkdir -p`

### LinkedIn post rejected
- Verify pageId (subaccount id) is correct
- Check image isn't too large (linkedin limit: 5MB)

### YouTube post rejected
- Verify title is provided
- Verify privacyStatus is valid (public/private/unlisted)
- Check video duration is within YT limits (Shorts: under 60s)

---

## When to abort a publish

- Caption has a fabricated stat (not in verified-facts.md)
- Image has a logo or real person's face
- Caption is over the platform max length
- Account doesn't match the brand
- User has not approved the post

**Never auto-publish without explicit user approval.**