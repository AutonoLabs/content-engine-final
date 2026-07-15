# Performance Log Template — Per-Brand Analytics

> Per-post engagement data. Populate as analytics come in. Used for pattern detection: what gets engagement, what doesn't.
>
> **CANONICAL ENTRY FORMAT** (the only format `scripts/compare_performance.py` parses correctly):
> - Header: `### YYYY-MM-DD — platform — theme`
> - Field names: `Impressions / reach`, `Likes / reactions`, etc. are auto-canonicalized
> - Numbers: `5.6%`, `0.056`, `5.6` all parse to `0.056`; `1.2k` parses to `1200`
> - Engagement rate is the default comparison metric

---

## Brand snapshot

- **Brand:** [name]
- **Primary platforms:** [list]
- **Log start:** [YYYY-MM-DD]

---

## Entries

One block per post:

```markdown
### YYYY-MM-DD — platform — theme

- Post URL: [link]
- Post age: [N days]
- Impressions / reach: [N]
- Likes / reactions: [N]
- Comments: [N]
- Shares / reposts: [N]
- Saves (IG/LinkedIn): [N]
- Click-throughs (link posts): [N]
- Engagement rate: [%]
- Top comment theme: [summary]
- Notes: [what worked, what to refine]
```

---

## DELETE ME — worked entries

> **The block below is an example of fully-logged entries. Delete this entire section before using this template for your brand.**

### 2026-07-08 — LinkedIn — escrow-milestone

- Post URL: https://linkedin.com/posts/example-1
- Post age: 7 days
- Impressions / reach: 5000
- Likes / reactions: 250
- Comments: 18
- Shares / reposts: 12
- Saves (IG/LinkedIn): 8
- Click-throughs (link posts): 35
- Engagement rate: 5.6%
- Top comment theme: "What happens if the builder just stops showing up?"
- Notes: UK tradesperson register landed. The hook inversion worked.

### 2026-07-10 — x — team-intro

- Post URL: https://x.com/example/status/123
- Post age: 5 days
- Impressions / reach: 1200
- Likes / reactions: 8
- Comments: 1
- Shares / reposts: 0
- Engagement rate: 0.75%
- Top comment theme: (none)
- Notes: Question hook underperformed. Drop this combo.

### 2026-07-12 — Instagram — escrow-milestone

- Post URL: https://instagram.com/p/example
- Post age: 3 days
- Impressions / reach: 8000
- Likes / reactions: 400
- Comments: 32
- Shares / reposts: 22
- Saves (IG/LinkedIn): 22
- Engagement rate: 5.68%
- Top comment theme: "How does the snagging retention work?"
- Notes: Carousel format works. Trade visual landed.

> **End of worked example. Delete from `## DELETE ME` to the end before filling in for your brand.**

---

## Analytics pulled from where

- **LinkedIn:** Page admin → analytics (impressions, reactions, comments, shares, click-throughs)
- **Instagram:** Business account → insights (reach, likes, comments, saves, profile visits)
- **X:** Tweet analytics (impressions, engagements, retweets, likes, replies, profile clicks)
- **TikTok:** Video analytics (views, likes, comments, shares, follows)
- **YouTube:** Studio → analytics (views, watch time, likes, comments)
- **Threads:** Insights (views, likes, reposts, replies) — limited vs. others
- **Facebook:** Page insights (reach, reactions, comments, shares)

---

## Pattern detection (over time)

After enough data:

- Which narrative styles get the most engagement per platform?
- Which hook patterns get the most engagement per platform?
- Which visual styles get the most engagement per platform?
- Which audience segments respond most?
- Which themes get engagement vs. silence?
- Time-of-day patterns per platform?
- Day-of-week patterns per platform?

Run `python scripts/compare_performance.py --brand <name>` weekly to surface patterns automatically.

---

## Cross-references

- `brands/<brand>/content-mix.md` — diversity tracker
- `brands/<brand>/voice-profile.md` — voice layer
- `brands/<brand>/target-audience.md` — audience segments