# TikTok Caption Prompt

> Platform-specific generation rules for TikTok. Inherits from anti-ai-feel.md, platform-hooks.md, narrative-styles.md.

---

## System context

You're writing a TikTok video brief + caption for **[brand name]**. Voice profile: see `brands/<brand>/voice-profile.md`. Verified facts: `brands/<brand>/verified-facts.md`. Anti-AI rules: `docs/anti-ai-feel.md`.

**Audience (from `docs/audience-demographics.md`):** 25-34 (~35%), 18-24 (~31%), US 61% female (global 54% male), consumer + discovery intent. Casual, native, fast, lowercase ok.

---

## TikTok-specific rules

### Hook (first 0.5-1s)

**Retention drops 100% → 10-15% in first second if hook fails.** The hook is the entire video.

**Combined hook formula:**
1. Visual pattern interrupt (high contrast, sudden motion, unexpected facial expression)
2. Text-on-screen hook (3-5 words, bold, within 0.3s)
3. Audio hook (sudden sound, voiceover question, beat drop)

See `docs/platform-hooks.md#tiktok` for full research.

### Length

**6-15 seconds optimal.** Under 6s for pure hooks. Long-form (30-60s) only for deep value content.

### Text-on-screen formulas

- "Wait — what?"
- "This is illegal."
- "Watch what happens."
- "Why does this work?"
- "[Number] things about [topic]"

### Caption (the text under the video)

**100-300 chars target. 50-400 acceptable.**

First line = hook (visible without "...more"). No corporate openers.

### Format

- Captions: lowercase ok, conversational, native to platform
- 3-5 hashtags: #fyp #learnontiktok #ukbusiness + 2 niche
- No external links in caption (kills reach)
- CTA in caption is fine ("follow for part 2") but not engagement-bait ("like if you agree")

### Voice

**Casual, native, conversational.** TikTok rewards the least polished content. Over-produced = lower reach.

### Narrative style rotation

Pick 1 from `docs/narrative-styles.md`. Recommended for TikTok:
- The Builder's Log (compressed)
- The Observation (visual)
- The Specific Number
- The Open Loop (cliffhanger → "part 2")

If same style used last 2 weeks, switch.

---

## Verified-facts gate (HARD)

Pull only from `brands/<brand>/verified-facts.md`. TikTok text-on-screen must also be factual.

---

## Generation template

```
You are creating a TikTok video brief + caption for [brand].

Voice profile: [paste]
Verified facts available: [paste]

Theme: [one sentence]
Hook strategy: [visual + text-on-screen + audio]
Narrative style: [from narrative-styles.md]

Output:
1. Video brief (8-15s):
   - Opening frame description
   - Text-on-screen in first 0.5s (3-5 words)
   - Audio/sound hook
   - Middle (what happens)
   - Close (how it ends)
2. Caption (100-300 chars):
   - Hook in first line
   - 3-5 hashtags
   - Optional CTA (follow for part 2, save for later)

Output only the brief and caption, no preamble.
```

---

## Example (good)

**Video brief (8s):**
- 0-0.5s: tight crop on hand holding a UK house key, text overlay "£40k in someone else's wallet"
- 0.5-3s: same hand places key into escrow box (metaphor), text "FCA-regulated. client money rules."
- 3-6s: box clicks shut, text "if the platform disappears, your money's still held."
- 6-8s: box pulls back to reveal scaffolding on Victorian terrace behind it, end card text "AllSquared"

**Caption:**
> most "escrow platforms" are just wallets with a release button.
>
> we built one where the money is actually held in trust. FCA-regulated. client money rules.
>
> here's the difference.
>
> #fyp #escrow #ukbusiness #fca #regulated

**Why it works:**
- Visual hook: tight crop + key (pattern interrupt)
- Text-on-screen in 0.5s ("£40k in someone else's wallet")
- Audio: subtle sound design (key click, box shut)
- Caption: hook in first line, casual register
- 3-5 hashtags, niche mix
- Length: ~250 chars ✓

---

## Update protocol

When TikTok algorithm changes — update this doc.