# Packet 02 — linkedin — snagging-ceremony

> **Paste the prompt block into Higgsfield model: `veo-3.1`**
> **Settings: 1:1, 8s**
> **Your job: paste → download → rename to `2026-W29-02.mp4` → drop in `brands/<brand>/inbox/`**
> **The agent handles everything else.**

---

## Settings

- **Model:** `veo-3.1` (Cinematic 8s shots, documentary-style, default video model)
- **Aspect ratio:** 1:1
- **Duration:** 8s
- **Credit cost estimate:** ~50 credits

## Prompt (copy everything below this line into the model's prompt field)

```
8s shot of builder inspecting finished work with notebook. completed kitchen, daylight. Warm natural light. Hands, documents, or screen — no full faces. Sense of quiet satisfaction, not staged joy.
```

**Audio:** Quiet ambient sound, no music, no speech.

## Accept if

- Clear focal point visible in first frame
- Reads correctly at thumbnail size
- No text overlays, no logos, no visible UI chrome
- Brand-appropriate visual register (lifestyle, candid, UK tradesperson register)
- No speech (unless pattern explicitly allows)

## Reject if

- Staged stock-photo high-five
- Visible corporate logos (unless brand-verified)
- Over-saturated colors
- Any visible text overlay
- Any visible watermark or AI-generation artifact
- Output doesn't match the prompt's setting (wrong location, wrong action, etc.)

## Return contract

Save the downloaded file as:

```
2026-W29-02.mp4
```

Drop it in: `brands/<brand>/inbox/`

`pair_media.py` will scan inbox/, match this packet by filename, move it to the right
post folder, and update the post's status to `media-ready`.
