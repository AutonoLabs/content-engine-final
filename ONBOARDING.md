# ONBOARDING — From Clone to First Published Post

> Anyone can clone this repo, follow this guide, and have a brand publishing within 2 weeks. No prior context needed.

---

## What this repo is

Multi-business content engine for Autono Labs portfolio. Generates platform-specific content for any brand with anti-AI-feel defaults, hooks-first engineering, voice-tuning, content-mix tracking, and AI-tell monitoring.

**Built for:**
- Multi-brand portfolio management
- New brands onboarding in <2 weeks
- Anyone wanting to run autonomous social publishing without vendor lock-in

**What it does:**
- Takes a brand brief (no seed posts needed)
- Generates voice profile, target audience, claim registry, content mix
- Plans weekly batches with diversity enforcement
- Drafts captions with platform-specific hooks + narrative styles
- Pulls media from content sources
- Routes through Higgsfield (or manual drop) for media generation
- Publishes via Blotato across 7 platforms
- Tracks performance + diversity in markdown

---

## Prerequisites

- **Python 3.11+** with venv or uv installed
- **Node.js 20+** (only if you want to extend the JS scripts)
- **Accounts:**
  - **Blotato** (publishing) — [blotato.com](https://blotato.com)
  - **Higgsfield** (video gen, optional) — [higgsfield.ai](https://higgsfield.ai)
  - **xAI / OpenAI / Anthropic** (research via perplexity, optional)
  - **Playwright** for content-pull (optional)
- **Git + GitHub account**
- **A brand to onboard** (you'll provide the brief)

---

## 1. Clone the repo

```bash
git clone https://github.com/AutonoLabs/content-engine-final.git
cd content-engine-final
```

---

## 2. Set up environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy env template and fill in keys
cp .env.example .env
# Edit .env with your actual keys (see docs/ENV-WIRING.md)
```

---

## 3. Run the brand-adapter skill

For a new brand:

```bash
# Create brand folder
mkdir -p brands/<your-brand-name>/{weeks,exemplars/edits,inbox}

# Edit the brand brief file
cp docs/templates/brand-brief.template.md brands/<your-brand-name>/brand-brief.md
# Fill in: brand name, sector, ICP, tone notes, founder samples

# Run the brand-adapter skill (via Claude/Cursor/etc)
# Or manually walk through each step in skills/brand-adapter.md
```

For each step in `skills/brand-adapter.md`:
1. **Voice profile** — use `skills/voice-from-brief.md` with your brand brief
2. **Target audience** — fill from `brands/target-audience.template.md` + `docs/audience-demographics.md`
3. **Verified facts** — sector rules from `skills/claim-verifier.md`, fill as claims emerge
4. **Content mix** — copy `brands/content-mix.template.md`
5. **Performance log** — copy `brands/performance-log.template.md`

---

## 4. Wire Blotato accounts

For each platform you want to publish on:

1. **Connect account** in Blotato dashboard
2. **Get account ID** — run:
   ```bash
   python scripts/blotato_list_accounts.py
   ```
3. **Document IDs** in `brands/<your-brand>/blotato-accounts.md` (see template below)

For Facebook pages, LinkedIn company pages, YouTube playlists → get pageId/playlistId via:
   ```bash
   python scripts/blotato_list_subaccounts.py <platform>
   ```

---

## 5. Generate first batch

```bash
# Pick theme (1 sentence)
# For each platform:
#   1. Pick hook from docs/platform-hooks.md
#   2. Pick narrative style from docs/narrative-styles.md (rotate)
#   3. Pick visual style from docs/visual-hooks.md
#   4. Draft caption using brand voice profile
#   5. Run claim verifier
#   6. Generate media brief from docs/media-brief.template.md
#   7. Generate or manually drop media
#   8. Log to brands/<brand>/content-mix.md
#   9. Run scripts/blotato_publish.py to push
#   10. Verify post URL, log to performance-log.md
```

Detailed weekly batch flow: `docs/WEEKLY-BATCH-FLOW.md`

---

## 6. Refine voice over time

After every edit pass:
```bash
# Save edits to exemplars/edits/<date>.md
# Run voice-from-brief refinement
# Update brands/<brand>/voice-profile.md
```

The skill converges to actual founder voice across 10-20 edits.

---

## File structure

```
content-engine-final/
├── README.md                        # Overview (you are here next)
├── ONBOARDING.md                    # This file — clone → publish in 2 weeks
├── LICENSE                          # MIT
├── .env.example                     # API keys template
├── .gitignore                       # Excludes secrets, generated media
├── requirements.txt                 # Python deps
├── scripts/                         # Operational scripts
│   ├── blotato_list_accounts.py
│   ├── blotato_publish.py
│   ├── blotato_create_post.py
│   ├── higgsfield_generate.py
│   ├── content_pull.py
│   └── performance_pull.py
├── prompts/                         # Per-platform generation prompts
│   ├── linkedin.md
│   ├── x.md
│   ├── instagram.md
│   ├── tiktok.md
│   ├── youtube-shorts.md
│   └── threads.md
├── docs/                            # Architecture + rules
│   ├── platform-hooks.md
│   ├── visual-hooks.md
│   ├── audience-demographics.md
│   ├── narrative-styles.md
│   ├── anti-ai-feel.md
│   ├── ai-tell-history.md
│   ├── content-type-taxonomy.md
│   ├── diversity-rules.md
│   ├── content-pull.md
│   ├── publish-runbook.md
│   ├── media-brief.template.md
│   ├── voice-profile.template.md
│   ├── ENV-WIRING.md
│   ├── WEEKLY-BATCH-FLOW.md
│   ├── WEEKLY-THEME.md
│   └── TROUBLESHOOTING.md
├── skills/                          # Generalizable skill layer
│   ├── voice-from-brief.md
│   ├── ai-tell-monitor.md
│   ├── claim-verifier.md
│   └── brand-adapter.md
├── brands/                          # Per-brand folders
│   ├── voice-profile.template.md
│   ├── target-audience.template.md
│   ├── verified-facts.template.md
│   ├── content-mix.template.md
│   ├── performance-log.template.md
│   ├── brand-brief.template.md
│   └── blotato-accounts.template.md
└── examples/                        # Reference brand showing full structure
    └── allsquared/
        ├── README.md
        ├── brand-brief.md
        ├── voice-profile.md
        ├── target-audience.md
        ├── verified-facts.md
        ├── content-mix.md
        ├── performance-log.md
        ├── blotato-accounts.md
        ├── weeks/
        │   └── 2026-W28/
        │       ├── captions.md
        │       └── media-briefs.md
        ├── exemplars/
        │   └── edits/
        └── inbox/
```

---

## Time budget for onboarding

- **Day 1-2:** Setup + voice profile + target audience
- **Day 3-4:** Claim rules + content mix + audience research
- **Day 5-7:** Blotato account wiring + tests
- **Day 8-10:** First batch generation (3-5 posts)
- **Day 11-12:** Publish + monitor
- **Day 13-14:** Refine + iterate

**Total: 2 weeks to first published batch with active learning loop.**

---

## What if something breaks?

See `docs/TROUBLESHOOTING.md` for common issues:
- Blotato auth failures
- Higgsfield credit exhaustion
- Claim verification rejections
- Diversity rule conflicts
- Platform-specific quirks

---

## What if I want to extend this?

The architecture is meant to be extensible:
- **Add a platform?** Create `prompts/<new-platform>.md`, add platform hooks to `docs/platform-hooks.md`, add to diversity rules
- **Add a sector?** Add sector rule set to `skills/claim-verifier.md`
- **Add a content type?** Add to `docs/content-type-taxonomy.md` + update diversity-rules.md
- **Add a brand?** Run `skills/brand-adapter.md` with new brand brief
- **Add a script?** Drop in `scripts/` + document in `docs/`

---

## Support

- **Issues:** Open GitHub issue
- **Discussions:** Use GitHub Discussions for Q&A
- **Updates:** Watch repo for notifications on quarterly AI-tell refreshes

---

**Last updated:** 2026-07-08
**Maintainer:** Autono Labs