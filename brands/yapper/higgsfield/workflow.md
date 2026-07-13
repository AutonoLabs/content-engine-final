# Higgsfield Workflow — Roboverse Method (ingested 2026-07-12)

**Source:** https://www.youtube.com/watch?v=OxNlBqHex44
**Channel:** Roboverse
**Title:** "How to Use Higgsfield AI Better than 99% of People"
**Published:** 2026-02-28
**Length:** 11:03
**Views:** 218,655+
**Category:** Education
**Author skill level:** operator-creator, production-pipeline mindset
**Yapper-relevant?** YES — multiple workflows apply directly to senior-care + AI-phone content

---

## Core thesis (Roboverse)

Most people use Higgsfield like a basic generator and waste credits. The platform is a **controlled production pipeline** — models, character training, video prompts, and camera simulation are **one system**. Treating them as separate features is the mistake.

**Implication for Yapper:** We need a production pipeline, not one-off generations. Every piece of media is part of a coherent visual brand world.

---

## The 4-stage pipeline (Roboverse's actual method)

### 1. IMAGE (foundation)
**Pick the model by job-to-be-done:**

| Goal | Model | Yapper use case |
|---|---|---|
| Photorealism (looks-shot-on-a-camera) | **Nano Banana Pro** (Google) | Hero images — rotary phone, cozy reading nook, terminal-on-residents — default for stills |
| Artistic / stylized | **Sea Dream 4.0** | Brand graphics, abstract campaign visuals (lavender mist) |
| Character consistency | **Higgsfield Soul** | Same character across multiple scenes (our "warm older woman" archetype) |
| Aspect ratio | Set explicitly: 1:1 (Instagram), 16:9 (LinkedIn/X), 4:5 (IG feed), 9:16 (Reels/YT Shorts) | Match platform |
| Quality | 4K whenever cost allows | Yapper is dignity-tier — never accept blurry |

### 2. APPS (post-production, not regeneration)
Roboverse says: **never regenerate from scratch to fix one detail. Use the apps.**

| App | What it does | Yapper use case |
|---|---|---|
| **Shots** | 1 image → 9 different camera angles in ~30s. Character + environment stay consistent. | Generate 9 angles of one scene for a carousel — e.g., one cozy chair, 9 angles = 9 slides without re-prompting. Massive credit saver. |
| **Angles** | Custom camera perspectives — drone, low angle, specific viewpoint. Rebuilds image from new angle, keeps everything else consistent. | Add variety to recurring scenes (cafe interior from overhead, hallway from low angle). |
| **Outfit Swap** | Two images → one combined image. Keep face/lighting/background, swap outfit. | Test "same resident, different time of day" — same woman, morning robe vs evening cardigan, no character break. |
| **Transitions** | Two shots → smooth cinematic transition (flying cam, morph, zoom, raven). | Stitch together scene cuts for our Reels — Yapper phone booth scene → memory care scene → ending card. |

### 3. VIDEO (Higgsfield video models — for Yapper Reels & YT Shorts)
Roboverse emphasizes: **video prompts should specify camera + subject motion + lighting separately, not as one blob.** His examples:

- "Drone shot pulling back from the explorer in the ice cave, smooth gimbal movement, no shake, blue glacial lighting maintained"
- "Close-up tracking shot following the subject's hands, shallow depth of field, warm practical lighting"

**Yapper translation:**

- Opening shot: "Static wide, lavender mist living room, cream rotary phone on table, soft morning light. Hold for 3s, no motion."
- Mid shot: "Slow dolly forward into the phone booth, ink plum walls closing around the camera, mint accents visible through the glass, no person visible yet."
- Closing: "Cut to end card: ink plum background, lavender dial dots rotating into place, mint accent dot materializes at lower right, warm chime. No motion after the dot lands."

### 4. CHARACTER + SOUL (the brand-character layer)

**Custom character creator lets us dial in:**
- Skin tone (color picker)
- Eye color (rare in other tools)
- Skin conditions: freckles, birthmarks, scars (these small details make "an AI influencer feel like an actual person")
- Face/body/style options
- Render style: hyperrealistic

**Then:** the same character can be placed in any scene via the "customize" step. **This is how you build a consistent brand without ever filming a real person.**

**Yapper Soul candidates (6 — 3 men, 3 women, balanced demographic):**

1. **Margaret** — warm older woman archetype, ~75. Long silver-gray hair, soft knit in lavender + mint, gentle smile, ink-plum or navy cardi. Reuse across phone booth, reading nook, family dinner, by window.
2. **Tom** — warm older man archetype, ~78. Silver-white hair, weathered hands, glasses, often in a cardigan over a checked shirt, reading chair or workshop. The character who proves Yapper isn't just for older women. **Critical for the lonely-men-actually-taking-the-call story.**
3. **CNA Diane** — staff archetype for B2B. Mid-50s, calm expression, badge, comfortable scrubs.
4. **CNA Marcus** — male staff counterpart to Diane. Mid-40s, friendly expression, athletic build under scrubs, can be in hallway at dusk or helping a resident to a seat. Important so we don't imply all care staff are women.
5. **Rebecca** — adult daughter archetype. Late 30s, phone in hand, soft blazer. Family-facing DTC content.
6. **Daniel** — adult son archetype. Late 30s/early 40s, hands often full (kid, work, parent), phone in hand, often at the office or in the car. Lives in the same guilt as Rebecca but rarely talks about it.

**Why 6, why males:** Per NCAL, 67% of assisted living residents are women, 33% men. But AARP 2025 reports men are now lonelier than women (42% vs 37%). Men also report worse quality of life in nursing homes than women per recent Medicare Advocacy data. A brand that only depicts older women as its audience is dishonest about who actually needs the call — and misses the audience that needs it most. Tom, Marcus, and Daniel exist to fill that gap without making it feel performative.

**Soul isolation:** Each Soul gets its own character ID on Higgsfield. They never cross-contaminate (per our existing Soul ID isolation rule for multi-brand separation, this same mechanism isolates personas within Yapper too).

Each Soul ID is isolated (per our existing rule). Use `refs/01-logo.png` + `04-rotary-phone.jpeg` + `05-phone-booth-hallway.png` as initial reference images for tone.

---

## Operational rules Roboverse enforces (translated for Yapper)

1. **Pick the right model per job.** Default to Nano Banana Pro for photos. Use Soul ID for character consistency. Use Sea Dream 4.0 only when going stylized.
2. **Never regenerate to fix one thing.** Use the apps (Shots, Angles, Outfit, Transitions).
3. **Specify camera + motion + lighting as separate fields in video prompts.** Don't blob them together.
4. **Dial in skin details.** Freckles, birthmarks, scars — these are what make a face look real vs. generic-AI.
5. **4K whenever cost allows.** Yapper is dignity-tier — never accept blurry.
6. **Treat Higgsfield as a pipeline, not a generator.** Each output is meant to flow into the next step.

---

## Yapper production templates (ready to use)

### Template A — Static hero image for LinkedIn
```
Model: Nano Banana Pro
Aspect: 1:1
Prompt structure:
  [Subject + setting] [Lighting] [Camera] [Vibe]
```

**Example applied:** "An elderly woman in her 70s sits in a wingback chair upholstered in deep ink plum, holding a vintage cream rotary telephone receiver to her ear, warm three-quarter portrait, soft side window light from the left, lavender mist wall behind, a folded cream knit throw on the chair arm, a mint green coffee mug on a small side table. Editorial photography, dignified, lived-in. No text. No logos."

### Template B — 9-angle carousel (Shots app)
```
1. Generate ONE image (Template A) with desired subject
2. Upload to Shots app
3. Generate → get 9 angles in 30s
4. Pick best 4-6
5. Upscale each
6. Use as carousel slides with caption from 05-CAPTIONS
```
Cost: 1 generation + 1 Shots run + N upscales. Vs 9 separate generations. Saves ~70% credits.

### Template C — Video Reel (9:16, 15s)
```
Video model: hailuo-2.3
Prompt structure:
  [Shot type] [Subject + setting] [Camera motion] [Lighting] [Duration cue]
End card at :13s: ink plum + dial dots + mint accent + yapper.care wordmark
```

**Example applied:** "Static medium close-up on a vintage cream rotary telephone resting on a small table in a quiet living room, lavender mist walls, soft morning light, no person. Hold for 4 seconds. Cut to: same phone, soft focus depth of field shift, slight push-in over 4 seconds. Cut to end card: ink plum background, twelve lavender dial dots arranged in a circle, one mint accent dot at the lower right, the text 'yapper.care' appearing in lavender below. No audio instruction (warm chime only on final card)."

### Template D — Brand character (Soul ID)
```
1. Build character using customizer (Margaret / Diane / Rebecca)
2. Save as Soul
3. When any post needs that character — just reference by name in prompt
4. Character stays consistent across scenes, outfits, lighting
```

---

## Cost-efficiency rules (Roboverse emphasizes)

- Use Shots for 5+ angle variations instead of separate generations
- Save a character once with Soul, reuse hundreds of times
- Use Angles to fix a composition issue, not regenerate
- Outfit Swap to change seasons/wardrobes without breaking character

**Yapper budget impact:** Estimated ~40% credit savings on the calendar once we adopt these patterns. Week 4's 4 carousel slides currently planned as 4 separate generations → becomes 1 generation + 1 Shots run.

---

## Action items for Rafael (you)

1. **Build 3 Soul characters** before we lock W3 (Pillar 3 — Feature Spotlights). Margaret first, then Diane, then Rebecca. Use the Higgsfield customizer settings as starting points; reference images from `brands/yapper/higgsfield/refs/` for tone.
2. **Add 'Shots app' to default workflow** for any carousel needing 4+ slides. Save 70% credits.
3. **Set Nano Banana Pro + 4K as default** for all hero images unless explicitly going artistic.
4. **Pull a frame from each Yapper video to use as the LinkedIn thumbnail cover** — Roboverse's "Shots" idea works in reverse for thumbs.
