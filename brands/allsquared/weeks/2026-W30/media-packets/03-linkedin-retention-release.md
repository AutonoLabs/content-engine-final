# Packet 03 — linkedin — retention-release

> **Paste the prompt block into Higgsfield image model: `nano-banana-pro`**
> **Settings: 1:1, 2k resolution**
> **Your job: paste → download → rename to `2026-W30-03.jpg` → drop in `brands/<brand>/inbox/`**
> **The agent handles everything else.**

---

## Settings

- **Model:** `nano-banana-pro` (Photoreal stills, inpainting, text overlay, product shots. Best default for LinkedIn images.)
- **Format:** single image
- **Aspect ratio:** 1:1
- **Resolution:** 2k
- **Credit cost estimate:** ~8 credits per image

## Prompt (copy everything below this line into the model's prompt field)

```
Photoreal still image of A tradesperson's hand on a signed retention-release document, with the figure clearly visible. The document sits on a clean timber worktop. In the soft-focus background: a finished UK kitchen extension, brass tap, bone-white walls. Late afternoon golden hour light from a side window. completed UK kitchen extension, late afternoon. late afternoon golden hour lighting. Editorial composition, clean negative space, square frame. architectural, premium, UK. UK architectural details. 
```

## Accept if

- Clear focal point visible at thumbnail size
- architectural, premium, UK register holds
- No text overlays, no logos, no visible UI chrome (unless specified above)
- No AI-tell artifacts (uncanny stillness, smoothed textures, plastic skin)
- Reads correctly at LinkedIn feed size (~600px wide)


## Reject if

- Stock-photo lighting
- Visible watermarks / UI chrome
- Non-UK building details
- Over-saturated colors
- Generic LinkedIn stock-photo aesthetic
- Any visible watermark or AI-generation artifact
- Output doesn't match the prompt's setting (wrong location, wrong subject, etc.)
- Generic stock-photo aesthetic (this is the #1 tell)

## Return contract

Save the downloaded file as:

```
2026-W30-03.jpg
```

Drop it in: `brands/<brand>/inbox/`

`pair_media.py` will scan inbox/, match this packet by filename, move it to the right
post folder, and update the post's status to `media-ready`.
