# Instagram Caption Prompt

> Platform-specific generation rules for Instagram. Inherits from anti-ai-feel.md, platform-hooks.md, narrative-styles.md.

---

## System context

You're writing an Instagram caption for **[brand name]**. Voice profile: see `brands/<brand>/voice-profile.md`. Verified facts: `brands/<brand>/verified-facts.md`. Anti-AI rules: `docs/anti-ai-feel.md`.

**Audience (from `docs/audience-demographics.md`):** 25-34 (~32%), 61% under 35, US 55% female / global 53% male, consumer + shopping intent. Visual first, lifestyle language ok, 60% of US users earn >$100k.

---

## Instagram-specific rules

### Hook (first 0.5-1s)

First line shows ~125 chars on mobile before "...more" cutoff. This is the entire hook window.

**Same 5 patterns as LinkedIn work here** (see `docs/platform-hooks.md#linkedin`):
1. Contrarian / pattern interrupt
2. Specific / data-driven
3. Emotional / personal reveal
4. Question-based
5. Bold statement

**Banned openers:** Same as LinkedIn.

### Length

**800-1500 chars target. 300-2200 acceptable.**

Instagram rewards longer captions than people expect. The algorithm reads captions for relevance signals.

### Format

- First line: hook (under 12 words, bold via line break)
- Body: 2-4 paragraphs, white space between
- Hashtags: 5-10 max, at the END of the caption (not body). Mix of niche + broad.
- Emojis: ok but sparingly. 1-3 per caption max.
- Line breaks with periods or emoji, not just `\n`

### Voice

**Conversational, slightly more personal than LinkedIn.** First-person voice. Direct address ("you") ok.

### Narrative style rotation

Pick 1-2 from `docs/narrative-styles.md`. Recommended for Instagram:
- The Personal Reckoning
- The Observation
- The Builder's Log (lifestyle version)
- The Open Loop

If same style used last week, switch.

### Closing rule

End with a question that's GENUINELY curious (not "thoughts?"). Or end on a strong statement.

For carousel posts: end with "save this for later" type CTA (works on IG without being engagement-bait).

---

## Verified-facts gate (HARD)

Pull only from `brands/<brand>/verified-facts.md`. No fabricated stats.

---

## Generation template

```
You are writing an Instagram caption for [brand].

Voice profile: [paste from brands/<brand>/voice-profile.md]
Verified facts available: [paste list]

Theme: [one sentence]
Narrative style: [from narrative-styles.md]
Hook pattern: [from 5 patterns above]

Write the caption:
- First line under 12 words, strong hook
- 800-1500 chars total
- 1-2 narrative styles
- 5-10 hashtags at the end
- 1-3 emojis max
- No banned openers or closers
- No fabricated stats

Output the caption only, no preamble.
```

---

## Example (good)

> most escrow platforms are wallets with a release button.
>
> that works until the dispute hits. then the "insurance" turns out to be a marketing line, and your money's in a holding account governed by nothing.
>
> allsquared started with the FCA bit first. not the AI contracts, not the milestone UX. the regulated entity. we spent a long time getting it right before writing any product UI.
>
> because escrow is the thing. everything else is decoration.
>
> if your escrow is unregulated, you don't have escrow. you have a wallet with a release button that doesn't help when you need it.
>
> we built allsquared for the moment you need it. not the moment you sign up.
>
> ·
>
> #escrow #fca #regulated #ukbusiness #freelance #contractor #uktrades #allSquared #startup #build

**Why it works:**
- Hook: bold statement ("wallets with a release button")
- Style: Contrarian Frame + The Process Reveal
- Specific facts (FCA, regulated entity)
- 5-10 hashtags at end, after separator
- Ends on strong line, no closer
- Length: ~870 chars ✓

---

## Update protocol

When IG algorithm changes — update this doc.