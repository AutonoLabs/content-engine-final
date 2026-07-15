# Packet 02 — linkedin — snagging-ceremony (carousel slide 2/3)

> **Paste the prompt block into Higgsfield image model: `nano-banana-pro`**
> **Settings: 4:5, 2k resolution**
> **Your job: paste → download → rename to `2026-W29-02-slide-2.png` → drop in `brands/<brand>/inbox/`**
> **The agent handles everything else.**

---

## Settings

- **Model:** `nano-banana-pro` (Photoreal stills, inpainting, text overlay, product shots. Best default for LinkedIn images.)
- **Format:** carousel (single slide)
- **Aspect ratio:** 4:5
- **Resolution:** 2k
- **Credit cost estimate:** ~8 credits per image

## Prompt (copy everything below this line into the model's prompt field)

```
Photoreal still image. Subject: Close-up of builder's hand on a cabinet hinge, notebook visible with item ticked off, late morning light. completed Victorian kitchen refit, late morning. late morning natural daylight lighting. Editorial composition, clean negative space, portrait frame (LinkedIn carousel). lifestyle, candid, UK tradesperson register. UK architectural details. Visual style must feel cohesive across all slides.
```

**Carousel:** Generate all 3 slides. Keep visual style consistent across slides (same lighting, same register, same color temperature).

## Accept if

- Clear focal point visible at thumbnail size
- lifestyle, candid, UK tradesperson register holds
- No text overlays, no logos, no visible UI chrome (unless specified above)
- No AI-tell artifacts (uncanny stillness, smoothed textures, plastic skin)
- Reads correctly at LinkedIn feed size (~600px wide)
- Slide 2 of 3 — visually consistent with sibling slides
- Reads correctly when stacked in LinkedIn carousel preview

## Reject if

- Stock-photo lighting
- Visual style inconsistent with a carousel series
- Visible watermarks / UI chrome
- Non-UK building details
- Any visible watermark or AI-generation artifact
- Output doesn't match the prompt's setting (wrong location, wrong subject, etc.)
- Generic stock-photo aesthetic (this is the #1 tell)

## Return contract

Save the downloaded file as:

```
2026-W29-02-slide-2.png
```

Drop it in: `brands/<brand>/inbox/`

`pair_media.py` will scan inbox/, match this packet by filename, move it to the right
post folder, and update the post's status to `media-ready`.
