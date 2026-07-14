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
- 15% emotional: "She stayed on the line because the conversation felt familiar."

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

## Working ranges and hard constraints

These are starting hypotheses for testing, not universal algorithm rules. The platform playbook in `research/cross-platform-attention-playbook.md` controls format-specific decisions.

```yaml
working_ranges:
  linkedin:
    image_caption: 300-700 characters
    short_video_caption: 150-450 characters
    founder_or_operator_insight: 600-1200 characters when earned
  x:
    single_post: 70-220 characters preferred; never exceed platform limit
  threads:
    conversation_start: 80-300 characters
  instagram:
    reel_caption: 1-5 short lines; video must stand alone
    carousel_caption: 150-500 characters to begin testing
  tiktok:
    caption: one concise context line plus one answerable question
  youtube_shorts:
    title_and_description: clear, concise, and secondary to the video story

constraints:
  emoji: minimal (max 1 per post, only if natural)
  hashtags:
    linkedin: 1-3 focused tags at end
    x: 0-2
    instagram: relevant and restrained; no tag stuffing
    threads: one relevant Topic Tag where available
    tiktok: relevant discovery tags only
    youtube_shorts: relevant niche tags only
  medical_disclaimer: required on any post mentioning health, memory, cognition, or wellbeing
  calendar_media: required on every post except ordinary Reddit comments
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
12. **Platform-native attention capture.** Treat “0.1 second” as a design mindset, not a universal metric: the first frame and first visible line must be understood instantly at mobile size. Adapt the same idea natively rather than copying one caption everywhere. Use `research/cross-platform-attention-playbook.md` for platform-specific hooks, pacing, interaction, and measurement.
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

- **Palette (from Brand Pack v4):** Lavender `#7B61AD` (brand anchor), Lavender 700 `#4E3E71` (depth/hover), Ink Plum `#241C36` (dark surfaces, never pure black), Mint `#98FFD9` (signature accent), Mint Deep `#3ECF9B` (accessible mint on light grounds), Lavender Mist `#F4F0FA` (light grounds)
- **Color rules:** Mint is accent only, never text-bearing ground. One purple, no gradients. Dark = ink plum not black. In product: mint = positive states, amber/red = flags, never purple for alerts.
- **Subjects:** older residents in real facility or home settings, rotary phones, phone booths, hands holding receivers, activity rooms, common areas
- **Mood:** dignified, warm, lived-in, documentary-style
- **Pattern:** use "Documentary / real" pattern from docs/higgsfield-prompts.md (iPhone photo feel, specific props, imperfection)
- **NO:** clinical/medical imagery, stock compositions, generic or inconsistent AI faces, fake/generated logos, sad/victim framing, or perfect studio lighting. Use approved trained Souls for recurring people; apply the authentic Yapper wordmark after generation.
- **Resident representation:** real moments, not staged. Crumpled receipt on a side table. A rotary phone on a wooden surface. Hands on a receiver. A phone booth in a hallway.
- **BRAND RECOGNITION (mandatory):** every image/video must weave in 1-2 canonical v4 colors naturally—such as a mint deep mug, lavender throw, ink plum cardigan, or lavender mist wall. Never use the obsolete navy/bright-purple/teal palette. Rotate intensity; do not force every color into every scene.
- **BRAND COLOR BAKED INTO EVERY PROMPT:** add a brand-color element to every Higgsfield prompt. Use the canonical hex names: lavender (#7B61AD), lavender 700 (#4E3E71, depth only), ink plum (#241C36), mint (#98FFD9), mint deep (#3ECF9B), lavender mist (#F4F0FA). Examples: "a mint deep mug on the side table", "a lavender throw blanket on the armchair", "ink plum accent wall in the background", "the phone booth has subtle mint trim." Rotate which colors appear and how dominant they are. Never force all colors into every image — 1-2 per image, naturally placed. Dark surfaces are ink plum, not black.
- **VIDEO BRAND SIGNATURE (mandatory for every video):** every video must end with the authentic Yapper identity visible. Preferred close: the scene transitions to ink plum, then the official ten-dot lavender 270-degree rotary arc and mint finger stop appear with the authentic Yapper wordmark and hold for two seconds. A subtle authentic corner lockup is acceptable when the full end card is not possible. Never use a generated approximation of the logo or publish a video without recognizable Yapper identity in the final frames.
- **AUDIO/SOUND DESIGN (mandatory for every video):** specify the background audio in every Higgsfield brief. Options: (a) ambient sound design (soft mechanical clicks, phone ring, ambient room tone), (b) trending TikTok/Reels audio (specify the track name + mood), (c) soft instrumental (warm piano, gentle strings, ambient pulse). For emotional posts: minimal piano or ambient. For product demos: upbeat but understated. Always specify whether the audio is generated by Higgsfield or added post-publish in TikTok/Reels editor. When in doubt: soft ambient pulse with a warm chime on the logo close.
- **BANNED IMAGERY (from Brand Pack v4):** stock hand-holding, hospital beds, robots, brains, circuit textures, cartoon elders, anyone baffled by technology. No pure black backgrounds (use ink plum #241C36). No purple→blue gradients. No violet glows.

---

## Refinements

(empty — populated after first edit pass)

---

## Note on voice convergence

This profile is built from website copy, design system, and product architecture. It will converge to the actual founder voice (Eli + Rafael) after 10-15 edit passes. The edit pass is the voice training.
