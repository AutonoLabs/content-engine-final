# Packet 05 — tiktok — quick-tip

> **Paste the prompt block into Higgsfield video model: `veo-3.1`**
> **Settings: 9:16, 9s**
> **Your job: paste → download → rename to `2026-W30-05.mp4` → drop in `brands/<brand>/inbox/`**
> **The agent handles everything else.**

---

## Settings

- **Model:** `veo-3.1` (Cinematic 8s shots, documentary-style, default video model)
- **Aspect ratio:** 9:16
- **Duration:** 9s
- **Credit cost estimate:** ~? credits

## Prompt (copy everything below this line into the model's prompt field)

```
Cinematic 9s shot of signing a milestone payment release on a phone, the milestone-payment confirmation visible on screen on a UK any. natural morning lighting. Handheld steadicam feel. Ambient construction sounds, no speech, no music. Worker shown only as hands/arms/tools — no full faces.
```

**Audio:** Ambient construction sounds: distant hammering, power tools, no speech, no music.

## Accept if

- Clear focal point visible in first frame
- Reads correctly at thumbnail size
- No text overlays, no logos, no visible UI chrome
- Brand-appropriate visual register (documentary, candid, UK, slightly looser than LinkedIn)
- No speech (unless pattern explicitly allows)

## Reject if

- Melted hand geometry
- Stock-photo studio lighting
- Non-UK building details (US-style suburb, tropical)
- AI-tell visual artifacts (uncanny stillness, smoothed textures)
- Any visible watermark or AI-generation artifact
- Output doesn't match the prompt's setting (wrong location, wrong action, etc.)

## Return contract

Save the downloaded file as:

```
2026-W30-05.mp4
```

Drop it in: `brands/<brand>/inbox/`

`pair_media.py` will scan inbox/, match this packet by filename, move it to the right
post folder, and update the post's status to `media-ready`.
