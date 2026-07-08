# Diversity Rules — Rotation Enforcement

> Hard rules to prevent content sameness. No two consecutive posts same format / same theme / same narrative style / same hook. Tracked in `content-mix.md`.

---

## Why this doc exists

Sameness is the silent killer of social accounts. Three failure modes:

1. **Format sameness:** all videos, or all images. Audience gets bored. Algorithm deprioritizes.
2. **Theme sameness:** same topic each week, different angles. Audience tunes out.
3. **Voice sameness:** same opening, same structure, same closing. AI feel maxes out.
4. **Hook sameness:** same first-line pattern every post. Algorithm learns, demotes.

Fix: explicit rotation rules, enforced by the agent, tracked in `content-mix.md`.

---

## Hard rules

These apply unless explicitly overridden by the user:

### Rule 1: Format rotation
**No 2 consecutive posts use the same content type.**

Examples:
- Post 1: TikTok short video
- Post 2: LinkedIn text-only ✓ (different type)
- Post 3: IG carousel ✓ (different type from Post 2)
- Post 4: X thread ✓ (different type)
- Post 5: YouTube short ✓ (different type from Post 4)

If format TBD (e.g., media is generated later), the format is locked when media is planned. Caption-only posts count as format too (text-only).

### Rule 2: Theme rotation
**A theme cannot repeat within 4 weeks.**

Themes are tracked in `content-mix.md`. Each entry has a theme tag. If a theme was used in W27, it can't be used in W28, W29, W30, or W31.

Themes can be referenced loosely (e.g., "boring plumbing that makes everything work" can re-emerge as "infrastructure over flash" — that's a new theme, not a repeat).

### Rule 3: Narrative-style rotation
**No 2 consecutive posts use the same narrative style.**

See `docs/narrative-styles.md` for the 8 styles. Rotation means across the post sequence, no repeats. After using "Contrarian Frame" on Post 1, Post 2 must be a different style.

### Rule 4: Hook-pattern rotation
**At least 3 different hook patterns per week.**

See `docs/platform-hooks.md`. Even within the same platform, vary the hook. Don't lead every LinkedIn post with "Hot take:". Don't open every IG caption with "POV:".

### Rule 5: Visual-style rotation
**No 3 consecutive posts in the same visual style across the brand.**

Visual styles include:
- Documentary / behind-the-scenes
- Cinematic / moody
- Architectural / geometric
- Lifestyle / aspirational
- Editorial / minimalist
- Portrait / face-forward
- Screen-recording / process

If 3 in a row used documentary, switch it up.

### Rule 6: Audience-segment coverage
**Each month must hit at least 2 distinct audience segments within the brand's target.**

If a brand's primary audience is "UK trades 30-55," they should see content aimed at different sub-segments (e.g., builders doing £50k+ projects, project owners commissioning kitchens, agency owners doing milestones). Don't optimize for just one sub-segment.

### Rule 7: Platform coverage (multi-platform brands)
**Each week must hit at least 3 distinct platforms.**

If your content mix targets LinkedIn + X + IG, all three need at least one post that week. Don't let one platform lag.

---

## Soft rules (defaults, overrideable)

- **2-3 posts/week** minimum cadence (adjustable per brand)
- **No more than 1 PDF/long-form per week** (longer format, lower frequency)
- **No more than 1 review/comparison per 2 weeks** (engagement-format fatigue)
- **Engagement hours:** stagger across platforms (don't blast everything at 9am)

---

## How the agent enforces

When generating a batch:

1. Pull recent entries from `content-mix.md`
2. Identify the latest format / theme / style / hook / visual used
3. Filter rotation options to non-repeats (per rules above)
4. Pick from filtered options
5. Document choice in `content-mix.md` BEFORE publish
6. After publish, update with platform-specific URL + analytics

---

## Tracking format

`content-mix.md` entry per post:

```markdown
## [YYYY-MM-DD] [platform] — [brief theme]

- **Format:** [from content-type-taxonomy.md]
- **Theme:** [theme tag]
- **Narrative style:** [from narrative-styles.md]
- **Hook pattern:** [from platform-hooks.md]
- **Visual style:** [from visual styles list]
- **Audience segment:** [sub-segment of target audience]
- **Caption URL:** [link to caption file]
- **Media URL:** [link to media file]
- **Post URL:** [link to published post]
- **Status:** [draft / approved / published / archived]
- **Engagement (when available):** [impressions, likes, comments, shares, rate]
- **Notes:** [what worked, what to refine]
```

---

## Edge cases

- **Re-posts / re-shares:** if a post did exceptionally well, reposting to a different platform is allowed (counts as a new post for diversity tracking, but theme override-flag).
- **Trendy / reactive content:** breaking news or viral moment posts may skip rotation. Document exception in `content-mix.md` with reason.
- **Launch / event:** scheduled launches may concentrate posts on one theme. That's allowed (override flag).
- **New brand onboarding:** first batch often has theme coherence by design. That's allowed.

---

## Cross-references

- `docs/content-type-taxonomy.md` — 16 formats
- `docs/narrative-styles.md` — 8 narrative styles
- `docs/platform-hooks.md` — hooks per platform
- `brands/<brand>/content-mix.md` — per-brand tracker