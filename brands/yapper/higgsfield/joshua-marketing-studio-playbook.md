# Yapper Marketing Studio Playbook (Joshua Mayo, adapted)

> Translation of Joshua Mayo's "$100k AI Ads with Higgsfield" video (itv4Xljkbqw, May 2026, 15k views) for Yapper. Joshua sells mascara on Amazon — we don't. **His framework is direct-to-camera sales energy. Yapper is dignity-tier senior care.** We translate the structure, replace the energy with ours.

**Joshua's core insight:** Marketing Studio is a **production pipeline**, not a generator. Two inputs — a product link (or asset reference) + an avatar (or Soul) — and one prompt = a $100k-style ad. Same prompt, different avatar = multiple ad variations. Splice different ad formats together = full marketing sequences.

**Yapper's translation:** Senior care doesn't sell on Amazon, but we DO have:
- A "product" (Yapper — the daily phone call)
- An "audience" (operators + adult-children + residents themselves)
- A need for **multiple avatar variations** (we already have 6 Souls queued: Margaret, Tom, Diane, Marcus, Rebecca, Daniel)
- A need for **multiple ad formats** (UGC, unboxing-style, tutorial, TV spot) for the same product
- A need for **spliced sequences** (hook + explanation + testimonial + CTA)

Joshua's framework is **exactly** what we need.

---

## 🎯 Joshua's 4 Marketing Studio formats — Yapper equivalents

### 1. TV SPOT — cinematic, premium

**Joshua uses it for:** Brand hero videos, looks like a Super Bowl ad.

**Yapper translates to:** The **Brand Anthem** format. The 30-second "what Yapper is" video. The one that goes on the homepage hero and the LinkedIn banner.

**Joshua's prompt structure (from his TV spot example):**
> Scene 1 (hook), Scene 2 (problem), Scene 3 (product reveals), Scene 4 (benefit), Scene 5 (CTA)

**Yapper's TV Spot template — "Yapper Anthem" (30s):**

| Second | Beat | Prompt content |
|---|---|---|
| 0-5 | Hook | Empty chair. Morning light. Phone on the table. No person. |
| 5-12 | Problem | Hands lift the receiver. A face we can't quite see yet. Soft inhale. |
| 12-18 | Product | The voice (no source) begins speaking. The hand on the receiver relaxes. |
| 18-25 | Benefit | Camera pulls back — we see it's a senior in their living room, smiling. |
| 25-30 | End card | Ink plum + dial dots + mint accent + yapper.care |

**Generative spec:**
- Higgsfield Marketing Studio → TV spot format
- Avatars: 2 Souls (one for the operator angle, one for the family angle — splice both)
- Aspect: 16:9 for homepage, 9:16 for Reels/YT Shorts, 1:1 for LinkedIn
- Audio: warm piano single notes, soft chime on end, ambient room tone only — **NEVER sales-y music bed**

**Joshua's rule we adopt:** *"This is where you describe what actually happens within the ad."* — Joshua uses Claude to write the prompt, we use it for our TV spots too. Use `brands/yapper/inbox/templates/claude-tvspot-prompt.txt`.

### 2. UGC — natural, on-platform, native

**Joshua uses it for:** TikTok/Reels ads. "Hi I'm a real person who tested this and here's what I think." Direct-to-camera. Authentic energy.

**Yapper translates to:** **The Adult-Child + Family POV.** Rebecca or Daniel on camera, phone in hand, telling the audience what changed for their parent. Authentic, considered, NOT sales-y.

**Joshua's prompt structure:**
> "Write me a short UGC style ad for [product], something that feels natural like a TikTok video."
> Then he tweaks. He specifies avatar, lighting, framing, etc.

**Yapper UGC template — "Rebecca's morning" (15-30s):**

| Second | Beat | What Rebecca does |
|---|---|---|
| 0-3 | Hook | Rebecca in her kitchen, looking at phone, slight tension |
| 3-10 | Context | "I work full-time. I have a kid. Mom's not answering when I call." |
| 10-18 | Product | "Three weeks ago she started getting a daily call. Now she picks up." |
| 18-25 | Reaction | Real-feeling smile. Cut to: photo of her mom, holding the phone, smiling. |
| 25-30 | CTA | "yapper.care." |

**Generative spec:**
- Higgsfield Marketing Studio → UGC format
- Avatar: **Soul: Rebecca** (or Daniel — alternate for sister-post dynamic)
- Aspect: 9:16 native to TikTok/Reels
- Audio: ambient kitchen morning, no music — Joshua's UGCs use ambient only
- LIP SYNC: Marketing Studio supports it. Use Rebecca's voice profile from training.

**Joshua's exact rule we copy:** *"You could create one version where someone is testing the product. Another version where somebody is drawing something. Another version where somebody is reacting to the colors."* For Yapper: generate **3 versions of the same Rebecca UGC** with slight prompt variations:
- v1: kitchen morning (anxious → relieved)
- v2: parked car after work (guilty → reassured)
- v3: walking the dog (rushed → calmer)

**Test all 3 on Reels with $5 spend each.** The winner becomes the template for the next 4 weeks.

### 3. UNBOXING — first-impression content

**Joshua uses it for:** Showing what comes in the package. His unboxing ad has the avatar opening the box, examining contents.

**Yapper translates to:** **"First call" content.** The moment a resident receives their first Yapper call. What that looks like. What's on the other end of the line.

**Joshua's unboxing structure:**
> Avatar opens package → shows items → comments on quality → first impressions

**Yapper unboxing template — "Tom's first call" (20s):**

| Second | Beat | Prompt content |
|---|---|---|
| 0-3 | Setup | Tom at his kitchen table, phone in front of him. He looks at it. |
| 3-8 | The ring | Phone rings. Tom reaches slowly, picks up the receiver. |
| 8-14 | The voice | We hear warm voice (no source, just suggestion). Tom's face relaxes. |
| 14-18 | Reaction | Soft smile. His shoulders drop. He's listening, present. |
| 18-20 | End card | Ink plum + dial dots + mint accent + yapper.care |

**Generative spec:**
- Higgsfield Marketing Studio → unboxing format
- Avatar: **Soul: Tom** (or alternate Margaret, Marcus depending on scene)
- Aspect: 9:16 for Reels, 1:1 for LinkedIn
- Audio: the dial tone of the cream rotary (we have this as a brand asset), warm voice (no actual words — just presence), soft chime

### 4. TUTORIAL — how-to content

**Joshua uses it for:** Showing how the product works. His blender tutorial has the avatar step through assembly, settings, use.

**Yapper translates to:** **"How Yapper works" content.** Family-facing B2C — for the adult-child who's just learned about Yapper and wants the 60-second version.

**Joshua's tutorial structure:**
> Step 1 (setup), Step 2 (first use), Step 3 (key feature), Step 4 (result)

**Yapper tutorial template — "How it works" (45s, LinkedIn carousel companion or 45s Reel):**

| Second | Beat | Prompt content |
|---|---|---|
| 0-8 | Setup | Hands opening the Yapper welcome box (we don't have one — substitute: hands wrapping a cream rotary phone in tissue paper). Soft moment. |
| 8-18 | Step 1 | A phone call: close-up of receiver being lifted. |
| 18-28 | Step 2 | Cut to dashboard: a mood-trend sparkline rising over 30 days. |
| 28-38 | Step 3 | Cut back: a CNA at a workstation glancing at the same dashboard, smiling. |
| 38-45 | End card | Ink plum + dial dots + mint accent + yapper.care |

**Generative spec:**
- Higgsfield Marketing Studio → tutorial format
- Avatars: 2 Souls (Rebecca + Marcus — sibling/operator dynamic)
- Aspect: 9:16 for Reels, 16:9 for LinkedIn, 4:5 for IG
- Audio: ambient room tone, soft piano single notes at step transitions

---

## 🔄 Joshua's "Multiple variations with different avatars" rule

**Joshua:** *"You could create one version where someone is testing the markers with one avatar. Another version where somebody is drawing. Another version where somebody is reacting to the colors. And very quickly, we can build out multiple variations of that same product."*

**For Yapper:**

Same scene, three Souls, three completely different emotional reads:

| Scene | Soul 1 | Soul 2 | Soul 3 |
|---|---|---|---|
| Picking up the phone | Margaret (relief) | Tom (memory) | Daniel (son's POV) |
| After the call ends | Margaret (calm) | Tom (smiling) | Rebecca (relieved) |
| Showing the dashboard | CNA Diane | CNA Marcus | (none, UI shot) |

We don't make these separately. We make the **base scene once** and run it 3 times with different Soul selected. Same prompt, different avatar.

**Cost efficiency:** 1 base generation + 3 Soul variants = 4 outputs for the price of ~2. Roboverse's "use the apps, not regenerate" rule, applied at the marketing level.

---

## 🧩 Joshua's "splice clips into full sequences" rule

**Joshua:** *"You could start the video with 5-10 seconds of avatar unboxing the product, then transition into a second ad using that same product and the same avatar, but this time in a tutorial-style format. Then take these two clips and splice them together in any editing software, and you end up with something that looks like this."*

**For Yapper — the "First call" sequence (60s, LinkedIn video or IG carousel):**

| Clip | Source format | Length | Purpose |
|---|---|---|---|
| 1 | Unboxing | 0-10s | Hook — Tom sees the phone |
| 2 | TV Spot | 10-25s | The call begins, voice speaks |
| 3 | UGC (Rebecca) | 25-40s | "Three weeks ago my dad started getting a daily call..." |
| 4 | Tutorial (dashboard) | 40-55s | What the operator sees |
| 5 | End card | 55-60s | yapper.care |

**Splice together in iMovie / CapCut / DaVinci Resolve.** This is **one** LinkedIn carousel / video ad that took ~5 separate Marketing Studio generations to build but feels like a single $50k production.

**Yapper rule:** Every pillar gets one **"splice sequence"** version per month. P1 B2B: founder + dashboard + testimonial. P6 Family Ed: Rebecca + Tom + end card. P7 Proof: Marcus + Marquis signage + end card.

---

## 🤖 Joshua's Claude AI workflow (we adopt this)

**Joshua's rule:** *"Instead of trying to come up with everything from scratch yourself, I'm going to use Claude AI to help me build out a prompt for this ad."*

He pastes the product link, gives Claude a simple instruction, gets a starting point, then **tweaks** so it sounds how he wants.

**Yapper Claude prompts (saved to inbox/templates):**

### `claude-tvspot-prompt.txt`
```
Write a 30-second TV spot script for Yapper (yapper.care — daily AI phone calls for senior care residents).

Format:
- Scene 1 (0-5s): Hook — visual silence, anticipation
- Scene 2 (5-12s): Problem — the absence of regular contact
- Scene 3 (12-18s): Product — the call begins
- Scene 4 (18-25s): Benefit — the person reacts
- Scene 5 (25-30s): End card — yapper.care

Tone: dignified, warm, never sales-y, never clinical, never AI-hype.
Brand: cream rotary phones, lavender + ink plum + mint palette.
Audience: senior living operators + adult children of aging parents.
Reference: this is the brand's flagship brand-anthem video, not a feature ad.

Include specific visual + audio cues per scene.
```

### `claude-ugc-prompt.txt`
```
Write a 20-30 second UGC script for [Soul: Rebecca | Soul: Daniel | etc] speaking directly to camera about Yapper (yapper.care — daily AI phone calls for senior care residents).

Tone: authentic, on-the-go, adult-child perspective. Not a sales pitch. A confession.
Pattern: opening hook + middle context + product reveal + soft reaction + soft CTA.
Constraint: NO hype words ("amazing", "incredible", "revolutionary"). NO clinical claims. NO medical-device claims.
Brand voice: sentence case, sourced claims only, dignity-first.
Output: scene-by-scene with visual + dialogue cues.
```

### `claude-tutorial-prompt.txt`
```
Write a 45-second tutorial script for Yapper (yapper.care — daily AI phone calls for senior care residents).

Audience: adult children considering Yapper for an aging parent. They've just discovered us. They want the 60-second explainer.

Steps to cover:
1. What Yapper is (one sentence)
2. How the resident experiences it (the phone call)
3. What the operator/family sees (the dashboard)
4. What changes over time (the outcomes)

Tone: clear, warm, no jargon. NOT clinical. NOT sales-y. NOT AI hype.
Output: scene-by-scene with visuals, voice-over (if any), and audio cues.
```

---

## 📊 Joshua's monetization playbook (we ignore this part)

Joshua monetizes by selling AI ad services to small businesses. We don't. We use his **production framework** (Marketing Studio + Claude + spliced clips), not his business model. **Yapper's business model is B2B SaaS subscriptions to senior living operators + DTC family plans.** The marketing is in service of that.

---

## 🆘 Joshua's mistakes to avoid

1. **Don't be sales-y in the UGC scripts.** Joshua's UGCs are sales-y by nature ("Links in my bio", "this is amazing"). Yapper's UGC must be **confessional, not pitchy**. Rebecca talking like a daughter, not a creator with affiliate links.

2. **Don't use stock music beds.** Joshua's ads have background music. Yapper's brand audio is **ambient + single piano notes + soft chime**. Music beds cheapen the dignity-tier positioning.

3. **Don't splice product into scenes that don't have it.** Joshua's UGC places the product (markers) in every frame. Yapper shouldn't put a Yapper-branded box into a senior's living room — the product is **invisible** in the resident experience, which is the point.

4. **Don't use lip-sync if the audio is a voice prompt.** Joshua uses lip-sync because his UGC has scripted dialogue. Yapper's TV spots and unboxing clips should have NO dialogue — just ambient and piano. Only the tutorial and Rebecca UGC use dialogue (and only with lip-sync on, not auto-captioning).

5. **Don't skip the "tweak the Claude output" step.** Joshua: *"I don't necessarily want to just copy this exactly as is."* Yapper Claude outputs need human voice-tuning. The Claude template is a starting point, not the final.

---

## 🔗 How this fits with Roboverse (the previous video)

| Joshua's contribution | Roboverse's contribution | Together for Yapper |
|---|---|---|
| Marketing Studio = production pipeline | Higgsfield = production pipeline | Marketing Studio is the "TV spot" path inside our 8-path framework |
| 4 ad formats (TV/UGC/Unboxing/Tutorial) | 8 tool paths | Use Joshua's 4 formats AS 4 distinct paths (9, 10, 11, 12) in our framework |
| Multiple avatar variations = A/B testing | Soul ID = consistent character | Test 3 Soul variants of the same UGC, then promote winner to monthly template |
| Splice clips into sequences | Transitions app + Kling video | Splice is at the marketing level; Kling is at the asset level |
| Claude writes the prompt | Manual prompt structures | Claude is the prompt-writer for ad-format paths; manual is for image paths |
| "Regenerate until it's right" | "Use the apps, not regenerate" | Compromise: 3 regen attempts max, then switch tools |

**Joshua gave us Marketing Studio as a tool. Roboverse gave us the toolset. Together = full production pipeline.**

---

## 🎬 Yapper's 12-path framework (UPDATED)

| Path | Tool | Yapper use case |
|---|---|---|
| 1 | Pure Image (Nano Banana Pro) | Hero stills, B-roll, single posts |
| 2 | Soul Character | Recurring brand people (Margaret, Tom, etc.) |
| 3 | Shots App | Every 4+ slide carousel — saves 70% credits |
| 4 | Outfit Swap | Same Soul, different daypart |
| 5 | Transitions App | Two Souls in one cinematic scene |
| 6 | Video (Kling 3.0) | Reels, YT Shorts (image-to-video, multi-shot ON) |
| 7 | Cinema Studio | Founder-grade B2B (Cooke S4 / full-frame cine) |
| 8 | AI Influencer Studio | Expedience / B-roll extras |
| **9** | **Marketing Studio: TV Spot** | **Brand Anthem — flagship 30s** |
| **10** | **Marketing Studio: UGC** | **Adult-child POV — authentic confessional** |
| **11** | **Marketing Studio: Unboxing** | **"First call" content — what the resident experiences** |
| **12** | **Marketing Studio: Tutorial** | **"How it works" content — family explainer** |

This replaces the previous 8-path framework in `rafael-command-sheet.md`.

---

## 📋 What changes in Sheet 11 (TOOL-ASSIGN)

Existing assignments stay. New opportunities open up:

- **Pillar 1 B2B Thought Leadership** → add Marketing Studio TV Spot option for flagship weeks
- **Pillar 6 Family Education** → Marketing Studio UGC is the new primary (Soul: Rebecca)
- **Pillar 3 Feature Spotlights** → Marketing Studio Tutorial for "How it works" weeks
- **Pillar 5 Walkthroughs** → Marketing Studio Unboxing for "first call" weeks

I will reassign specific posts to Marketing Studio paths when we hit those weeks, and update Sheet 11 then. No retroactive churn.

---

## ⚠️ Final note — Joshua's affiliate disclaimer applies to Yapper too

Joshua: *"This video may contain affiliate links."* Yapper's content must never imply medical claims, never feel like sponsored content, never use affiliate-style CTAs ("links in bio", "buy now", "code YAPPER20"). The brand voice is warm, dignified, operator-grade. We use Joshua's **framework**, not his **energy**.

Last updated: 2026-07-13, from Joshua Mayo video itv4Xljkbqw.