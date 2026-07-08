# Content Engine — Final

> Multi-business content engine for Autono Labs portfolio. Anti-AI-feel by default, hooks-first for scroll-stopping, voice-tuned per brand, content-mix-tracked, AI-tell monitor keeps it current. Multi-format: video, image, text-only, PDF, presentation, review, and more.

---

## What's in this repo

### Architecture (universal — works for any new business)

- **`docs/`** — 9 architecture docs
  - `platform-hooks.md` — 5-7 hook patterns per platform, mobile-first
  - `visual-hooks.md` — image design rules per platform
  - `audience-demographics.md` — ages/gender/intent per platform
  - `narrative-styles.md` — 8 storytelling formats to rotate through
  - `anti-ai-feel.md` — banned words, banned structures, verified-facts gate
  - `content-pull.md` — scraper fallback chain
  - `publish-runbook.md` — pre-publish checklist
  - `content-type-taxonomy.md` — 16 content types + rotation
  - `diversity-rules.md` — no 2 consecutive same format, etc.

- **`prompts/`** — 6 platform prompts (linkedin, x, instagram, tiktok, youtube-shorts, threads)

- **`skills/`** — ongoing system health
  - `voice-from-brief.md` — given brand brief, generate voice profile (no seed posts required)
  - `ai-tell-monitor.md` — quarterly refresh of AI writing tells
  - `claim-verifier.md` — sector-aware claim verification
  - `brand-adapter.md` — onboard any new business in <2 weeks

- **`brands/`** — per-brand folders, templates only (Yapper, AllSquared, TreeAI, etc.)
  - `voice-profile.template.md`
  - `target-audience.template.md`
  - `verified-facts.template.md`

- **`.env.example`** — keys + budget notes

### Reference example (AllSquared)

- **`examples/allsquared/`** — anonymized reference for how a running brand looks. Includes voice profile, target audience, first batch of W28 captions, media briefs, content mix, performance log. NOT for clone — for understanding the structure.

---

## Onboarding a new brand

1. Create `brands/<brand-name>/` folder
2. Fill in `voice-profile.md` (use `skills/voice-from-brief.md`)
3. Fill in `target-audience.md` (use `brands/target-audience.template.md` + `docs/audience-demographics.md`)
4. Fill in `verified-facts.md` (use `skills/claim-verifier.md`)
5. Set up Blotato accounts for the brand
6. Generate first batch: pick theme, rotate narrative style, hit hooks per platform
7. Log to `content-mix.md` before publish
8. Log to `performance-log.md` after analytics collected
9. Edit pass loop: every edit feeds `voice-from-brief.md` for self-refinement

Time target: <2 weeks from brief to first published post.

---

## Key design decisions

- **Anti-AI-feel is the default.** 11 banned words, 10 banned structures, rhythm rules, specificity rule, banned intensifiers. Quarterly refreshed.
- **Hooks before content.** Platform-hooks.md sets the scroll-stopping bar per platform. Visual hooks handle non-text platforms.
- **Verified facts are gated.** No stat in any post unless sourced + dated in `verified-facts.md`.
- **Narrative rotation is enforced.** 8 styles, no 2 consecutive of the same. Tracks in `content-mix.md`.
- **Format rotation is enforced.** 16 content types, no 2 consecutive same format. Tracks in `content-mix.md`.
- **Voice can be brief-only.** Don't need seed posts. Voice-from-brief skill generates from brand theme + product + tone notes.
- **Multi-tenant, multi-brain.** Same repo can serve multiple businesses, multiple teams (autonio for portfolio, yapper for health, etc.). Each team owns their brand folder.

---

## Status

Built 2026-07-08. Currently staged for first push. To be expanded with first Yapper brand content (pending brand brief + voice notes from eli).

---

## License

Private. Autono Labs internal.