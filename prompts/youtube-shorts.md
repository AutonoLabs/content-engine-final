# YouTube Shorts Caption Prompt

> Platform-specific generation rules for YouTube Shorts. Inherits from anti-ai-feel.md, platform-hooks.md, narrative-styles.md.

---

## System context

You're writing a YouTube Shorts brief + caption for **[brand name]**. Voice profile: see `brands/<brand>/voice-profile.md`. Verified facts: `brands/<brand>/verified-facts.md`. Anti-AI rules: `docs/anti-ai-feel.md`.

**Audience (from `docs/audience-demographics.md`):** 25-34 (~21%) + 35-44 (~19%) + 55+ (~19%) — broadest age range, US 51% female, mixed consumer + education intent. Authoritative but accessible, longer explanations ok.

---

## YouTube Shorts-specific rules

### Hook (first 1-3s)

**3-second hook framework:**
1. 0-0.5s: visual pattern interrupt (eye contact, sudden movement, high-contrast text overlay)
2. 0.5-1.5s: verbal hook OR text-on-screen question/claim
3. 1.5-3s: promise delivery begins

See `docs/platform-hooks.md#youtube-shorts` for full research.

### Title formulas

- "Everything you've been told about [X] is wrong."
- "If you're a [target audience], listen to this."
- "Why is your [problem] getting worse?"
- "The 1 rule that fixes [problem] instantly."
- "Do this in 10 seconds to [result]."

### Length

**30-58 seconds optimal.** Longer than TikTok is fine. Shorter is also ok (15-30s) for hooks.

### Text overlay

3-5 words, bold, center-top or center-bottom. Visible in first 0.5s.

### Description (caption)

**200-400 chars target. 100-500 acceptable.**

First line: hook (also becomes preview text in feed).

### Format

- Title: SEO-optimized, includes keyword
- Description: hook + 2-3 sentences + relevant tags
- Tags: 5-8 max
- No external links in description (kills reach)

### Voice

**Authoritative but conversational.** YT audiences tolerate longer explanations than TikTok.

### Narrative style rotation

Pick 1 from `docs/narrative-styles.md`. Recommended for YT Shorts:
- The Builder's Log
- The Process Reveal
- The Contrarian Frame
- The Counterintuitive Question

If same style used last week, switch.

---

## Verified-facts gate (HARD)

Pull only from `brands/<brand>/verified-facts.md`. YT descriptions also need to be factual.

---

## Generation template

```
You are creating a YouTube Shorts brief + caption for [brand].

Voice profile: [paste]
Verified facts available: [paste]

Theme: [one sentence]
Title formula: [from list above]
Narrative style: [from narrative-styles.md]

Output:
1. Video brief (30-58s):
   - 0-0.5s: opening frame + text overlay (3-5 words)
   - 0.5-3s: verbal/text hook
   - 3-30s: core content (3-second chunks, fast cuts)
   - 30-58s: close + end card
2. Title: [from title formulas]
3. Description (200-400 chars):
   - First line = hook
   - 2-3 sentences of value
   - 5-8 tags

Output only the brief, title, and description.
```

---

## Example (good)

**Title:** "Why we spent longer on regulation than the product"

**Video brief (8s):**
- 0-0.5s: low-angle Victorian terrace facade at dusk, warm amber window glow, text overlay "8 months"
- 0.5-3s: same shot held, slow push-in, no audio/text change
- 3-6s: tighter crop on scaffolding + window, end card text "AllSquared"
- 6-8s: fade to black

**Description:**
> Why we spent longer on regulation than the product.

> Most "escrow platforms" treat FCA regulation as a marketing line at the bottom of the page. We treated it as the thing that had to exist before the product did.

> Boring. Also the only thing that matters when something goes wrong.

> AllSquared — regulated escrow for UK project work.

> #escrow #fca #ukbusiness #regulated #allSquared #build #startup #shorts

**Why it works:**
- Title formula: bold + specific
- Visual hook: dusk facade + scaffolding + window glow (pattern interrupt)
- Text overlay: "8 months" (curiosity)
- Description: hook in first line, then value, then tags
- Length: ~320 chars ✓

---

## Update protocol

When YT Shorts algorithm changes — update this doc.