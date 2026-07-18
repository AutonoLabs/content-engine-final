# Compare Performance — Engine Documentation

> How `scripts/compare_performance.py` works, what it surfaces, and how to use it to refine the next batch.

---

## Why this exists

Two existing layers cover what the engine doesn't:

1. **`docs/diversity-rules.md`** — rotation enforcement (don't repeat formats/themes/hooks).
2. **`brands/<brand>/content-mix.md`** — tracker of which posts used which theme/hook/visual style.

But **rotation alone doesn't tell you what's *winning***. You can rotate formats perfectly and still publish formats/themes/hooks/visuals that don't engage.

This engine **correlates** the metadata in `content-mix.md` with engagement in `performance-log.md` to surface which patterns actually win. Then the next batch plan uses those winners.

---

## How it works

```
content-mix.md                performance-log.md
┌─────────────────────┐        ┌─────────────────────┐
│ YYYY-MM-DD          │        │ YYYY-MM-DD          │
│ Platform            │  ───►  │ Platform            │
│ Theme               │  join  │ Impressions         │
│ Narrative style     │  on    │ Likes               │
│ Hook pattern        │  date+ │ Comments            │
│ Visual style        │  plat- │ Shares              │
│ Audience segment    │  form  │ Engagement rate     │
│ Format              │        │ Saves               │
└─────────────────────┘        └─────────────────────┘

                          │
                          ▼

            compare_performance.py
            │
            ├─ Group by field (theme, narrative_style, ...)
            ├─ Aggregate metric (avg engagement_rate)
            ├─ Sort + rank
            └─ Surface: TOP winners, BOTTOM losers, actionable suggestions
```

**The script:**
1. Parses `content-mix.md` into per-post dicts (date, platform, theme, narrative style, hook, visual, audience, format).
2. Parses `performance-log.md` into `(date, platform) → engagement dict`.
3. Correlates via `(date, platform)` join.
4. Aggregates by any field, computing avg/min/max for the chosen metric.
5. Surfaces top + bottom performers.
6. Outputs actionable suggestions: "lean into X, reduce Y."

---

## Usage

### Basic — see top/bottom per field

```bash
python scripts/compare_performance.py --brand allsquared
```

Outputs:
- Overall summary (avg, best, worst, median of chosen metric)
- By-platform breakdown
- Top + bottom 5 per field: theme, narrative_style, hook_pattern, visual_style
- Actionable suggestions ("lean into X, reduce Y")

### Specific metric

```bash
python scripts/compare_performance.py --brand allsquared --metric likes
python scripts/compare_performance.py --brand allsquared --metric shares
python scripts/compare_performance.py --brand allsquared --metric engagement_rate
```

### Specific field

```bash
python scripts/compare_performance.py --brand allsquared --by theme --top 10
python scripts/compare_performance.py --brand allsquared --by visual_style
```

Multiple fields:

```bash
python scripts/compare_performance.py --brand allsquared --by theme --by hook_pattern
```

### JSON output (for dashboards / automation)

```bash
python scripts/compare_performance.py --brand allsquared --json > perf-$(date +%Y-%m-%d).json
```

---

## When to run it

| Cadence | Why |
|---|---|
| **Weekly** (after pulling performance data) | Decide next week's theme/hook mix based on what won |
| **Monthly** | Bigger pattern detection — what audience segments respond, what narrative styles compound |
| **Quarterly** | Strategic review — is the brand drifting toward a winning format niche? |

---

## Required data

**For the engine to surface patterns, you need:**

1. **`content-mix.md` populated** with every post's metadata (theme, narrative_style, hook_pattern, visual_style, audience_segment, format).

2. **`performance-log.md` populated** with engagement data for those posts.

**To populate performance-log.md:**

- **Manual:** pull analytics from each platform, paste in the entry format.
- **Automated:** `python scripts/performance_pull.py --brand <brand> --days 30`

**To populate content-mix.md:**

- After every batch, log each post's metadata. Use the entry template in `brands/content-mix.template.md`.

---

## Field definitions

| Field | Source | What it captures |
|---|---|---|
| `theme` | You tag it | The post's topic / angle. Track themes to enforce 4-week rotation. |
| `narrative_style` | `docs/narrative-styles.md` | One of 8 storytelling formats (Contrarian Frame, Hero's Journey, etc.) |
| `hook_pattern` | `docs/platform-hooks.md` | The opening-line pattern (question, statement, observation, etc.) |
| `visual_style` | `docs/visual-hooks.md` | Documentary / cinematic / architectural / lifestyle / editorial / portrait / screen-recording |
| `audience_segment` | `brands/<brand>/target-audience.md` | Sub-segment of target audience (e.g., "UK project owners £20-50k") |
| `format` | `docs/content-type-taxonomy.md` | Image-square, video-short, text-only, carousel, thread, PDF, etc. |

**The cleaner the tagging, the better the patterns surface.** Use consistent theme names (don't tag one post "escrow milestone" and another "milestone-based escrow" — pick one).

---

## What to do with the output

### Scenario 1: Theme X wins consistently, Theme Y loses

```
TOP:    "escrow-milestone" avg 0.087 (n=4)
BOTTOM: "team-intro" avg 0.012 (n=2)
```

→ **Action:** Plan next month's batch around escrow-milestone. Drop team-intro unless strategically required.

### Scenario 2: Visual style C wins on LinkedIn but loses on TikTok

```
LinkedIn:  "architectural" avg 0.092 (n=3)
TikTok:    "architectural" avg 0.018 (n=2)
```

→ **Action:** Use architectural on LinkedIn. Switch TikTok to "documentary" or "lifestyle" — the platform-specific audience wants motion-driven content.

### Scenario 3: Hook pattern W wins, Hook pattern V wins on a different platform

```
X: "question-hook" wins
LinkedIn: "statement-hook" wins
```

→ **Action:** Don't generalize "question wins" — the engine reveals platform-specific truth.

### Scenario 4: All themes perform similarly

→ **Action:** You don't have enough data yet (small N). Keep posting, keep tracking. Re-run in a month.

---

## Pitfalls

1. **Don't over-rotate to one winner.** Diversity rules still apply. Winning theme ≠ only theme.
2. **Small N = noise.** A theme with n=1 isn't a winner; it's an anecdote. Look for n≥3 before declaring patterns.
3. **Engagement rate ≠ impact.** A low-engagement post might be the one that converted a key customer. Track business outcomes separately.
4. **Audience segments compound.** A hook that wins with "UK project owners £20-50k" might lose with "agencies." Look at segment-level data, not just overall.
5. **Date matters.** A post from Q1 vs Q4 might perform differently due to seasonality. The engine doesn't auto-detect this — flag it manually.

---

## Integration with weekly batch flow

**Updated `docs/WEEKLY-BATCH-FLOW.md` flow:**

1. **Monday:** Pull performance data (`performance_pull.py`) → updates `performance-log.md`.
2. **Monday:** Run `compare_performance.py` → identifies winning patterns.
3. **Tuesday:** Plan next week's batch using diversity rules + winning patterns.
4. **Wed-Thu:** Draft captions, generate media.
5. **Friday:** Validate + publish.
6. **Repeat.**

---

## Examples

See `brands/allsquared/weeks/2026-W29/` for a worked example (with captions + media-briefs). Run:

```bash
python scripts/compare_performance.py --brand allsquared
```

Once `performance-log.md` is populated for that brand.

---

**Last updated:** 2026-07-08
**Maintainer:** Autono Labs