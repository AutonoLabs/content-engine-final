# Higgsfield Workflow — Yapper

> The human (Rafael/Eli) workflow for producing Higgsfield media. Copy-paste from here into Higgsfield UI, change settings, post output back to Discord.

---

## How this works (the loop)

1. **I draft the post + write the Higgsfield brief** (prompt, model, aspect ratio, duration)
2. **I paste the brief here in a code block** — you copy it into Higgsfield
3. **You set the model + settings** (I specify which model + parameters)
4. **You generate in Higgsfield UI**
5. **You download the output and post it back here** (or drop the file URL)
6. **I validate the output** against the quality gate
7. **I publish via Blotato** with the caption + your media

That's it. You never write prompts. You never touch Blotato. You just copy-paste-generate-download-drop.

---

## Higgsfield model selection (Yapper defaults)

| Use case | Model | Aspect | Duration | Credits |
|---|---|---|---|---|
| IG image post | Nano Banana Pro | 1:1 or 4:5 | static | ~5 |
| IG Reel | veo-3.1 | 9:16 | 15-30s | ~45-90 |
| TikTok | veo-3.1 or hailuo-2.3 | 9:16 | 15-30s | ~30-60 |
| YouTube Shorts | seedance-2.0-4k or kling-3.0 | 9:16 | 30-60s | ~60-120 |
| LinkedIn image | Nano Banana Pro | 1:1 or 1.91:1 | static | ~5 |
| LinkedIn video | veo-3.1 | 1:1 or 16:9 | 15-30s | ~45-90 |
| X image | Nano Banana Pro | 16:9 | static | ~5 |
| X video | hailuo-2.3 | 16:9 | 15s | ~15-30 |
| Threads image | Nano Banana Pro | 1:1 | static | ~5 |

**Credit budget:** 6000 credits/month. ~1500/week for Yapper.
- 3-5 posts/week
- 2-3 of those use Higgsfield
- Use grok-video (1 credit/sec) to test prompts before committing to expensive models

---

## Yapper visual style rules (baked into every prompt)

**Always include in prompt:**
- Warm natural light, not studio
- Documentary feel, like an iPhone photo
- Specific props: rotary phone, phone booth, side table, common room
- Navy/purple/teal palette where applicable
- No faces visible (use hands, over-shoulder, objects)
- No logos, no text overlay, no watermarks
- No clinical/medical imagery
- No stock photo composition

**Pattern library (from docs/higgsfield-prompts.md):**
- Pattern 2 (Documentary/real) = Yapper default
- Pattern 5 (Quiet visual/negative space) = LinkedIn contemplative posts
- Pattern 6 (Action/kinetic) = behind-the-scenes, hands picking up phone

---

## Brief template (what I output for each post)

```
=== HIGGSFIELD BRIEF — [post ID] ===

MODEL: [model name]
ASPECT: [ratio]
DURATION: [seconds or "static"]
CREDITS: [estimated cost]

PROMPT (copy-paste this):
---
[full prompt text, Yapper style rules baked in]
---

QUALITY GATE (check before approving):
□ First frame lands in 0.5s on phone
□ Clear focal point
□ No logos, no faces, no text artifacts
□ Warm, documentary feel (not stock, not clinical)
□ Matches caption tone

SETTINGS:
- Credit mode: ON (required)
- [any other model-specific settings]
```

---

## Weekly batch flow (simplified for Rafael)

```
Monday: I post the week's plan (6 posts, formats, platforms, themes)
    ↓
Monday: I post Higgsfield briefs for posts that need media (2-3 per week)
    ↓
Mon-Wed: Rafael generates in Higgsfield, drops files back in Discord
    ↓
Wed: I validate media, draft final captions with media attached
    ↓
Thu: Rafael reviews/approves captions
    ↓
Thu-Fri: I publish via Blotato on schedule
    ↓
Following Mon: Performance pull + retro → informs next week's plan
```

---

## What Rafael does (the only 3 things)

1. **Copy-paste Higgsfield prompts** → generate → download → drop file in Discord
2. **Review captions** → approve or edit (edits feed back into voice profile)
3. **Say "go"** → I publish

That's it. Everything else is automated.
