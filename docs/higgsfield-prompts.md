# Higgsfield Prompts Library

> Working prompt templates for each Higgsfield model. Engineer for **stop-the-scroll in 0.5s**, gate by **what-good-looks-like** vs **what-to-reject**, and read this before every generation.

**Hard rule (2026-07-08):** ALL automated generation uses **credit mode**. Higgsfield's "unlimited" tier is gated against automation per ToS fair-use. Don't try to bypass — credit mode is enforced in `scripts/higgsfield_generate.py` (it refuses `--credit-mode false`).

**Stack:** Higgsfield Ultra $99/mo → 6000 credits/mo. ~5 credits/image, ~50-200 credits/video depending on model + duration.

---

## How to use this doc

1. **Pick a model** from the [model registry](#model-registry) below based on platform + duration + budget
2. **Pick a prompt pattern** from the [pattern library](#pattern-library) (architectural, documentary, cinematic, etc.)
3. **Fill in the 6-field brief** following `docs/media-brief.template.md`
4. **Run** `python scripts/higgsfield_generate.py --brief <path-to-brief.md>`
5. **Gate the output** by checking against the model's [what-good/what-reject](#model-specific-what-goodwhat-reject) before approving

If output fails the gate, regenerate with more specific prompt + a different model. Don't ship a borderline result.

---

## Model registry

| Model | Best for | Aspect | Max duration | Cost (credits/sec) | 4K | Notes |
|---|---|---|---|---|---|---|
| **kling-3.0** | Cinematic motion, longer takes | any | 30s | 2 | ❌ | Good default for video. Strong human motion if needed. |
| **seedance-2.0-4k** | Hero videos, product shots | any | 30s | 4 | ✅ | 4K output. Use for hero posts, big launch videos. |
| **veo-3.1** | Realistic, naturalistic | any | 60s | 3 | ❌ | Best for documentary / lived-in feel. Longer max duration. |
| **sora-2-max** | Complex scenes, multi-subject | any | 60s | 5 | ❌ | High cost. Use sparingly — only for the most demanding scenes. |
| **grok-video** | Cheap iteration, low-stakes | 16:9 only | 15s | 1 | ❌ | Use for drafts / testing concepts before committing credits. |
| **hailuo-2.3** | Quick turnaround, decent quality | any | 30s | 2 | ❌ | Workhorse. Solid middle-ground option. |

**Per-platform default:**

| Platform | Default model | Aspect | Duration |
|---|---|---|---|
| LinkedIn (image) | n/a — use Nano Banana Pro for static images, or veo-3.1 for 30s+ video | 1:1 / 1.91:1 | n/a |
| X (image) | veo-3.1 (video) or hailuo-2.3 | 16:9 / 1:1 | 30-140s |
| Instagram (image) | n/a — Nano Banana Pro | 1:1 / 4:5 | n/a |
| Instagram Reels | veo-3.1 or seedance-2.0-4k | 9:16 | 15-90s |
| TikTok | veo-3.1 or hailuo-2.3 | 9:16 | 15-60s |
| YouTube Shorts | seedance-2.0-4k or kling-3.0 | 9:16 | 30-60s |
| Threads (image) | n/a — Nano Banana Pro | 1:1 | n/a |
| YouTube (long-form) | sora-2-max or veo-3.1 | 16:9 | 60s+ |

---

## Pattern library

These are **proven prompt structures** — copy the template, fill in the brackets. Each has what-good/what-reject baked in.

### Pattern 1: Architectural / contemplative (good for AllSquared, B2B, professional services)

```
A [specific architectural element, e.g., Victorian terraced house with scaffolding]. [Lighting, e.g., dusk amber light filtering through scaffolding poles]. [Mood]. No people. No text overlay. [Palette, e.g., warm browns, charcoal, muted ochre]. Photographic, [adjective], [adjective]. No logos, no brands visible.
```

**Adjectives that work:** `contemplative`, `quiet`, `dignified`, `weathered`, `specific`, `real`.

**Adjectives that fail (AI-tells):** `beautiful`, `stunning`, `professional`, `eye-catching`, `dynamic`.

**What good looks like:**
- Specific, identifiable subject (not "a building")
- Clear focal point with depth (foreground detail, background blur)
- Cohesive palette (3-5 named colors)
- Mood read: contemplative, real, dignified — not generic stock

**What to reject:**
- ❌ Generic cityscape or skyline with no focal point
- ❌ Over-saturated "stock photo" lighting
- ❌ Visible AI artifacts (weird geometry, melted windows, melted bricks)
- ❌ Anything with people (we said no people)
- ❌ Text or watermarks

### Pattern 2: Documentary / real (good for Yapper, founder-to-founder, lived-in)

```
A [specific scene, e.g., morning routine shot in a bathroom with bright fluorescent light]. [Specific detail 1, e.g., open medication bottle on sink]. [Specific detail 2, e.g., crumpled receipt visible in trash]. [Lighting]. No people. [Adjective], [adjective], [adjective]. Muted [palette]. Looks like an iPhone photo, not a stock image.
```

**Adjectives that work:** `real`, `lived-in`, `specific`, `documentary`, `honest`, `unpolished`.

**What good looks like:**
- Reads as "real person took this" — slight imperfection, not staged
- 2+ specific props/details that ground the scene
- Color temperature feels right for the lighting described
- No "stock photo" over-production

**What to reject:**
- ❌ Anything that looks like a stock photo composition
- ❌ Clean, minimal, staged setups (looks like a brand shoot)
- ❌ Perfect lighting / no shadows
- ❌ Missing specific details (too generic)

### Pattern 3: Cinematic video (good for TikTok, YouTube Shorts, founder-story videos)

```
[N]-second video. [Camera movement, e.g., slow dolly forward]. [Subject, e.g., construction site at sunrise, scaffolding silhouetted]. [Specific detail 1, e.g., worker's hard hat on a beam]. [Specific detail 2, e.g., steam rising from a kettle in foreground]. [Lighting]. No people visible (or: one person visible from behind only). [Mood, e.g., contemplative], [adjective], [adjective]. [Aspect ratio] vertical/horizontal, high quality.
```

**Camera movements that work:** `slow dolly forward`, `static with subtle handheld drift`, `low-angle tracking`, `pan left to right revealing subject`.

**What good looks like:**
- One camera move, one subject, no cuts (Higgsfield doesn't cut well, plan around this)
- Visible motion in the scene (steam, leaves, light shift) — keeps the viewer watching
- First frame must look like a strong thumbnail

**What to reject:**
- ❌ Multiple cuts (Higgsfield struggles with this — regenerate without "cuts" in prompt)
- ❌ Subject that disappears mid-frame
- ❌ No motion at all (looks like a still photo with 1 frame of movement)
- ❌ AI-tell adjectives in output: "beautiful", "stunning", "dynamic"

### Pattern 4: Product / object focus (good for hero posts, launch announcements)

```
A [specific product or object, e.g., a brass padlock with key]. [Material details, e.g., tarnished brass, slight patina]. [Lighting, e.g., single window light from left, soft shadow]. [Background, e.g., out-of-focus wooden surface]. No people. Photographic, [mood], [adjective]. No logos, no text, no brands visible.
```

**What good looks like:**
- Hero-quality composition (rule of thirds, clear focal point)
- Material reads as real (not CGI-smooth)
- Light direction consistent throughout (no AI flicker)

**What to reject:**
- ❌ Flat, evenly-lit product shots (looks like e-commerce)
- ❌ CGI-smooth surfaces (looks AI-generated)
- ❌ Multiple products competing for attention
- ❌ Logos or brand marks (trademark risk)

### Pattern 5: Quiet visual / negative space (good for LinkedIn contemplative posts)

```
A [minimal scene, e.g., a single window in an otherwise empty wall]. [Lighting, e.g., late afternoon light casting one long shadow]. No people. No objects. [Mood, e.g., quiet, waiting, contemplative]. [Palette]. Photographic. No text overlay. No logos.
```

**What good looks like:**
- Lots of negative space (good for caption overlay in LinkedIn if user adds text manually)
- Single subject or even empty frame
- Mood reads clearly: quiet, waiting, contemplative

**What to reject:**
- ❌ Anything busy or visually loud
- ❌ Multiple focal points
- ❌ Bright saturated colors (kills the contemplative mood)

### Pattern 6: Action / kinetic (good for behind-the-scenes, process videos)

```
[N]-second video. [Camera, e.g., overhead static]. [Action, e.g., hands tying knots in climbing rope]. [Specific details, e.g., frayed rope ends, worn leather gloves]. [Lighting, e.g., warm work light]. [Subject, e.g., worker's hands only, no face]. Photographic, [mood], real.
```

**What good looks like:**
- Hands-only / object-only action (avoids face uncanny valley)
- Real motion: tying, hammering, mixing, drilling
- Visible texture/material details

**What to reject:**
- ❌ Visible faces (deepfake risk + uncanny valley)
- ❌ Static frame (no motion = no retention)
- ❌ Generic "worker hands" stock imagery (lacks specifics)

---

## Model-specific what-good/what-reject

Different models have different failure modes. Use these as the per-model quality gates.

### kling-3.0

**Strengths:** Cinematic motion, human motion if needed, decent text in frame (still avoid).
**Weaknesses:** Backgrounds can smear. Wide shots lose detail.

**What good looks like (kling-3.0):**
- Subject in foreground, sharp
- Camera move is single + smooth
- Motion is contained (one subject, one direction)

**What to reject (kling-3.0):**
- ❌ Wide establishing shots (smears)
- ❌ Multiple subjects in motion (motion blur + identity drift)
- ❌ Anything requiring legible text

### seedance-2.0-4k

**Strengths:** 4K output, hero-quality, long takes (up to 30s).
**Weaknesses:** Slow generation, expensive credits. Sometimes over-smooths.

**What good looks like (seedance-2.0-4k):**
- Hero-quality composition
- Crisp detail (4K visible)
- Long-form motion that doesn't drift

**What to reject (seedance-2.0-4k):**
- ❌ Anything that looks CGI-smooth (over-processed)
- ❌ Static frames (waste of 4K budget)
- ❌ Cheap throwaway content (too expensive for this)

### veo-3.1

**Strengths:** Realistic, naturalistic, documentary feel. Best "this looks real" model.
**Weaknesses:** Slower generation. Struggles with stylized.

**What good looks like (veo-3.1):**
- Reads as documentary / real
- Natural lighting
- Specific environment, not generic

**What to reject (veo-3.1):**
- ❌ Anything stylized or cartoonish
- ❌ Studio-lit scenes (defeats the realistic strength)
- ❌ Fast cuts / dynamic motion (this model is for slow + real)

### sora-2-max

**Strengths:** Complex multi-subject scenes, long duration (60s).
**Weaknesses:** Most expensive. Most prone to AI-tells.

**What good looks like (sora-2-max):**
- Complex scene with multiple focal points, all reading correctly
- Long-form narrative arc visible

**What to reject (sora-2-max):**
- ❌ Simple scenes (waste of credits — use veo-3.1)
- ❌ Anything with visible AI-tells (this model has the most)
- ❌ Generic stock compositions

### grok-video

**Strengths:** Cheap, fast. Good for iteration.
**Weaknesses:** Lowest quality. Only 16:9.

**What good looks like (grok-video):**
- Concept reads correctly
- Good enough to test if the prompt works before scaling up

**What to reject (grok-video):**
- ❌ Anything you'd actually ship (use this for drafts only)
- ❌ Hero-quality expectations
- ❌ Vertical video (16:9 only)

### hailuo-2.3

**Strengths:** Workhorse. Solid middle ground.
**Weaknesses:** Not best-in-class for anything specific.

**What good looks like (hailuo-2.3):**
- Reliable output
- Good enough for non-hero posts

**What to reject (hailuo-2.3):**
- ❌ Hero-quality expectations (use seedance-2.0-4k instead)
- ❌ Anything requiring best-in-class realism (use veo-3.1)

---

## Output gate (universal)

After generation, before publishing, run this gate:

```
□ 1. Hook test: Does the first frame/visual land in 0.5s on a phone screen?
□ 2. Composition: Is there a clear focal point?
□ 3. Brand safety: No logos, no real faces, no text artifacts?
□ 4. Caption alignment: Does the visual match the caption's tone and message?
□ 5. Mobile readability: Can you tell what the image is at thumbnail size?
□ 6. Model-specific gate: Does it pass the model-specific what-good/what-reject above?
```

If any fail, regenerate. Don't ship a borderline result.

---

## Credit budget planning

**Monthly: 6000 credits.**

**Suggested allocation per brand:**
- ~500 credits/week for image posts (LinkedIn, X, Instagram, Threads)
- ~1000 credits/week for video posts (TikTok, YouTube Shorts, Reels)
- ~1500 credits/week per brand active

**Per-brand-per-week budget:**
- 3-5 posts across platforms
- 1-2 of those are video (use veo-3.1 or hailuo-2.3 for cost control)
- Use grok-video to iterate on prompts before committing credits

**Burn tracking:**
- Log credit usage in `brands/<brand>/weeks/<YYYY-W##>/generation-log.md`
- If trending toward mid-month exhaustion, switch to Nano Banana Pro for images + hailuo-2.3 for video

---

## Common prompt failures (do not retry, regenerate fresh)

- **"Beautiful [X]"** → swap for a specific material/lighting detail
- **"Professional [X]"** → swap for a specific style reference (iPhone photo, documentary, cinematic)
- **"High quality"** → model assumes this, remove
- **"Eye-catching"** → not a visual specification, remove
- **Asking for text on image** → if you need text, add it in post
- **Asking for logos** → trademark risk + AI-tell, never
- **Asking for real people's faces** → deepfake/misleading conduct risk + uncanny valley

If a prompt fails twice with the same model, switch models. Don't retry the same model three times — credits add up.

---

## Related docs

- `docs/media-brief.template.md` — the 6-field brief template per post
- `docs/visual-hooks.md` — what stops the scroll per platform
- `docs/audience-demographics.md` — who's on each platform
- `examples/allsquared/weeks/2026-W28/media-briefs.md` — worked example
- `scripts/higgsfield_generate.py` — automation, credit-mode enforcement

---

**Last updated:** 2026-07-08
**Maintainer:** Autono Labs