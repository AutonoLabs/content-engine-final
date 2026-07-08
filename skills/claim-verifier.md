---
name: claim-verifier
description: Sector-aware claim verification. Health (FDA/FTC), finance (FCA/SEC), legal (state bar), consumer products (FTC). Populates brands/<brand>/verified-facts.md with source + verified_date. Rejects posts with unverifiable claims.
---

# Claim Verifier

> Sector-aware verification of any claim, stat, or assertion in social content. Rejects unverifiable claims. Populates `brands/<brand>/verified-facts.md` with source + verified_date. Critical for: consumer health (FTC/FDA), fintech (FCA/SEC), legal services (state bar), professional services (industry regs).

---

## Why this skill exists

Every post can break trust. Three failure modes are common:

1. **Made-up stat to land the post.** ("78% of contractors..." when no such study exists.) Common AI-failure. Fix: source-required gate.

2. **Real stat, wrong attribution.** (LinkedIn's "X% engagement boost" when the source actually said something different.) Common copywriter-failure. Fix: source + verified_date required.

3. **Real stat, outdated.** ("Founded in 2019" when actually 2018.) Drift over time. Fix: re-verify annually.

4. **Sector violations.** (Health brand saying "cures X" without FDA, fintech saying "guaranteed returns" without FCA, lawyer saying "we'll win your case" — all actionable.) Fix: sector-specific rule sets.

---

## When to use this skill

- Before any post containing a stat or factual claim
- When populating `verified-facts.md` for a new brand
- Annual re-verification of all claims in `verified-facts.md`
- When a brand pivots into a new sector or claim category

---

## Sector-specific rule sets

### Consumer health / wellness (Yapper, etc.)

**Hard violations (FTC):**
- "Cures," "treats," "diagnoses" without FDA approval
- "Clinically proven" without study citation
- Health claims tied to products without substantiation
- Before/after photos without disclosure

**Soft violations (FTC):**
- "Studies show" without specific source
- Affiliate links without #ad disclosure

**Verification requirements:**
- All health claims: source URL + author + study sample size
- All stats: date + source + context
- All testimonials: written consent + relationship disclosure

### Fintech / financial services (AllSquared, etc.)

**Hard violations (FCA/SEC):**
- "Guaranteed returns" without risk disclosure
- Performance claims without context (e.g., "X% APY" only valid for specific terms)
- Regulatory status misrepresentation (e.g., saying "FCA-regulated" when only registered, not authorized)
- Promotional claims crossing into advice

**Soft violations:**
- Generic claims without source ("most customers prefer...")
- Comparisons to competitors without disclaimer

**Verification requirements:**
- All regulatory claims: registration/authorization number + official register URL
- All stat claims: source + date + sample methodology
- All product/feature claims: feature lives in product + legal review

### Legal services (Motio, etc.)

**Hard violations (state bar):**
- "We can win your case" (guaranteed outcome)
- Specific outcome projections ("you'll get $X")
- Solicitation in jurisdictions where prohibited

**Verification requirements:**
- All case result claims: written client consent + matter number
- All fee/structure claims: actual engagement letter language

### Other regulated

- Consumer products: FTC compliance, Prop 65 (CA), child-product safety
- Professional services: industry-specific compliance + certification claims
- Crypto: SEC enforcement context (claims about returns are dangerous)
- Education: accreditation claims

### Unregulated businesses

Even unregulated businesses should verify:
- "5,000 customers" — actual count + recent
- "98% satisfaction" — actual survey + methodology
- "Featured in [publication]" — actual publication + date

---

## Process

### Step 1: Identify claims in the post

Scan the proposed caption for:
- Numbers (counts, percentages, dollar amounts)
- Dates (founded, launched, milestone)
- Regulatory claims (regulated, certified, compliant, partnered)
- Performance claims (faster, better, more effective)
- Comparative claims (vs. competitors, vs. industry standard)
- Testimonials / case studies
- Health/safety/efficacy claims

### Step 2: For each claim, run sector check

Apply the relevant sector rule set above.

### Step 3: For each stat/claim, demand source

Required:
- Source URL or document
- Source date
- Source author / publisher
- Methodology if applicable
- Sample size if applicable

### Step 4: Verify

For each source:
- URL is reachable (curl/fetch check)
- Source actually says what the claim says (cross-reference)
- Date is recent enough to still be relevant

### Step 5: Populate verified-facts.md

For verified claims, add entry:

```markdown
## [Claim ID]

**Claim:** "78% of UK contractors prefer milestone-based payment"
**Source:** [URL]
**Author/publisher:** [Name]
**Date accessed:** 2026-07-08
**Verified by:** [agent name or human]
**Methodology:** [survey n=200 UK contractors, conducted March 2026]
**Used in post:** [post ID or URL]
```

### Step 6: Gate

If any claim cannot be verified:
- **Reject the post** (do not publish)
- **Suggest alternatives** ("rewrite without the stat" or "swap to verifiable claim")

---

## Output format

Save claim entries to `brands/<brand>/verified-facts.md`. Format:

```markdown
# Verified Facts — [Brand Name]

> Per-brand claim registry. Every stat, date, and regulatory claim used in social content lives here with source + verified_date. HARD GATE: no post contains an unverified claim.

## Sector rules
[Which sector rule set applies, e.g., "Fintech — FCA"]

## Claim registry
[Entries as above]

## Verification log
[Append-only list: date, claim ID, verifier, outcome]

## Rejected claims (do not use)
[Any claim that failed verification, with reason. Useful to prevent re-attempts.]
```

---

## Annual re-verification protocol

Every claim entry in `verified-facts.md` should be re-verified annually:
- Source still reachable?
- Stat still current?
- Regulatory status still accurate?
- Company facts (founded date, etc.) still accurate?

Mark entry as `re-verified: YYYY-MM-DD` when checked.

If a claim expires (e.g., "launched 2024" becomes irrelevant in 2026), move to "expired" sub-section, don't reuse.

---

## Self-review pass

Before approving any post, check:
- Any claim in the post has a corresponding `verified-facts.md` entry?
- Source is reachable and current?
- Sector rules respected?

If any check fails → rewrite or escalate.

---

## Worked example (abbreviated)

Input: AllSquared caption with claim "8 months to FCA authorization"

Process:
1. Identified as regulatory claim (FCA status)
2. FCA rule set applies
3. Demanded source: official FCA register, FRN, authorization date
4. Verified in FCA register (assumed hypothetical here)
5. Populated `verified-facts.md` with claim ID, source URL, date

Output: Post approved for publish, claim now versioned in verified registry.

---

## Cross-references

- `docs/anti-ai-feel.md` — banned words (anti-AI), claim-verifier handles substance (anti-error)
- `brands/verified-facts.template.md` — output structure
- `brands/<brand>/voice-profile.md` — voice layer
- `skills/brand-adapter.md` — combines this for full onboarding