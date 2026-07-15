# Performance Log — AllSquared (worked example)

> Real-shape entries for `scripts/compare_performance.py`. Use as format reference.

---

## Brand snapshot

- Brand: allsquared
- Primary platforms: LinkedIn, X, Instagram, TikTok, YouTube Shorts
- Log start: 2026-07-01

---

## Entries

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

### 2026-07-14 — TikTok — milestone-dispute

- Post URL: https://tiktok.com/@allsquared/video/example
- Post age: 1 day
- Impressions / reach: 15k
- Likes / reactions: 850
- Comments: 45
- Shares / reposts: 38
- Engagement rate: 6.22%
- Top comment theme: "Wish this existed for my extension last year"
- Notes: Documentary style + statement hook on TikTok outperformed LinkedIn.

### 2026-07-15 — LinkedIn — team-intro

- Post URL: https://linkedin.com/posts/example-5
- Post age: 0 days (just published)
- Impressions / reach: 3000
- Likes / reactions: 22
- Comments: 2
- Shares / reposts: 1
- Engagement rate: 0.83%
- Top comment theme: (none)
- Notes: Personal-reckoning didn't rescue the team-intro theme. Confirms theme is the problem.

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

Run `python scripts/compare_performance.py --brand allsquared` weekly to surface patterns automatically.

---

## Cross-references

- `brands/allsquared/content-mix.md` — diversity tracker
- `brands/allsquared/voice-profile.md` — voice layer
- `brands/allsquared/target-audience.md` — audience segments