# Content Mix Template — Per-Brand Tracker

> Running tracker of every post: date, platform, type, theme, narrative style, hook, visual style, audience segment, URL, status. Diversity enforcement lives here.
>
> **CANONICAL ENTRY FORMAT** (the only format `scripts/compare_performance.py` parses correctly):
> - Header: `### YYYY-MM-DD — platform — theme` (three-em-spaces em-dash separator; ## also accepted)
> - Dates: `YYYY-MM-DD` preferred; `01/07/2026`, `July 7, 2026` also accepted
> - Platform names: case-insensitive (`LinkedIn`, `linkedin`, `LI`, `IG` all work)
> - Fields: `- **Field:** value` OR `- Field: value` (both work)

---

## Brand snapshot

- **Brand:** [name]
- **Primary platforms:** [list, e.g., LinkedIn, X, Instagram]
- **Cadence:** [posts/week, e.g., 4]
- **Launch date:** [YYYY-MM-DD]

---

## Diversity rules (from docs/diversity-rules.md)

- No 2 consecutive posts same format
- Theme can't repeat within 4 weeks
- No 2 consecutive posts same narrative style
- At least 3 different hook patterns per week
- No 3 consecutive posts same visual style
- Each month hits at least 2 audience segments
- Each week hits at least 3 platforms

---

## Entries

Each post gets an entry like this:

```markdown
### YYYY-MM-DD — platform — theme

- Format: [image-square | video-short | text-only | pdf | carousel | thread]
- Theme: [theme tag]
- Narrative style: [from docs/narrative-styles.md]
- Hook pattern: [from docs/platform-hooks.md]
- Visual style: [documentary | cinematic | architectural | lifestyle | editorial | portrait | screen-recording]
- Audience segment: [sub-segment from target-audience.md]
- Caption file: [link]
- Media file: [link]
- Post URL: [link]
- Status: [draft | approved | published | archived]
- Engagement: [fill in when available]
- Notes: [what worked, what to refine]
```

---

## DELETE ME — worked entries

> **The block below is an example of fully-logged entries. Delete this entire section before using this template for your brand. The format above is the canonical entry format.**

### 2026-07-08 — LinkedIn — escrow-milestone

- Format: image-square
- Theme: escrow-milestone
- Narrative style: contrarian-frame
- Hook pattern: statement
- Visual style: architectural
- Audience segment: UK project owner
- Caption file: brands/allsquared/weeks/2026-W28/post-01.md
- Media file: brands/allsquared/inbox/allsquared-linkedin-01.png
- Post URL: https://linkedin.com/posts/example-1
- Status: published
- Engagement: impressions 5000, likes 250, comments 18, shares 12, rate 0.056
- Notes: Strong hook. UK tradesperson register landed. Test variation with retention angle next week.

### 2026-07-10 — x — team-intro

- Format: text-only
- Theme: team-intro
- Narrative style: observation
- Hook pattern: question
- Audience segment: UK agency
- Caption file: brands/allsquared/weeks/2026-W28/post-02.md
- Status: published
- Engagement: impressions 1200, likes 8, comments 1, shares 0, rate 0.0075
- Notes: Question hook underperformed. Drop this combo.

### 2026-07-12 — Instagram — escrow-milestone

- Format: carousel
- Theme: escrow-milestone
- Narrative style: specific-number
- Hook pattern: statement
- Visual style: lifestyle
- Audience segment: UK tradesperson
- Caption file: brands/allsquared/weeks/2026-W28/post-03.md
- Media file: brands/allsquared/inbox/allsquared-instagram-01.png
- Post URL: https://instagram.com/p/example
- Status: published
- Engagement: impressions 8000, likes 400, comments 32, saves 22, rate 0.0568
- Notes: Carousel format works. Trade visual landed. Statement hook confirmed winning on this theme.

> **End of worked example. Delete from `## DELETE ME` to the end before filling in for your brand.**

---

## Diversity check

(Manual or agent-calculated)

- Last 5 posts format rotation: [list]
- Theme cycle this month: [list]
- Narrative style rotation: [list]
- Hook pattern rotation: [list]
- Visual style rotation: [list]
- Platforms active this week: [list]
- Audience segments hit this month: [list]

---

## Themes by week

Track themes to enforce the 4-week rule:

```markdown
- W28: [theme-1]
- W29: [theme-2]
- W30: [theme-3]
```

---

## Cross-references

- `docs/diversity-rules.md` — full rotation rules
- `brands/<brand>/voice-profile.md` — voice layer
- `brands/<brand>/target-audience.md` — audience segments
- `brands/<brand>/performance-log.md` — engagement data