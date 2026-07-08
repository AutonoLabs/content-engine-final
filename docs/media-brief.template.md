# Media Brief Template

> Higgsfield prompt package. One per post. Engineer for "stop the scroll" in first 0.5s. Updated 2026-07-07 (added what-good/what-reject, hook engineering).

---

## Brief structure

Every media brief has 6 sections:
1. **The brief** — exact prompt to paste into higgsfield
2. **Model + format** — what model, what aspect ratio, what duration
3. **Visual hook** — what catches the eye in first 0.5s (from `docs/visual-hooks.md`)
4. **Audience context** — who's on this platform (from `docs/audience-demographics.md`)
5. **What good looks like** — the visual the prompt should produce (so user can judge)
6. **What to reject** — visual tells that mean the prompt didn't land

---

## Brief naming convention

```
<brand>-<platform>-<post-number>-<version>
```

Examples:
- `allsquared-linkedin-01.png`
- `allsquared-x-01.png`
- `allsquared-youtube-01.mp4`
- `yapper-instagram-03-v2.jpg` (regenerated)

---

## Template (copy for each brief)

### Post [N] — [Platform]

**Post context:** [1-2 sentences on what the caption is about]

**Hook engineering:** [What the visual needs to do in the first 0.5s to stop the scroll. E.g. "High contrast lighting, single window glow, scaffolding visible — visual equivalent of a contrarian hook."]

**The brief (paste this into higgsfield):**

```
[Exact prompt text]
```

**Model + format:**
- Model: [Nano Banana Pro / Veo 3.1 Fast / Seedance 2.0 / Kling 3.0]
- Aspect ratio: [1:1 / 16:9 / 9:16]
- Duration (if video): [6s / 8s / 15s / 30s / 58s]
- Quality: [standard / high / 4k]

**What good looks like:**
[2-3 sentences describing the ideal output. Specific composition, lighting, mood. The user judges the generated image against this.]

**What to reject:**
- [Visual tell 1 that means the prompt didn't land]
- [Visual tell 2]
- [Visual tell 3]

---

## Platform defaults

### LinkedIn (image post)
- Model: Nano Banana Pro
- Aspect: 1:1
- Tone: contemplative, professional, no people, no logos

### X / Twitter (image post)
- Model: Nano Banana Pro
- Aspect: 16:9
- Tone: thumbnail-readable, high contrast, no people

### Instagram (image post)
- Model: Nano Banana Pro
- Aspect: 1:1 or 4:5
- Tone: aesthetic, mood-driven, can have people (but no synthetic testimonials)

### TikTok / Reels (video)
- Model: Veo 3.1 Fast (cheap) or Seedance 2.0 Fast (slower but better motion)
- Aspect: 9:16
- Duration: 8-15 seconds (sweet spot for retention)
- Hook in first 0.5s (visual + text + audio)

### YouTube Shorts (video)
- Model: Veo 3.1 Fast or Seedance 2.0 Fast
- Aspect: 9:16
- Duration: 30-58 seconds (longer than TikTok is fine)
- Thumbnail-quality first frame

### Threads (image post)
- Model: Nano Banana Pro
- Aspect: 1:1
- Tone: casual, iPhone-aesthetic, lived-in

---

## Common prompt patterns (proven)

### Architectural / contemplative (AllSquared)
```
A [specific architectural element]. [Lighting]. [Mood]. No people. No text overlay. [Palette]. Photographic, [adjective], [adjective]. No logos, no brands visible.
```

### Documentary / real (Yapper, personal)
```
A [specific scene]. [Specific detail]. [Specific detail]. [Lighting]. No people. [Adjective], [adjective], [adjective]. Muted [palette]. Looks like an iPhone photo, not a stock image.
```

### Cinematic video (TikTok, YouTube Shorts)
```
[N] second video. [Camera movement]. [Subject]. [Specific detail]. [Specific detail]. [Lighting]. No people. [Mood], [adjective], [adjective]. [Aspect ratio] vertical/horizontal, high quality.
```

---

## What to ALWAYS avoid in prompts

- ❌ "beautiful" (vague, AI-tell)
- ❌ "stunning" (AI-tell)
- ❌ "professional" (vague without specifics)
- ❌ "high quality" (model assumes this anyway)
- ❌ "eye-catching" (not a visual specification)
- ❌ Asking for text on image (AI-generated text is usually broken; if you need text, add it in post)
- ❌ Logos or brand names (trademark issues + AI-tell)
- ❌ Real people's faces (deepfake/misleading conduct risk + uncanny valley)

---

## What to ALWAYS include

- ✅ Specific subject (not "a building" but "a Victorian terraced house")
- ✅ Specific detail (scaffolding, window type, material)
- ✅ Specific lighting (soft natural light, dusk amber, etc.)
- ✅ Specific palette (3-5 named colors)
- ✅ "No people" if no people wanted
- ✅ "No text overlay" if no text wanted
- ✅ Mood (contemplative, real, documentary, etc.)
- ✅ Style reference (photographic, cinematic, iPhone-aesthetic, etc.)

---

## Generation credit costs (Higgsfield Ultra, July 2026)

| Model | Cost per generation |
|---|---|
| Nano Banana Pro (image) | ~5 credits |
| Veo 3.1 Fast (8s video) | ~50 credits |
| Seedance 2.0 Fast (8s video) | ~80 credits |
| Seedance 2.0 (15s video, 4k) | ~200 credits |
| Kling 3.0 (15s video) | ~150 credits |
| Grok Video (15s) | ~80 credits |

**Budget per week:** ~500 credits for image posts, ~1000 credits for video. Stay under to avoid mid-month credit exhaustion.

For the **full prompt library per model** (kling 3.0, seedance 2.0 4k, veo 3.1, sora 2 max, grok video, hailuo 2.3) — including what-good/what-reject gates per model — see `docs/higgsfield-prompts.md`.

---

## Quality check after generation

Before approving a generated asset:

1. **Hook test:** Does the first frame/visual land in 0.5s on a phone screen?
2. **Composition:** Is there a clear focal point?
3. **Brand safety:** No logos, no real faces, no text artifacts?
4. **Caption alignment:** Does the visual match the caption's tone and message?
5. **Mobile readability:** Can you tell what the image is at thumbnail size?

If any fail, regenerate with a more specific prompt or different model.

---

## File delivery

After generation, save to:
```
~/clawd/agents/autonio/inbox/media/week-<YYYY>-<W##>/<brand>-<platform>-<post-number>.<ext>
```

The agent (autonio) picks up from there for blotato upload + publishing.