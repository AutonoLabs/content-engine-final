# Troubleshooting

> Common issues + fixes. If something breaks, check here first.

---

## Blotato issues

### "Authentication Failed: Bad credentials"

**Cause:** BLOTATO_API_KEY is wrong or expired.

**Fix:**
1. Go to [blotato.com](https://blotato.com) → Settings → API
2. Verify key matches `.env`
3. Generate new key if expired
4. Restart scripts

---

### "Account not connected for platform X"

**Cause:** Platform account not OAuth'd in Blotato yet.

**Fix:**
1. Blotato → Connect Account → Platform
2. Complete OAuth flow
3. Verify account appears in `scripts/blotato_list_accounts.py` output

---

### "Post submission failed: missing required field"

**Cause:** Platform-specific required field missing.

**Fix:** Check platform docs in `docs/platform-hooks.md` for required fields per platform:
- **Facebook:** pageId required
- **LinkedIn:** pageId required for company pages
- **TikTok:** privacyLevel, disabledComments, disabledDuet, disabledStitch, isBrandedContent, isYourBrand, isAiGenerated required
- **Pinterest:** boardId required
- **YouTube:** title, privacyStatus, shouldNotifySubscribers required

---

### "Post scheduled but never published"

**Cause:** Schedule time in past, or Blotato downtime.

**Fix:**
1. Check post status via `scripts/blotato_get_post_status.py <submission-id>`
2. Reschedule with future timestamp
3. Contact Blotato support if persistent

---

## Higgsfield issues

### "Credit limit reached"

**Cause:** Used all 6000 credits for the month.

**Fix:**
1. Switch to manual-media mode for the rest of the month
2. Or upgrade plan
3. Or wait until next billing cycle

**Prevention:** Track credit usage in `brands/<brand>/inbox/credit-log.md`

---

### "Model not available: kling-3.0"

**Cause:** Model temporarily unavailable, or plan doesn't include it.

**Fix:**
1. Try alternative model: `scripts/higgsfield_generate.py --model veo-3.1`
2. Or check Higgsfield status page
3. Or downgrade to manual-media mode for this post

---

### "Unlimited mode blocked for automation"

**Cause:** Higgsfield ToS — automation workflows can't use unlimited features, must use credit mode.

**Fix:**
1. Verify `scripts/higgsfield_generate.py` uses `--credit-mode true`
2. Never route cron jobs through "unlimited" toggle
3. See `docs/ENV-WIRING.md` for ToS summary

---

## Claim verification issues

### "Post rejected: claim not verified"

**Cause:** Caption contains a stat/date/regulatory claim with no entry in `brands/<brand>/verified-facts.md`.

**Fix:**
1. Either:
   - Verify the claim now (find source, add to verified-facts.md)
   - Or rewrite caption without the claim
2. Re-submit for approval

---

### "Verified source URL returns 404"

**Cause:** Source moved or was removed.

**Fix:**
1. Re-verify claim against alternative source
2. Update entry in `verified-facts.md` with new source
3. Mark old source as expired

---

## Diversity rule conflicts

### "Cannot pick format: rotation blocked all options"

**Cause:** All formats used in last N posts.

**Fix:**
1. Override with explicit reason (e.g., "launch event")
2. Or expand content-type-taxonomy (add new format)
3. Or push post to next week

---

### "Theme already used in last 4 weeks"

**Cause:** Theme rotation rule.

**Fix:**
1. Pick a sub-angle that's distinct (theme can be loose)
2. Or wait 4 weeks
3. Or override with explicit reason

---

## Content-pull issues

### "Playwright failed: browser launch error"

**Cause:** Playwright browsers not installed.

**Fix:**
```bash
pip install playwright
playwright install chromium
```

---

### "Blotato source extraction timed out"

**Cause:** Source video >20 min, or server slow.

**Fix:**
1. Poll manually via Blotato dashboard or check `scripts/blotato_get_post_status.py` for the post submission.
2. Or fallback to curl + BeautifulSoup
3. Or skip content pull for this post

---

## Discord / approval issues

### "Founder not responding in Discord"

**Cause:** Founder unavailable.

**Fix:**
1. Wait 24 hours
2. Or escalate to backup approver (list in `brands/<brand>/README.md`)
3. Or proceed with "default approve" if pre-approved

---

### "Edit pass broke caption voice"

**Cause:** Founder edits sometimes dilute voice profile.

**Fix:**
1. Compare edit to original
2. Run voice-from-brief refinement to update profile
3. Ensure future generations don't drift

---

## Cron / scheduling issues

### "Cron job didn't fire"

**Cause:** Cron daemon not running, or schedule misconfigured.

**Fix:**
1. Check cron logs
2. Verify schedule syntax
3. Test manually: `python scripts/<script>.py`

---

### "Batch publish failed halfway"

**Cause:** One post failed, others queued.

**Fix:**
1. Check status of each submission ID
2. Manually re-publish failed ones
3. Update `content-mix.md` with actual status

---

## Performance tracking issues

### "Engagement data not pulling"

**Cause:** Platform API rate limit, or auth issue.

**Fix:**
1. Wait 1 hour
2. Use manual data entry fallback
3. Check Blotato API status

---

## General debugging

### "Logs are silent"

**Cause:** Log level too high.

**Fix:**
1. Set `LOG_LEVEL=DEBUG` in `.env`
2. Re-run script
3. Check `logs/` directory

---

### "Script imports broken after pip install"

**Cause:** Virtualenv not activated, or deps not installed.

**Fix:**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

---

## When to escalate

If issue persists after troubleshooting:
1. Check GitHub Issues for similar reports
2. Open new GitHub Issue with:
   - What you were doing
   - What you expected
   - What happened
   - Full error message + logs
   - Your OS + Python version
3. Maintainer responds within 48 hours

---

**Last updated:** 2026-07-08