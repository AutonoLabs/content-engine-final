# ONBOARDING — From Clone to First Published Post

> Anyone can clone this repo and have a brand publishing within 2 weeks. No prior context needed.
>
> **Two human touchpoints, that's it:** paste prompts into Higgsfield, and approve posts before publish. Everything else is agent-executable from this repo.

---

## What this repo is

An open-source content engine for any brand. Generates platform-specific content with anti-AI-feel defaults, hooks-first engineering, voice-tuning per brand, content-mix tracking, and AI-tell monitoring.

**Built for:**
- Multi-brand portfolio management
- New brands onboarding in <2 weeks
- Anyone wanting to run autonomous social publishing without vendor lock-in

**What it does:**
- Takes a brand brief (no seed posts needed)
- Generates voice profile, target audience, claim registry, content mix
- Plans weekly batches with diversity enforcement
- Drafts captions with platform-specific hooks + narrative styles
- Routes media through Higgsfield (with human-in-the-loop prompt packets)
- Publishes via Blotato across 9 platforms
- Tracks performance + diversity in markdown
- Self-improves via three loops with a human-locked compliance spine

**Two human touchpoints:**
1. **Paste prompt packets into Higgsfield UI** (paste → download → rename → drop in inbox/)
2. **Approve posts before publish** (review captions, hit publish)

Everything else — planning, drafting, validating, packet generation, pairing, publishing on approval, measuring, reweighting, voice updates — runs from this repo.

---

## Prerequisites

- **Python 3.11+** with venv or uv installed
- **Git + GitHub account**
- **A brand to onboard** (you provide the brief)
- **Accounts (when ready to publish):**
  - **Blotato** (publishing) — [blotato.com](https://blotato.com)
  - **Higgsfield** (video gen, optional) — [higgsfield.ai](https://higgsfield.ai) — Ultra plan recommended
  - **Playwright** for content-pull (optional) — `pip install playwright && playwright install`

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

# Copy env template
cp .env.example .env
# Edit .env when you have API keys (see docs/ENV-WIRING.md)
```

---

## 3. Run doctor (preflight check)

```bash
python scripts/doctor.py
```

Should report "All checks passed" (or only env-key warnings if you haven't added keys yet). If it reports missing files, your checkout is incomplete — re-clone or check git status.

---

## 4. Onboard your brand

```bash
# From repo root — creates folder + copies all 7 templates:
python scripts/onboard_brand.py --name <your-brand> --sector <sector>

# Sector options: consumer_health | fintech | legal | professional | education | creative | other
```

This creates:
```
brands/<your-brand>/
├── brand-brief.md           # FILL THIS FIRST
├── voice-profile.md
├── target-audience.md
├── verified-facts.md
├── content-mix.md
├── performance-log.md
├── blotato-accounts.md
├── weeks/                   # weekly batches go here
├── exemplars/edits/         # edit diffs accumulate here
└── inbox/                   # media files dropped here
```

### 4a. Fill the brand brief

Open `brands/<your-brand>/brand-brief.md`. The template has inline "delete me" examples showing what good looks like — delete that section before filling in your own.

**Required fields:** Brand name, sector, what you do (1-3 sentences), target audience, tone (sounds like / doesn't sound like), banned phrases, founder voice samples.

### 4b. Generate voice profile

Use the `skills/voice-from-brief.md` skill — either with an LLM agent (Claude, Cursor, etc.) or by manually walking through its steps.

The output fills in `brands/<your-brand>/voice-profile.md`. Make sure the `sector:` field at the top matches what you passed to `onboard_brand.py` (drives `validate_post.py` phrase policies).

### 4c. Fill target audience + verified facts

- `target-audience.md` — use `docs/audience-demographics.md` as baseline, override with brand-specific segments
- `verified-facts.md` — apply the sector's compliance rules from `skills/claim-verifier.md`. For regulated sectors (fintech, legal, health), this is critical — the validator blocks posts that make unverified claims

### 4d. Wire Blotato accounts

```bash
# Connect accounts in Blotato dashboard
# Then list them:
python scripts/blotato_list_accounts.py

# Document IDs in brands/<your-brand>/blotato-accounts.md
```

---

### 4e. Register in portfolio.yaml + brand.yaml

Add your brand to `portfolio.yaml` (`brands:` section) and fill
`brands/<your-brand>/brand.yaml` — sector, platform→account-ID wiring (from
step 4d), and defaults. This is what `scripts/engine.py` reads; the .md files
stay the human knowledge layer. `python scripts/doctor.py` verifies both.

---

## 5. Plan your first batch

```bash
# The orchestrator wraps the runbook steps:
python scripts/engine.py plan --brand <your-brand> --week $(date +%Y-W%V)
# Draft posts as post-NN-<platform>.md per docs/post-file-spec.md, then:
python scripts/engine.py validate --brand <your-brand>
python scripts/engine.py approve --brand <your-brand>    # human gate
python scripts/engine.py schedule --brand <your-brand>   # publishes + logs content-mix

# Full runbook detail:
cat docs/WEEKLY-BATCH-FLOW.md
```

For each post:
1. Pick a theme (rotate per `docs/diversity-rules.md`)
2. Pick narrative style + hook pattern + visual style (rotate)
3. Draft caption using `brands/<your-brand>/voice-profile.md` as conditioning
4. Verify any claims against `verified-facts.md`

Save captions as: `brands/<your-brand>/weeks/<YYYY-W##>/post-NN-<platform>.md`

---

## 6. Generate media (Higgsfield human-in-the-loop)

```bash
# 1. Write media briefs for each visual post
# Save to brands/<your-brand>/weeks/<YYYY-W##>/media-briefs.md
# (use docs/media-brief.template.md as format spec)

# 2. Generate prompt packets
python scripts/media_packet.py --brand <your-brand> --week <YYYY-W##>

# This emits one packet per post at weeks/<YYYY-W##>/media-packets/

# 3. HUMAN TOUCHPOINT 1: For each packet:
#    a. Open the packet file
#    b. Paste the prompt into Higgsfield UI (model + settings specified)
#    c. Download the result
#    d. Rename to the packet's return-filename contract (e.g., 2026-W30-01.mp4)
#    e. Drop in brands/<your-brand>/inbox/

# 4. Pair inbox files back to packets
python scripts/pair_media.py --brand <your-brand>

# This moves matched files into the week folder and reports any unmatched.
```

**Why human-in-the-loop:** Higgsfield doesn't have a public API for media generation. The packet/inbox contract makes the human's job 90 seconds per asset with zero judgment about where things go.

---

## 7. Validate + publish

```bash
# Validate each post against voice, claims, diversity
python scripts/validate_post.py --brand <your-brand> --platform <platform> --text "..."
# OR validate all posts from a captions file:
python scripts/validate_post.py --brand <your-brand> --platform <platform> --caption-file brands/<your-brand>/weeks/<YYYY-W##>/post-NN-<platform>.md

# HUMAN TOUCHPOINT 2: Review each caption before publishing

# Publish approved posts
python scripts/blotato_publish.py --brand <your-brand> --platform <platform> --text "..." --media-url "..."
# OR via the blotato MCP tool if running in Claude/Cursor

# Get post URL
python scripts/blotato_get_post_status.py <submission-id>

# Log to content-mix + performance-log (see templates for format)
```

---

## 8. Track performance + iterate

```bash
# Pull engagement data weekly
python scripts/performance_pull.py --brand <your-brand> --days 7

# Surface winning patterns
python scripts/compare_performance.py --brand <your-brand>

# Run doctor to catch silent failures
python scripts/doctor.py --brand <your-brand>
```

Each week:
- `compare_performance.py` updates `pattern-weights.md` (Loop B in `docs/SELF-IMPROVEMENT.md`)
- Edit diffs in `exemplars/edits/` accumulate (Loop A input)
- Engine-level docs may get cross-brand updates via PR (Loop C)

**Locked spine (never autonomous):** verified facts, sector compliance rules, approval gate, banned compliance phrases. These require human review on every change.

---

## File structure

```
content-engine-final/
├── README.md                        # Overview
├── ONBOARDING.md                    # This file
├── LICENSE                          # MIT
├── .env.example                     # API keys template
├── .gitignore
├── requirements.txt                 # Python deps
├── scripts/
│   ├── onboard_brand.py             # Bootstrap new brand
│   ├── doctor.py                    # Preflight check
│   ├── compare_performance.py       # Pattern detection (Loop B)
│   ├── validate_post.py             # Anti-AI + diversity + claims
│   ├── media_packet.py              # Generate Higgsfield prompt packets
│   ├── pair_media.py                # Pair inbox files with packets
│   ├── content_pull.py              # Research from URLs
│   ├── performance_pull.py          # Pull engagement data
│   ├── blotato_client.py
│   ├── blotato_publish.py
│   ├── blotato_list_accounts.py
│   ├── blotato_get_post_status.py
│   └── higgsfield_generate.py       # Model registry + credit tracking
├── docs/
│   ├── SELF-IMPROVEMENT.md          # 3-loop architecture + locked spine
│   ├── WEEKLY-BATCH-FLOW.md         # Operational runbook
│   ├── diversity-rules.md
│   ├── higgsfield-prompts.md        # Prompt library + accept/reject gates
│   ├── compare-performance.md       # Engine documentation
│   ├── media-brief.template.md
│   ├── ENV-WIRING.md
│   └── TROUBLESHOOTING.md
├── skills/
│   ├── voice-from-brief.md
│   ├── ai-tell-monitor.md
│   ├── claim-verifier.md
│   └── brand-adapter.md
├── brands/
│   ├── *.template.md                # 7 templates with inline examples
│   └── <brand-name>/                # Per-brand folders
└── examples/
    └── allsquared/                  # Worked example
        ├── content-mix.md           # Canonical format reference
        └── performance-log.md
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

```bash
python scripts/doctor.py        # catches the silent failures
```

See `docs/TROUBLESHOOTING.md` for:
- Blotato auth failures
- Higgsfield credit exhaustion
- Claim verification rejections
- Diversity rule conflicts
- Platform-specific quirks

---

## What if I want to extend this?

- **Add a platform?** Add platform hooks to `docs/platform-hooks.md`, update `docs/diversity-rules.md`
- **Add a sector?** Add sector rule set to `skills/claim-verifier.md` + `validate_post.py` policies
- **Add a content type?** Add to `docs/content-type-taxonomy.md` + update diversity-rules.md
- **Add a brand?** `python scripts/onboard_brand.py --name <brand> --sector <sector>`
- **Add a script?** Drop in `scripts/` + document in `docs/` + add to `scripts/doctor.py` required list

---

## Support

- **Issues:** Open GitHub issue
- **Discussions:** Use GitHub Discussions for Q&A
- **Updates:** Watch repo for notifications on quarterly AI-tell refreshes

**Last updated:** 2026-07-08 (v1.3 — brand-agnostic, two-touchpoint workflow, doctor preflight)
**Maintainer:** AutonoLabs / open-source contributors