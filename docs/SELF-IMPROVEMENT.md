# Self-Improvement Architecture

> How the engine gets better over time, what's allowed to change automatically, and what stays under human control.
>
> **TL;DR:** Three loops run autonomously on different cadences. Verified facts, sector compliance, and approval gate are **locked** — human-only, never self-modified.

---

## Why this exists

A self-modifying content system with broken measurement (compare_performance.py producing confidently-wrong 100x-off recommendations) would converge on noise. Self-improvement is only safe downstream of correct measurement, so:

**Loop B (the data-driven loop) requires the v1.3 measurement fixes** to be safe. Patch 1 in fable's review is the prerequisite.

Once measurement is sound, the engine can improve itself along three dimensions:

---

## Loop A — Voice convergence (per brand, human-signal-driven)

**Cadence:** After every edit pass (Eli taps ✏️ Edit on a draft).
**Trigger:** Human edit creates a diff between draft and published.
**Scope:** `brands/<brand>/voice-profile.md` for that brand only.

**What happens:**
1. Agent diffs draft vs published caption
2. Agent appends a structured entry to `brands/<brand>/exemplars/edits/YYYY-MM-DD.md`:
   ```markdown
   # Edit annotation

   ## Original (draft)
   "..."

   ## Published
   "..."

   ## What I changed
   - Cut the "just"
   - Removed em-dash chain
   - Added retention angle

   ## Pattern observed
   - I always cut "just" (3rd occurrence)
   ```
3. If the same pattern appears in 3+ edits, agent proposes a voice-profile update (NOT a silent rewrite)
4. Diff is shown to human; on approval, change appends with date + evidence
5. Voice profile becomes a changelog, so a later agent or human can audit and revert

**Locked:** Banned phrases that affect compliance (e.g. "guaranteed returns", "your money is safe" for fintech) can only be ADDED with human approval, never removed automatically.

---

## Loop B — Performance-driven pattern weighting (per brand, data-driven)

**Cadence:** Weekly, after `compare_performance.py` run.
**Trigger:** n≥3 for any pattern (hard guardrail; smaller n is noise).
**Scope:** `brands/<brand>/pattern-weights.md` for that brand only.

**What happens:**
1. Run `python scripts/compare_performance.py --brand <name>`
2. For each field (theme, narrative_style, hook_pattern, visual_style, format, audience_segment):
   - If any value has n≥3 AND avg is 30%+ better than another value with n≥3, weight increases
   - Weight change is bounded: shifts by 0.05 per cycle, never to zero
3. Batch planner reads `pattern-weights.md` when choosing the next batch's theme/style mix
4. Diversity rules still apply — weights don't override the rotation policy, they only bias the rotation pool

**Hard guardrails:**
- Minimum n=3 per pattern before any weight moves (single-post wins are noise)
- Weights shift in bounded steps (0.05/cycle max)
- Weights never go to zero (kills exploration; bandit problem needs preserved arms)
- Weights never exceed 0.5 (50/50 split — keeps room for exploration)
- Diversity rules (`docs/diversity-rules.md`) are the exploration policy; weights bias within it

**Locked:** No pattern weight can be set to 1.0 (forced winner). No pattern can be set to 0 (forced loser). The diversity rules exist to prevent both.

---

## Loop C — Engine-level learning (cross-brand, slow)

**Cadence:** When triggered (≥2 brands independently produce the same edit pattern or same anti-pattern).
**Trigger:** Edit annotation in `exemplars/edits/` shows the same pattern across 2+ brands.
**Scope:** `docs/anti-ai-feel.md`, `docs/platform-hooks.md`, `docs/narrative-styles.md` — the engine-level docs.

**What happens:**
1. Agent notices pattern duplication across brands
2. Agent opens a PR/diff to the engine-level doc, with dated entry and which brands' data triggered it:
   ```markdown
   ## 2026-07-15 — "cut 'just' as filler" graduated to engine level
   - Triggered by: allsquared (3x edits), yapper (4x edits)
   - Added to anti-ai-feel.md banned list with explanation
   ```
3. Human reviews PR; merges or rejects

**Locked:** Cross-brand changes always require human review. No autonomous edits to engine docs.

---

## Locked spine — what humans own

These never change autonomously:

| Layer | Who changes it | Trigger |
|---|---|---|
| Hooks, visual styles, pattern weights | Agent, autonomously | Loop B, n≥3 |
| Voice profile, rhythm, banned style phrases | Agent proposes, appends with evidence | Loop A |
| Engine docs (anti-ai-feel, platform-hooks) | Agent proposes via PR/diff | Loop C, ≥2 brands |
| **Verified facts** | **Human only** | **Never autonomous** |
| **Sector compliance rules** | **Human only** | **Never autonomous** |
| **Approval gate (before publish)** | **Human only** | **Never autonomous** |
| **Banned compliance phrases** | **Human only** | **Never autonomous** |

For AllSquared specifically, the locked spine includes:
- "guaranteed returns" / "risk-free" / "your money is safe" — FCA financial promotion compliance
- Claims about milestone protection that imply guarantee
- Anything in `verified-facts.md`

These cannot be edited, removed, or downweighted by any loop. A change here requires a human + a dated entry in the brand's compliance log.

---

## Why this matters for external partners

When yapper or any future brand picks up the repo:
- They get self-improving content generation that adapts to their audience
- They do NOT get a system that can quietly remove compliance gates or "optimize" past approval requirements
- The locked spine is the trust boundary — the parts that guarantee the engine won't get them in regulatory trouble

If a future brand is in a different sector (legal, health), the locked-spine table in their brand's `voice-profile.md` can be extended with sector-specific phrases, but always human-curated.

---

## Cross-references

- `docs/compare-performance.md` — engine behind Loop B
- `docs/diversity-rules.md` — exploration policy that weights bias within
- `docs/anti-ai-feel.md` — engine-level doc that Loop C updates
- `docs/WEEKLY-BATCH-FLOW.md` — weekly cadence that runs Loop B
- `brands/<brand>/voice-profile.md` — Loop A target
- `brands/<brand>/pattern-weights.md` — Loop B output (created on first run)

**Last updated:** 2026-07-08 (v1.4 — three-loop architecture with locked spine)