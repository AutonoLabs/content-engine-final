# Weekly Batch Flow

> Full operational runbook. From "what theme this week" → "posts published + tracked." Repeat weekly.

---

## Time budget

- **Light week (4 posts, all ready media):** ~2 hours
- **Normal week (6-8 posts, mix of formats):** ~4-5 hours
- **Heavy week (10+ posts, multiple brands):** ~8 hours

---

## Step 1: Pick theme (10 min)

```bash
# Create new week folder
mkdir -p brands/<brand>/weeks/$(date +%Y-W%V)
```

Pick ONE theme for the week. Theme is a 1-sentence positioning:
- "Boring infrastructure that makes everything work" (AllSquared W28)
- "Small wins with chronic illness" (Yapper hypothetical)

Document in `brands/<brand>/weeks/<week>/THEME.md`:
```markdown
# Theme — W[##]

## Theme statement
[1 sentence]

## Why this theme
[2-3 sentences on resonance]

## Sub-angles (rotate across platforms)
1. [angle 1]
2. [angle 2]
3. [angle 3]
4. [angle 4]
```

---

## Step 2: Plan diversity (20 min)

Check `brands/<brand>/content-mix.md` for:
- Last week's formats → pick non-repeats
- Themes used in last 4 weeks → confirm no repeats
- Narrative styles used in last batch → pick a different rotation
- Hook patterns → at least 3 different this week
- Visual styles → confirm no 3-consecutive same
- Platforms covered → at least 3 active

Draft a plan table:

| Day | Platform | Format | Narrative | Hook | Visual | Segment |
|---|---|---|---|---|---|---|
| Mon | LinkedIn | text-only | Contrarian Frame | "Most companies get this wrong" | — | trades |
| Wed | IG | image-square | Personal Reckoning | "Three years ago" | portrait | agencies |
| Fri | TikTok | video-short | Specific Number | "The math on £50k" | cinematic | prop devs |
| Sun | X | thread | Observation | "Watch this pattern" | — | trades |

Save to `brands/<brand>/weeks/<week>/PLAN.md`.

---

## Step 3: Draft captions (60-90 min, 10-15 min each)

For each post:

1. **Open prompt file** — `prompts/<platform>.md`
2. **Voice profile** — `brands/<brand>/voice-profile.md`
3. **Hook from platform-hooks** — `docs/platform-hooks.md`
4. **Narrative style from narrative-styles** — `docs/narrative-styles.md`
5. **Draft caption** in `brands/<brand>/weeks/<week>/captions.md`

Each caption entry:
```markdown
### [platform] — [format] — [theme-angle]

**Hook:** [first-line hook pattern]
**Narrative style:** [style]
**Caption:**
[the full caption text]

**Media:** [link to file or media brief]
**Status:** draft
```

---

## Step 4: Claim verification (15 min, per post)

For each caption with a stat/date/regulatory claim:

1. Open `brands/<brand>/verified-facts.md`
2. Check if claim has an entry
3. If not, verify it now (search + source)
4. Add entry or reject post

Skip if caption has no claims.

---

## Step 5: Generate media briefs (30 min, per post)

For posts with media (not text-only):

1. Open `docs/media-brief.template.md`
2. Fill for each visual post
3. Save to `brands/<brand>/weeks/<week>/media-briefs.md`

For video briefs → use Higgsfield auto-gen:
```bash
python scripts/higgsfield_generate.py \
  --brand <brand> \
  --brief brands/<brand>/weeks/<week>/media-briefs.md \
  --model kling-3.0 \
  --output brands/<brand>/inbox/
```

For manual-media mode → skip auto-gen, drop file in `brands/<brand>/inbox/` after generating in Higgsfield UI.

---

## Step 6: Approval pass (30 min)

For each caption:
- Run `docs/publish-runbook.md` pre-flight
- Show to founder/owner (Discord reply, comment, or review session)
- Get approval OR get edits
- Save edits to `brands/<brand>/exemplars/edits/<date>.md`

---

## Step 7: Log to content-mix (5 min)

Before publish, log each post to `brands/<brand>/content-mix.md`:
```markdown
### [YYYY-MM-DD] — [platform] — [theme-angle]
- Format: [type]
- Theme: [tag]
- Narrative: [style]
- Hook: [pattern]
- Visual: [style]
- Audience: [segment]
- Caption file: [path]
- Media file: [path]
- Status: approved
```

---

## Step 8: Publish via Blotato (10 min, per post)

```bash
python scripts/blotato_publish.py \
  --brand <brand> \
  --platform linkedin \
  --caption "..." \
  --media-url "https://..." \
  --account-id <id>
```

Or use the MCP tool if running in Claude/Cursor:
- `blotato_create_post` with platform-specific params

---

## Step 9: Capture post URLs (5 min)

After each publish, get the post URL:
```bash
python scripts/blotato_get_post_status.py <submission-id>
```

Update `brands/<brand>/content-mix.md` with URL + change status to `published`.

---

## Step 10: Performance tracking (5 min initially, ongoing)

```bash
# Pull latest engagement data
python scripts/performance_pull.py --brand <brand> --days 7
```

Updates `brands/<brand>/performance-log.md`.

---

## Step 11: Compare to past (15 min) — pattern detection

**This is the learning loop.** Pull engagement data, then run the comparison engine to surface which themes/hooks/narrative styles/visual styles/audiences/audience segments actually won engagement.

```bash
python scripts/compare_performance.py --brand <brand>
```

Output includes:
- Overall summary (avg, best, worst, median)
- By-platform breakdown
- Top + bottom per field: theme, narrative_style, hook_pattern, visual_style
- **Actionable suggestions** ("lean into X, reduce Y")

**Use the output to inform next week's plan (Step 2).** Specifically:
- Drop bottom performers (themes that lose)
- Lean into top performers (themes that win)
- Check platform-specific winners (architectural wins on LinkedIn, documentary wins on TikTok)
- Don't over-rotate: diversity rules still apply — winners ≠ only theme

**Document patterns in `brands/<brand>/weeks/<week>/RETRO.md`** (see "Pattern observations" section).

Full engine docs: `docs/compare-performance.md`.

---

## End-of-week retrospective (20 min)

```markdown
# Week [##] Retro — [brand]

## What worked
- [post 1] — [why]
- [post 3] — [why]

## What didn't
- [post 5] — [why]

## Pattern observations
- [narrative style X] outperformed [style Y]
- [format X] got 2x engagement of [format Y]

## Adjustments for next week
- [adjustment 1]
- [adjustment 2]
```

Save to `brands/<brand>/weeks/<week>/RETRO.md`.

---

## Cross-references

- `ONBOARDING.md` — first-time setup
- `skills/brand-adapter.md` — new brand onboarding
- `docs/diversity-rules.md` — rotation enforcement
- `docs/compare-performance.md` — pattern detection from past posts
- `docs/publish-runbook.md` — pre-flight checklist
- `brands/content-mix.template.md` — diversity tracker

**Last updated:** 2026-07-08 (added Step 11: compare to past)