---
name: brand-adapter
description: Onboard any new business to the content engine in <2 weeks. Combines voice-from-brief, ai-tell-monitor, claim-verifier, plus platform-demographics and content-mix-tuning. Output: a fully operational brand folder ready to publish.
---

# Brand Adapter

> Master onboarding pipeline. Combines voice-from-brief + ai-tell-monitor + claim-verifier + platform-demographics + content-mix-tuning into a single <2-week workflow. Takes a new business from "empty hands" to "first published post."

---

## Why this skill exists

New businesses join the portfolio constantly. They each need:
- Voice profile
- Target-audience override
- Verified-facts gate
- Content mix weights (which platforms, which formats, which cadence)
- Blotato account wiring
- First test batch
- Edit-pass loop

Doing these in series across multiple skills/tools was fragile. This skill is the **orchestrator**: input is a brand brief, output is a fully operational brand folder.

---

## When to use this skill

- New business joins the portfolio (e.g., Yapper, AllSquared, TreeAI, Politicall, etc.)
- Existing business restructures (pivot, rebrand, sector change)
- Quarterly — to ensure brand folders stay current as the engine evolves

---

## Input schema

```yaml
brand_name: "Yapper"
sector: "consumer_health"  # consumer_health | fintech | legal | professional | other
icp_summary: "young women 18-34 managing chronic health conditions"
brand_brief: |
  [1-3 paragraphs describing the business, product, audience, positioning]
tone_notes:
  sounds_like: "..."
  doesnt_sound_like: "..."
  banned_phrases_initial: ["peace of mind", "wellness warrior", ...]
founder_voice_samples: |
  [paste of founder's actual writing — chat logs, emails, anything]
website_url: "https://yapper.com"
existing_assets: "..."
launch_target_date: "2026-W30"
```

---

## Process (sequential, <2 weeks)

### Phase 1: Setup (Day 1-2)

1. Create `brands/<brand-name>/` folder structure:
   ```
   brands/<brand>/
   ├── README.md
   ├── voice-profile.md
   ├── target-audience.md
   ├── verified-facts.md
   ├── content-mix.md
   ├── performance-log.md
   ├── weeks/
   ├── exemplars/edits/
   └── inbox/
   ```

2. Run `skills/voice-from-brief.md` with brand brief → fills voice-profile.md

3. Run `skills/claim-verifier.md` sector rule identification → seeds verified-facts.md with sector rules (empty claim registry initially)

4. Fill target-audience.md using `brands/target-audience.template.md` + `docs/audience-demographics.md`

### Phase 2: Mix calibration (Day 3-4)

5. Determine content-mix weights:
   - **Platform priority:** which platforms lead, which are secondary, which are skipped
   - **Format priority:** which content types lead (image, video, text-only, PDF, etc.)
   - **Cadence:** posts/week target per platform
   - **Theme rotation:** what's the cycle for themes? (weekly, bi-weekly, monthly)

6. Populate `content-mix.md` template (empty — entries get added on publish)

### Phase 3: Account wiring (Day 5-7)

7. Identify all Blotato accounts needed (one per platform)
8. For accounts not yet wired, list OAuth setup steps
9. Once wired, document `accountId` and `pageId` (for FB/LinkedIn) in `brands/<brand>/blotato-accounts.md`
10. Test publish (dummy post) to confirm account works

### Phase 4: First batch (Day 8-10)

11. Pick first theme (1 sentence)
12. For each platform (3-5 in first batch):
    - Pick hook from `docs/platform-hooks.md`
    - Pick narrative style from `docs/narrative-styles.md` (rotate)
    - Pick visual style from `docs/visual-hooks.md`
    - Draft caption using brand voice profile
    - Run claim verifier
    - Draft media brief using `docs/media-brief.template.md`
13. Generate media (Higgsfield or manual)
14. Approval pass with founder
15. Log to `content-mix.md` BEFORE publish

### Phase 5: Publish + monitor (Day 11-12)

16. Run `docs/publish-runbook.md` pre-flight
17. Publish via Blotato
18. Capture URLs
19. Document in `performance-log.md`

### Phase 6: Refine (Day 13-14)

20. Founder reviews published posts
21. Edits feed back into `exemplars/edits/`
22. Run `skills/voice-from-brief.md` refinement loop to update `voice-profile.md`
23. Brand folder is now operational

---

## Output

After 2 weeks:
- `brands/<brand>/` is fully filled
- First batch published + tracked
- Edit-pass loop running
- Brand is autonomous in the engine

---

## Self-review pass

Before declaring onboarding "done," check:
- All docs filled (no "pending" sections)
- All required accounts wired in Blotato
- First batch published + tracked
- Voice profile actually distinct from default (not just paraphrasing anti-ai-feel)
- Edit pass loop in place

---

## Anti-patterns

- **Don't skip voice-profile.** Even for "obvious" brands, the profile is what makes the AI output non-default.
- **Don't hardcode content-mix weights.** They should evolve as the brand finds what works.
- **Don't ignore claim verification.** Especially for regulated sectors.
- **Don't skip the edit-pass loop.** That's how voice converges to actual founder tone.

---

## Worked example (abbreviated)

Input: Yapper brand brief.

Phase 1 (Day 1-2):
- Created `brands/yapper/`
- Ran voice-from-brief → filled `voice-profile.md` (warm, peer-to-peer, lowercase, fragments, anti-wellness-cliche)
- Ran claim-verifier → seeded `verified-facts.md` with consumer-health sector rules
- Filled `target-audience.md`

Phase 2 (Day 3-4):
- Determined: IG + TikTok primary, YT secondary, X/Threads minimal, LinkedIn skipped
- Format weights: 50% video, 30% image, 20% text-only

Phase 3 (Day 5-7):
- Wired YapperCare IG (55570), Yapper YT (41192), YapperCare X (55618)
- Queued OAuth for TikTok, Threads

Phase 4 (Day 8-10):
- First theme: "the small wins with chronic illness"
- Generated 4 posts across IG (image), TikTok (video), YT (video), X (text)
- 4 different narrative styles (rotation)
- Approved by eli

Phase 5 (Day 11-12):
- Published via Blotato
- All URLs captured
- Performance log empty, awaiting analytics

Phase 6 (Day 13-14):
- Eli edited 2 captions
- Edits saved to `exemplars/edits/`
- Voice-from-brief re-run, refined profile

Brand operational.

---

## Cross-references

- `skills/voice-from-brief.md` — voice generation
- `skills/ai-tell-monitor.md` — keeps universal anti-AI layer current
- `skills/claim-verifier.md` — sector-aware claim checking
- `docs/audience-demographics.md` — platform baseline knowledge
- `docs/visual-hooks.md`, `docs/platform-hooks.md`, `docs/narrative-styles.md` — generation inputs
- `docs/publish-runbook.md` — pre-flight before publish
- `brands/voice-profile.template.md`, `brands/target-audience.template.md` — output templates