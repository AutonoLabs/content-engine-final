# Rafael's Higgsfield Command Sheet (Yapper)

> The single doc to open before every Higgsfield generation. Roboverse's exact prompt structures, the 5 Higgsfield tools, and copy-paste Yapper examples for each.

**Reference video:** Roboverse, "How to Use Higgsfield AI Better than 99% of People" (Feb 2026, 218k views). His core idea: **don't treat Higgsfield like a generator. Treat it like a production pipeline — image → apps → video → character. Each step feeds the next.**

---

## 🚦 Decision tree — pick your path BEFORE you start

```
What is this post?
│
├── Single image, no person → Path 1: PURE IMAGE
├── Image WITH a recurring brand character → Path 2: SOUL CHARACTER
├── Carousel (4-9 slides) → Path 3: SHOTS APP
├── Outfit change for an existing character → Path 4: OUTFIT SWAP
├── Two images that need to flow together → Path 5: TRANSITIONS
├── Reel / YT Short → Path 6: VIDEO (image-to-video)
├── Cinematic "shot on $200k camera" look → Path 7: CINEMA STUDIO
└── Brand new human character from scratch → Path 8: AI INFLUENCER STUDIO
```

---

## Path 1 — PURE IMAGE (most used)

**When:** Hero shots, social cards, blog images — anything where you want a single strong photo with no recurring character.

**Click:** `Image` at top → pick a model:

| Model | Use for | Yapper case |
|---|---|---|
| **Nano Banana Pro** (Google) | Photorealism, looks-shot-on-camera | Default for ALL hero images. Margaret alone in her chair. The phone booth. The dashboard. |
| **Sea Dream 4.0** | Artistic / stylized / painterly | Brand graphics, lavender-mist mood boards, end-card backgrounds |
| **Sora 2 / Kling 3.0** | Realistic physics, multi-camera (Roboverse preferred these for cinematic video) | Sometimes Nano Banana Pro + sometimes these — see Path 6 |
| **Seedance 2.0** | Newer model, Roboverse's "Seedance 2.0 + Claude" tutorial subject | Hold for next iteration, not first-pass |

**Roboverse's exact prompt structure** (from his Nano Banana Pro example):

> `[Subject + wardrobe + gear] [position/pose] [setting] [lighting] [camera spec]`

His example: *"A female explorer with weathered leather jacket and climbing gear stands at the edge of a massive ice cave. Blue glacial light filtering through translucent walls, our breath visible in the freezing air, dramatic side lighting."*

**Yapper application — hero still for LinkedIn (1:1):**

> `[Subject + wardrobe + setting]` `[pose + action]` `[lighting]` `[camera spec]`
>
> *"Margaret, a 75-year-old woman with shoulder-length silver-gray hair and reading glasses, sits in an ink-plum wingback chair beside a window. She holds a cream-colored vintage rotary telephone receiver close to her ear with both hands, smiling gently. Lavender mist painted wall behind her. A folded cream knit throw on the chair arm. Soft morning side light from the upper left, warm practical lamp glow from the off-camera right. Editorial three-quarter portrait, 35mm lens equivalent, shallow depth of field."*

**Settings to set (Roboverse default):**
- Aspect ratio: **1:1** (LinkedIn, IG feed), **16:9** (X, LinkedIn banner), **4:5** (IG portrait), **9:16** (Reels/YT Shorts still cover)
- Quality: **4K** always when budget allows

---

## Path 2 — SOUL CHARACTER (recurring brand people)

**When:** A specific character (Margaret, Tom, CNA Diane, CNA Marcus, Rebecca, Daniel) needs to appear in multiple posts across weeks/months. THIS is what makes Yapper feel like a brand, not random AI.

**Click:** Two-step process:

### Step A — Build the Soul (do this ONCE per character)

`Soul` → `Create Character` → **upload 20-30 reference photos of the same face from different angles.**

**Roboverse's rule:** *"The more angles you give it, the better it understands what this person looks like from every direction."*

How to generate reference photos for a NEW Soul you don't have real photos of:
1. Go to `Image` → Nano Banana Pro
2. Generate a base character with this exact prompt structure:
   > *"Young male with short dark hair and rugged features, neutral expression, standing against a white background, front facing portrait, natural lighting, photorealistic."*
3. Take that single image to `Apps` → `Shots` → upload → generate
4. Now you have **9 different angles of the same character**
5. Upscale the best 3-5
6. Take those into Shots AGAIN from different moods (smiling, side profile, looking down)
7. Repeat 2-3 more rounds → you have 20-30 photos
8. Upload ALL of them to `Soul` → name the Soul → training takes 3-5 min

**6 Souls we need (built in this order):**

1. **Margaret** (F, 75) — warm woman, silver hair, glasses, lavender-mist cardi
2. **Tom** (M, 78) — silver-white hair, glasses, cardigan over checked shirt
3. **CNA Diane** (F, 50s) — calm, badge, navy scrubs
4. **CNA Marcus** (M, 40s) — friendly, athletic, teal scrubs
5. **Rebecca** (F, late 30s) — phone-in-hand adult daughter
6. **Daniel** (M, late 30s) — adult son, hands busy

### Step B — Use the Soul (every future post)

`Image` → pick your Saved Soul from the character dropdown → write prompt.

**Roboverse's example with a trained character:**
> *"Sam wearing futuristic spacesuit inside a Mars habitat, red planet visible through window, soft interior lighting, confident expression."*

Note: NO face/identity description in the prompt — the Soul carries that. **Just describe scene + wardrobe + lighting + mood.**

**Yapper Soul application — Tom in a reading chair:**
> *"Tom in his reading chair by a window, holding a vintage cream rotary phone, soft afternoon light, gold reading glasses low on his nose, ink-plum cardi over checked shirt, slight amused smile. Warm, quiet, lived-in. Editorial portrait, 35mm, shallow DOF, lavender mist wall."*

---

## Path 3 — SHOTS APP (1 image → 9 angles)

**When:** Carousel needs 4-9 slides. ONE good image becomes 9 usable assets.

**Roboverse's rule:** *"Most people would just regenerate the whole thing from scratch and hope it turns out better. That wastes credits."*

**Click:** `Apps` → `Shots` → upload your single image → `Generate` → wait 30 seconds → 9 unique camera angles.

**Setup sequence:**

1. Generate one strong base image first (Path 1 or Path 2)
2. Open `Apps` tab at top → click `Shots`
3. Upload the image
4. Hit `Generate`
5. ~30 seconds later: 9 angles appear (close-ups, upward framing, overhead, etc.)
6. Pick the 4-6 best
7. Click `Upscale` on each → wait for full-res → download

**Yapper application — Pillar 2 Memory Care carousel (4 slides):**

Generate ONE image: *"Margaret and Tom sitting together on a couch, her hand on his arm, lavender mist room, soft afternoon light."*

Run Shots → pick 4:
- Slide 1: Wide two-shot (the start image)
- Slide 2: Close-up of Margaret's smile
- Slide 3: Close-up of Tom's profile, half-cocked smile
- Slide 4: Close-up of their hands, hers on his arm

**Credit math:** 1 generation + 1 Shots run + 4 upscales = ~5 credits. Vs. 4 separate generations + 4 upscales = ~16 credits. **You just saved 11 credits (70%).**

---

## Path 4 — OUTFIT SWAP (test different clothing on existing character)

**When:** Same Soul needs different wardrobe — morning robe vs evening cardi; fall sweater vs summer linen; bathrobe vs going-out outfit.

**Roboverse's rule:** *"Incredibly useful when you need the same character in scene, but want to test different outfit styles without starting from scratch."*

**Click:** `Apps` → `Outfit Swap` → upload the character image + the outfit reference image → `Generate`.

**Yapper application — Tom across dayparts:**
- Morning: *"Tom in his checked flannel robe, hair slightly tousled, holding a coffee mug, soft morning light"*
- Afternoon: Use Outfit Swap with a cardigan reference → *"Tom in his navy cardigan over checked shirt, glasses, reading a book"*
- Evening: Use Outfit Swap with a knit sweater → *"Tom in a cream knit sweater, reading lamp on, dog-eared novel"*

Same Soul. Three dayparts. Zero identity drift.

---

## Path 5 — TRANSITIONS (cinematic flow between two scenes)

**When:** Two images need to flow into each other cinematically — for Reels, hero video loops, or animated carousel end-cards.

**Roboverse's rule:** *"Upload two different shots and this creates a smooth cinematic transition between them."*

**Click:** `Apps` → `Transitions` → upload image 1 + image 2 → pick transition type:

| Transition type | Use case |
|---|---|
| **Flying cam** | Aerial swoop — best for opening shot |
| **Morph** | Smooth dissolve — best for memory/journey moments |
| **Zoom** | Fast push/pull — best for emphasis |
| **Raven** | Cinematic flythrough (his preferred for sci-fi) |

**Yapper application — Reel scene transition:**

Image 1: Margaret alone in the living room, holding the phone
Image 2: Tom across town, hands on the desk, phone ringing

Transition type: **Morph** — meaning the camera "becomes" the second scene from the first. Best for the "two people connected by one phone call" theme.

---

## Path 6 — VIDEO (image-to-video, the right way)

**When:** Instagram Reel, YouTube Short, LinkedIn video post — anything that moves.

**Roboverse's most important rule:** *"Since I'm using image-to-video, I don't need to describe the character or environment. I only need to describe the action and camera movement."*

**Click:** `Video` at top → pick model:

| Model | When |
|---|---|
| **Kling 3.0** | Realistic physics, multi-camera work, has audio (Roboverse's default) — use for physics-driven scenes |
| **Sora 2** | Cinematic — best for emotional scenes, faces |
| **Google V03.1** | Varied, good fallback |
| **hailuo-2.3** | Fast, cheaper — use for static-camera scenes |

### Setting up a video (Roboverse's exact sequence):

1. **Upload your image** — already generated via Path 1 or Path 2
2. **Pick your model** — Kling 3.0 is the default unless physics don't matter
3. **Write the prompt** — Roboverse's exact structure:

> `Shot 1: [camera] [subject doing what] in [setting]`
> `Shot 2: [camera move] [next action]`
> `Shot 3: [close-up] [specific moment]`
> `Audio: [sound design notes]`

**His Mars example:**
> *"Shot 1 — wide establishing shot of Sam standing in the Mars habitat looking out the window at the red planet. Shot 2 — medium close-up as Sam turns and walks toward the equipment panel. Shot 3 — close-up of Sam's face as he examines the controls with concern. Ambient space station sounds, soft mechanical hums."*

4. **Multi-shot mode: ON** — non-negotiable. Roboverse: *"I'm also breaking this into three distinct shots so we get that professional multi-camera feel."*
5. **Duration:** 10s for multi-shot Reels, 30s for YT Shorts
6. **Resolution: 1080p** for Reels, 4K for YT if budget allows

**Audio rule — Roboverse's:** Kling 3 has audio. *"If you don't tell it what you want, it might add random dialog or weird sounds."* Always specify:
- "Warm piano, single notes, no vocals" (default Yapper)
- "Ambient room tone, no music, no dialog"
- "Soft chime at the end"

**Yapper application — 15s Reel for LinkedIn:**

Image source: Soul "Tom" in the reading chair, holding a cream rotary phone.

> *"Shot 1 — wide establishing shot of Tom in his reading chair, afternoon light on his face. Shot 2 — medium close-up as he lifts the phone receiver to his ear, a small warm smile. Shot 3 — close-up on his weathered hand cradling the receiver. Audio: ambient room tone, soft warm piano single notes at second 8, no dialogue, no narration."*

End card at :13: ink plum background + dial dots + mint accent dot + "yapper.care" wordmark.

### When to use text-to-video instead

**Roboverse's test:** *"It's not as controlled as image-to-video but for quick concepts or when you don't have a specific image in mind, it works."*

For Yapper: ONLY use text-to-video for stock-style B-roll (no Soul character, no recurring brand identity). Example: a "world turning" time-lapse for an awareness post about isolation stats.

---

## Path 7 — CINEMA STUDIO ("shot on $200k camera" look)

**When:** A post needs that "shot on RED Helium with Master Anamorphic lenses" feel. Premium B2B content, founder-voiced posts.

**Click:** From homepage → `Cinema Studio` → pick camera/lens combo → write cinematic prompt.

**Roboverse's exact camera setup example:** *"Full frame cine digital at 35mm gives you that cinematic film quality look."*

Other useful combos:
- Anamorphic 50mm → cinematic letterbox feel
- Cooke S4 32mm → documentary warmth
- Macro 100mm → product detail (use for the rotary phone close-ups)

**Yapper application — founder-voiced hero image:**

> *"Editorial portrait of a mid-40s founder in a quiet office, late afternoon golden-hour light from west-facing windows, layers of books on a shelf behind him, a vintage rotary phone as a desk object in soft focus foreground, warm neutral palette, confident but unhurried expression. Cinema Studio: full-frame cine digital, 35mm Cooke S4 lens equivalent, shallow depth of field."*

### Cinema Studio Video (the "dolly in" trick)

**Roboverse:** *"Now you can add camera movement. I'll select a dolly in to create that pushing effect."*

> *"Camera slowly pushes forward toward the [subject]. [Lighting note]. [Environmental continuity cue]."*

Yapper: *"Camera slowly pushes in toward Margaret's face as she smiles into the phone. Warm window light holds steady. Lavender mist wall stays the same color."*

---

## Path 8 — AI INFLUENCER STUDIO (build a brand-new human from scratch)

**When:** You need a Soul character but have no reference photos, and Seedance/Influencer studio fits the aesthetic.

**Roboverse's walkthrough:**
> *Pick character type → gender → ethnicity → skin tone (color picker) → eye color → skin conditions (freckles, birthmarks, scars — "these small details make an AI influencer feel like an actual person") → age → settings (face, body, style) → render style (hyperrealistic) → hairstyle → Generate.*

**Yapper use:** When we need Tom or CNA Marcus but don't have time to do the full reference-photo training pipeline. AI Influencer Studio gives us a custom Soul in 3 minutes vs. 30+.

**Caveat from Roboverse:** This produces "designable" people, not "real-feeling" people. For dignity-tier senior content, we should still go through the full Soul pipeline (Path 2) for the 6 main characters. Use AI Influencer Studio for short-term cover needs or B-roll extras.

---

## 🎬 The end-card rule (Yapper brand signature)

**Every Reel and YT Short ends the SAME way.** Roboverse doesn't say this — we do. It's our brand signature:

```
[13s into a 15s video, or 28s into a 30s video]
   INK PLUM background
   12 lavender dial dots arranged in a circle
   1 mint accent dot materializes at lower-right
   "yapper.care" wordmark appears below
   Warm chime plays once
   [freeze 1s, fade]
```

Generate the end card ONCE as a static image. Save to `brands/yapper/inbox/brand/end-card-v1.png`. Reuse in every video's tail.

If video doesn't render the end card automatically: cut to the static end card in post.

---

## ⚙️ Operational defaults (lock these in)

| Setting | Default | Why |
|---|---|---|
| Image model | Nano Banana Pro | Best photorealism, Roboverse default |
| Video model | Kling 3.0 | Has audio, multi-shot, realistic physics |
| Aspect 1:1 | LinkedIn, IG feed, FB | Default square |
| Aspect 4:5 | IG portrait | Default portrait |
| Aspect 16:9 | X, LinkedIn banners | Default widescreen |
| Aspect 9:16 | Reels, YT Shorts | Default vertical |
| Quality | 4K images, 1080p video | Cost-efficient |
| Multi-shot video | ON | Roboverse default |
| Audio in Kling 3 | Always specified — never default | Roboverse rule |
| Shots app | ON for any carousel 4+ slides | Saves ~70% credits |
| Outfit Swap | ON for any daypart changes | Saves time + identity drift |
| Transitions | Only when 2+ images need cinematic flow | Don't use for still posts |
| End card | Always present in video | Brand signature |

---

## 📋 Pre-flight checklist (use before each generation)

- [ ] Which Path am I on? (1-8 above)
- [ ] For Souls (Path 2): which Soul character + which scene?
- [ ] For Video (Path 6): did I specify AUDIO?
- [ ] For Video (Path 6): did I enable Multi-shot mode?
- [ ] For Video (Path 6): is the end card in the prompt at :13/:28?
- [ ] For Carousels (Path 3): did I think about Shots app before regenerating?
- [ ] Aspect ratio matches platform?
- [ ] Brand palette cues present (lavender + ink plum + mint)?
- [ ] Does this character match the Soul's established look? (Margaret's hair length, Tom's glasses, etc.)

---

## 🆘 Common mistakes Roboverse calls out

1. **Treating each generation as independent** — generating a new image of "the same character" instead of using a trained Soul. **Fix: always use Soul if you have one.**
2. **Re-generating to fix a small thing** — instead of using the apps (Shots, Outfit Swap, Angles). **Fix: apps > regeneration.**
3. **Blob video prompts** — describing everything in one paragraph. **Fix: structure as Shot 1 / Shot 2 / Shot 3 + Audio.**
4. **Letting Kling add random audio** — Roboverse: "weird sounds." **Fix: always specify audio. "No dialogue" is not enough — describe the room tone.**
5. **Skipping the angle pipeline for Souls** — using only front-facing reference photos. **Fix: 3-4 rounds of Shots from different moods → 20-30 photos → Soul training.**
6. **Going to text-to-video when image-to-video would work** — Roboverse: text-to-video is "not as controlled." **Fix: always start with a generated image, then animate it.**

---

## 🔁 Refresh cadence

This file is the source of truth for Yapper Higgsfield ops. Update when:
- New Soul characters are built → add to Path 2 step B
- A model gets version-bumped (Nano Banana Pro → v2) → update Path 1
- A new app launches in Higgsfield → add as new Path

Last updated: 2026-07-12, from Roboverse video OxNlBqHex44.
