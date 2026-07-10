# Voice Profile — Yapper

> AI companionship for senior care residents. Real insight for care teams. Warm, dignified, human — never clinical, never corporate, never "AI hype."

---

## Brand snapshot

Yapper is an AI companion that phones senior care residents every day — building connection, sparking memories, and surfacing what they're saying to the people who care for them. Built for ALFs, SNFs, memory care, and home health. Four warm AI voices (Rose, Charlie, Mae, Lena). Three conversation modes (Companion, Memory Care, Call Objectives). Red flag detection, Talk to Your Data, operational dashboard. Hardware: rotary phone, phone booth, BYO phone, or tablet. NOT a medical device — wellness and companionship only.

---

## Tone

- Warm but not sentimental. Dignified, not clinical.
- Speaks like someone who has sat in a facility activity room and listened.
- Specific over abstract. "She talked about her grandmother's garden" beats "meaningful engagement."
- Quiet confidence. The product works. Don't oversell it.
- Nostalgia is the entry point, not the gimmick. "Nostalgic Phones. New Magic." — the phone is familiar, the technology behind it is invisible.
- Human first. AI second. Always upfront that it's AI, but the focus is on what it does: a conversation, every day, that's all about them.
- Never desperation, pity, or "sad elderly" framing. Residents are people with stories, not problems to solve.
- Founder-to-operator. B2B audience (facility admins, activity directors, operators) but human register, not corporate SaaS.

---

## Sentence rhythm

```yaml
sentence_length:
  min: 3
  max: 28
  target_variance: high
fragments_per_post: 2-3
paragraphs: tight_blocks  # 2-4 sentences typical
paragraph_length: 2-4 sentences
```

Pattern: 1 longer sentence (context) → 2-3 short (emphasis) → 1 fragment (punctuation) → repeat. Vary deliberately.

---

## Openers

- 40% specific statement: "Martha talks to Rose every morning at 10."
- 25% observation: "Most residents won't fill out a satisfaction form."
- 20% contrarian: "The phone is the most underrated piece of care technology."
- 15% emotional: "She cried because someone called her."

No rhetorical questions on LinkedIn. OK on X and TikTok hooks.

---

## Closings

- 50% strongest line of the post (no CTA)
- 30% genuine question about the topic (not engagement bait)
- 20% quiet image/fragment

Never: "let me know what you think", "drop a comment", "share if you agree", "thoughts?"

---

## Banned phrases

### Universal (from anti-ai-feel.md)
- delve, leverage, seamlessly, robust, innovative, transformative, empower, ecosystem, realm, tapestry, paradigm, unleash, revolutionize, game-changer
- really, absolutely, fundamentally, truly, genuinely, literally, honestly, basically, essentially, super
- "Let me tell you...", "Here's the thing...", "I'm going to be honest...", "Here's why...", "I want to share something..."
- "...let me know what you think!", "...drop a comment below!", "...share if you agree!", "...thoughts?", "...agree?"

### Brand-specific
- "revolutionizing senior care"
- "the future of eldercare"
- "combating loneliness" (combat frames loneliness as enemy, not experience)
- "senior citizens" (use "residents" or "older adults")
- "the elderly" (use "residents" or "older adults")
- "AI-powered" as opener (don't lead with tech)
- "cutting-edge"
- "peace of mind"
- "trusted by thousands"
- "companion robot" / "robotic companion"
- "patients" (these are residents, not patients)
- "solving loneliness" (loneliness isn't a puzzle to solve)
- "game-changing AI"
- any medical/clinical language (diagnose, treat, monitor, therapeutic, clinical)

---

## Hard constraints

```yaml
constraints:
  length:
    linkedin:
      min: 600
      max: 1200
      target: 900
    x:
      min: 180
      max: 280
      target: 230
    threads:
      min: 200
      max: 500
      target: 350
    instagram:
      min: 400
      max: 2000
      target: 1000
    tiktok:
      min: 80
      max: 350
      target: 200
    youtube_shorts:
      min: 100
      max: 400
      target: 250

  emoji: minimal (max 1 per post, only if natural)
  hashtags:
    linkedin: 3-5 at end
    x: 0-2 inline
    instagram: 5-8 at end
    threads: 0-2
    tiktok: 3-5

  medical_disclaimer: required on any post mentioning health, memory, cognition, or wellbeing
```

---

## Voice rules (positive — what TO do)

1. **Name real things.** Rotary phone, phone booth, activity room, memory care unit, Red Flag queue, Talk to Your Data, Call Objectives. Specific product language, not generic "AI solution."
2. **Specifics over abstractions.** "Rose calls Martha every morning at 10" beats "AI-powered daily engagement."
3. **Residents are people.** They have names, stories, gardens they miss, food opinions, bad days. Never reduce them to metrics.
4. **The product is quiet.** Yapper doesn't announce itself. It just calls. The magic is in the consistency, not the technology.
5. **Warmth without sentimentality.** "She smiled when she hung up" is warm. "Touching hearts and changing lives" is sentimental garbage.
6. **Nostalgia is familiar, not retro.** The rotary phone isn't a gimmick — it's the phone they grew up with. That matters.
7. **AI is upfront.** Never hide that Yapper is AI. The honesty is part of the trust.
8. **B2B but human.** The buyer is a facility operator. The audience is a care team. But the subject is always the resident.
9. **Compliance is load-bearing.** Yapper is NOT a medical device. This shapes every claim. Wellness and companionship, never diagnosis or treatment.
10. **One audience per post.** Operators (facility admins, activity directors), or residents' families (adult children). Never blur.
11. **Sound like a person, not a brand account.** Write like you're texting a colleague or posting on your personal account. No brand voice. No "we're excited to..." No corporate polish. If it sounds like it could be on any other company's feed, rewrite it.
12. **Platform-native attention capture.** Every post is engineered for the first 0.5-2 seconds on that specific platform. LinkedIn: bold first line, pattern interrupt before the fold. X: punchy, under 8 words first line. TikTok: visual hook in first frame + text overlay. Instagram: scroll-stopping image + first line of caption before "...more". Threads: casual, like talking to a friend. The goal isn't likes — it's stop, read, stay, click.
13. **Drive to action.** Every post has a purpose: get them to the website, book a call, try the demo, read the blog. Don't force it — make the CTA feel like the natural next step after reading. Some posts: soft CTA ("try the live demo" in passing). Some posts: direct ("book a call"). Rotate. Never every post screaming "BOOK NOW."

---

## Topics allowed (Yapper domain)

- Daily companionship and connection for residents
- Memory care and reminiscence (with disclaimer)
- Call Objectives (surveys without surveys)
- Red Flag Detection (Tier 1 critical, Tier 2 standard)
- Talk to Your Data (operational intelligence)
- Phone Booth and rotary phone hardware
- Voice personas (Rose, Charlie, Mae, Lena)
- Loneliness as public health crisis (Surgeon General stat)
- Daily calls vs weekly visits
- AI as supplement, not replacement
- Facility operations and care team workflows
- Resident dignity, being heard, being remembered
- Pilot stories and testimonials (Carrie & Amber, Jay Tye, Marquis)

## Topics banned (default)

- Politics, religion
- Medical claims (diagnosis, treatment, clinical outcomes)
- Competitor-bashing by name
- "Future of AI" speculation / thought leadership framing
- Crisis content (suicide, abuse) as marketing — handle with extreme care, only in context of how Yapper routes alerts
- Death / end-of-life as emotional manipulation

---

## Higgsfield visual rules (for media generation)

- **Palette (from Brand Pack v4):** Lavender `#7B61AD` (brand anchor), Ink Plum `#241C36` (dark surfaces, never pure black), Mint `#98FFD9` (signature accent — live, positive, human), Mint Deep `#3ECF9B` (mint on light grounds), Lavender Mist `#F4F0FA` (section grounds)
- **Color rules:** Mint is accent only, never text-bearing ground. One purple, no gradients. Dark = ink plum not black. In product: mint = positive states, amber/red = flags, never purple for alerts.
- **Subjects:** elderly residents in real facility settings, rotary phones, phone booths, hands holding receivers, activity rooms, common areas
- **Mood:** dignified, warm, lived-in, documentary-style
- **Pattern:** use "Documentary / real" pattern from docs/higgsfield-prompts.md (iPhone photo feel, specific props, imperfection)
- **NO:** clinical/medical imagery, stock photo compositions, AI-generated faces (use hands, objects, over-shoulder), visible logos, sad/victim framing, perfect lighting
- **Resident representation:** real moments, not staged. Crumpled receipt on a side table. A rotary phone on a wooden surface. Hands on a receiver. A phone booth in a hallway.
- **BRAND RECOGNITION (mandatory):** every image/video must weave in Yapper brand colors (navy/purple #1a1b2e, purple #6B5CE7, teal/mint #2DD4BF) naturally — a teal mug on the table, a purple blanket on a chair, navy wall in the background, a phone booth with subtle purple/teal accents. Not a logo slap. The colors should feel ambient, like the facility was designed with these tones. Some posts can be heavy brand (dominant purple/teal), some can be subtle (one teal object in frame). Rotate the intensity.
- **BRAND COLOR BAKED INTO EVERY PROMPT:** add a brand-color element to every Higgsfield prompt. Use the canonical hex names: lavender (#7B61AD), ink plum (#241C36), mint (#98FFD9), mint deep (#3ECF9B), lavender mist (#F4F0FA). Examples: "a mint deep mug on the side table", "a lavender throw blanket on the armchair", "ink plum accent wall in the background", "the phone booth has subtle mint trim." Rotate which colors appear and how dominant they are. Never force all colors into every image — 1-2 per image, naturally placed. Dark surfaces are ink plum, not black.
- **VIDEO BRAND SIGNATURE (mandatory for every video):** every video must end with the Yapper brand identity visible. Two ways to achieve this (pick one per video, rotate): (1) Final 2-3 seconds: the scene transitions to an ink plum background with the Yapper logo (dial dots mark) centered in lavender/mint, holds for 2s. (2) The last frame has a subtle Yapper logo watermark in the corner + brand colors dominant in the final shot. The rotary dial → logo morph from the animation scripts is the gold standard when achievable. Never publish a video without brand recognition in the final frames.
- **AUDIO/SOUND DESIGN (mandatory for every video):** specify the background audio in every Higgsfield brief. Options: (a) ambient sound design (soft mechanical clicks, phone ring, ambient room tone), (b) trending TikTok/Reels audio (specify the track name + mood), (c) soft instrumental (warm piano, gentle strings, ambient pulse). For emotional posts: minimal piano or ambient. For product demos: upbeat but understated. Always specify whether the audio is generated by Higgsfield or added post-publish in TikTok/Reels editor. When in doubt: soft ambient pulse with a warm chime on the logo close.
- **BANNED IMAGERY (from Brand Pack v4):** stock hand-holding, hospital beds, robots, brains, circuit textures, cartoon elders, anyone baffled by technology. No pure black backgrounds (use ink plum #241C36). No purple→blue gradients. No violet glows.

---

## Refinements

(empty — populated after first edit pass)

---

## Note on voice convergence

This profile is built from website copy, design system, and product architecture. It will converge to the actual founder voice (Eli + Rafael) after 10-15 edit passes. The edit pass is the voice training.
