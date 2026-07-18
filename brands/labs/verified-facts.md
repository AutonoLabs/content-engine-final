# Verified Facts Template

> Per-brand claim registry. Every stat, date, and regulatory claim used in social content lives here with source + verified_date. HARD GATE: no post contains an unverified claim.

Updated 2026-07-08.

---

## Sector rules

Fill in:
- **Sector:** [e.g., consumer_health | fintech | legal | professional | other]
- **Regulatory body:** [e.g., FDA/FTC, FCA/SEC, state bar, etc.]
- **Hard-violation list:** [from skills/claim-verifier.md for this sector]
- **Soft-violation list:** [from skills/claim-verifier.md for this sector]
- **Verification requirements:** [what each claim needs]

---

## Claim registry

Each claim gets an entry like this:

```markdown
### [claim-id]

- **Claim:** [exact wording used in post]
- **Source:** [URL or document reference]
- **Author/publisher:** [name]
- **Date accessed:** [YYYY-MM-DD]
- **Verified by:** [agent or human name]
- **Methodology:** [survey n=200 UK contractors, conducted March 2026, etc.]
- **Used in post:** [platform + post ID or URL]
- **Re-verification due:** [YYYY-MM-DD, annual]
- **Status:** [active | expired | rejected]
```

Add as many entries as needed. New claims get new entries. Expired claims move to "Expired claims" section.

---

## Verification log

Append-only list:

```markdown
- 2026-07-08: Initial claim [claim-id] verified by [name] from [source]
- 2026-07-08: Claim [claim-id] rejected — source unreliable
```

---

## Expired claims

Claims that no longer hold (date passed, source dead, regulatory change). Move here, don't reuse.

---

## Rejected claims

Claims that failed verification. Useful to prevent re-attempts. Add with reason:
```markdown
- "78% of UK contractors prefer milestone-based payment" — rejected: no source survey, appears AI-fabricated
```

---

## See also

- `skills/claim-verifier.md` — full verification protocol
- `brands/<brand>/voice-profile.md` — voice layer
- `docs/anti-ai-feel.md` — universal banned phrases (AI tells)
- `skills/brand-adapter.md` — onboarding pipeline that populates this

---

**Note:** This file may be empty at brand creation. That's OK — empty means no claims are approved yet. Posts must avoid specific stats, dates, customer counts, regulatory status until this file is populated.

When populated, every post that uses a claim MUST reference an entry here. No exceptions.
