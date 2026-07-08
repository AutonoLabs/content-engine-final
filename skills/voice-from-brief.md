---
name: voice-from-brief
description: Generate a per-brand voice profile from a brand brief (no seed posts required). Input: brand theme, product positioning, target audience, founder tone notes. Output: voice-profile.md filled in. Anti-AI-feel by default, anti-AI rules baked in.
---

# Voice-from-Brief

> Generate a brand voice profile when no past posts exist (typical for new businesses). Anti-AI-feel enforced. Works for any new business in <1 hour.

---

## Why this skill exists

Many businesses we onboard don't have a track record of posts yet. Asking for "5-10 of your past posts" doesn't apply.

What we DO have:
- website URL or content
- product description
- founder notes about how the brand should/shouldn't sound
- target audience + what they care about
- sometimes: 1-2 examples of the founder's actual talking/chat/email voice

This skill takes that input and generates a **synthetic-but-grounded voice profile** that:
- fits the brand positioning
- bans AI tells by default (cross-references `docs/anti-ai-feel.md`)
- rotates rhythm and structure to avoid boring sameness
- starts synthetic but converges to actual voice via edit pass

---

## When to use this skill

- New business onboarding
- Voice profile needs major overhaul (pivot, rebrand)
- Existing voice profile is too vague / not actionable
- User wants to refresh brand tone

---

## Input schema

The skill takes one or more of:

1. **Brand theme / positioning** (1-3 sentences)
   - Example: "UK FCA-regulated escrow platform for project-based work — kitchens, extensions, agency retainers"

2. **Product description** (1-2 paragraphs)
   - What it is, who it's for, what makes it different

3. **Target audience**
   - Demographics + psychographics + what they care about

4. **Tone notes** (free-form)
   - "Sounds like: ___"
   - "Doesn't sound like: ___"
   - "Banned phrases: ___"

5. **Founder voice samples** (if any)
   - Chat logs, emails, anything they've written themselves
   - Even fragments help

6. **Web content** (URL or pasted)
   - Homepage, about page, manifesto

---

## Process

### Step 1: Synthesize the brand snapshot

Combine inputs 1-2-3 into a tight brand snapshot (max 200 words). This becomes the first section of `voice-profile.md`.

### Step 2: Extract tone signals

Pull from inputs 4-5-6:
- Sentence length tendency
- Register (formal / casual / peer / corporate)
- Slang / jargon level
- Hedging vs declarative
- Opening patterns (does the brand lead with statement / question / story / contrast?)
- Closing patterns (CTA / open-loop / tagline / question?)
- Punctuation tendency (heavy em-dash? semicolons? fragments?)

### Step 3: Generate banned-phrases list (brand-specific)

Inherit from `docs/anti-ai-feel.md` (universal banned words).
Add brand-specific bans:
- Industry clichés (FCA-aware brands: "peace of mind", "trusted by thousands")
- Competitor-speak (anything that sounds like a competitor's tagline)
- Founder pet peeves (whatever the founder explicitly flags)

### Step 4: Generate rhythm rules (brand-specific)

Based on extracted signals:
- Sentence length windows: e.g., "8-20 words, average 14, no 3 consecutive long sentences"
- Openers distribution: e.g., "60% opening statements, 25% questions, 15% contrasts"
- Closing patterns: same distribution rule

### Step 5: Generate the voice profile document

Output structure (matches `brands/voice-profile.template.md`):

```markdown
# Voice Profile — [Brand Name]

## Brand snapshot
[200-word snapshot]

## Tone
- [5-8 bullet points describing the voice]

## Sentence rhythm
[specific rules with numbers]

## Openers
[distribution rules with examples]

## Closings
[distribution rules with examples]

## Banned phrases
### Universal (from anti-ai-feel.md)
[inherited list]

### Brand-specific
[brand-specific bans]

## Verified facts
[reference verified-facts.template.md]

## Edit-pass protocol
[how to feed edits back into this profile]
```

### Step 6: Self-review pass

Before saving the profile, check it against:
- Does it pass the "would I read this at 2am when I can't sleep" test? (rhythm + specificity)
- Does it ban AI tells explicitly?
- Is it actionable? (Can an AI agent use it without guessing?)
- Is it evolvable? (Can we update it as the brand voice converges via edits?)

### Step 7: Save and reference

Save to `brands/<brand-name>/voice-profile.md`.
The agent should reference this when generating any content for the brand.

---

## Output format requirements

Must work as a prompt input:
- Self-contained (no external references that aren't paths)
- Numbered rhythm rules where possible
- Banned-phrases list as an explicit checklist
- Real-world examples in-line, not abstract descriptions

---

## Self-refinement loop

After every batch of edits from the founder:
1. Read the edits in `brands/<brand>/exemplars/edits/`
2. Identify patterns (what got cut, what got added, what got rephrased)
3. Update `voice-profile.md` accordingly
4. Re-anchor banned phrases if new AI-tell phrases appear
5. Update rhythm rules if sentence-length tendencies shift

This is the "voice converges over time" loop. Document each refinement in `voice-profile.md` with date + reason.

---

## Anti-patterns to avoid

- **Don't write abstract descriptors.** "Authentic voice" is meaningless. "20-word sentences, lowercase opener, no CTA" is actionable.
- **Don't describe what the brand is for.** Describe how it talks.
- **Don't ignore founder signals.** If the founder says "we don't use exclamation marks," that becomes a hard rule.
- **Don't skip the AI-tell ban.** Even if the brand is technical or formal, AI tells still apply (just maybe less em-dashes, more rigid structure).
- **Don't generate static profiles.** The skill is meant to be re-run as the voice converges.

---

## Worked example (abbreviated)

Input: AllSquared brand brief — UK FCA-regulated escrow for project work, founder-to-founder, premium register, regulatory clarity without being pedantic.

Output (excerpt):
```
## Tone
- Founder-to-founder (peer level, not B2B corporate)
- Regulatory clarity without pedantry
- Construction-trade vocabulary ok (milestone, retention, snagging, JCT)
- Premium register — quality > quantity
- No exclamation marks anywhere
- Em-dashes used sparingly (max 1 per long post)
```

This is actionable. An AI can generate without guessing.

---

## Cross-references

- `docs/anti-ai-feel.md` — universal banned phrases + AI tells
- `brands/voice-profile.template.md` — output structure template
- `skills/ai-tell-monitor.md` — keep banned list current
- `skills/brand-adapter.md` — combines this + other skills for full onboarding