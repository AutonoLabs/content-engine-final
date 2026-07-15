# Packet 06 — x — tradesperson-broll

> **Paste the prompt block into Higgsfield video model: `veo-3.1`**
> **Settings: 16:9, 10s**
> **Your job: paste → download → rename to `2026-W30-06.mp4` → drop in `brands/<brand>/inbox/`**
> **The agent handles everything else.**

---

## Settings

- **Model:** `veo-3.1` (Cinematic 8s shots, documentary-style, default video model)
- **Aspect ratio:** 16:9
- **Duration:** 10s
- **Credit cost estimate:** ~? credits

## Prompt (copy everything below this line into the model's prompt field)

```
Cinematic 10s shot of a tradesperson walking through a finished kitchen, hands in pockets, looking around slowly, no text on a UK completed UK kitchen extension, Victorian terraced house. late afternoon golden hour lighting. Handheld steadicam feel. Ambient construction sounds, no speech, no music. Worker shown only as hands/arms/tools — no full faces.
```

**Audio:** Ambient construction sounds: distant hammering, power tools, no speech, no music.

## Accept if

- Clear focal point visible in first frame
- Reads correctly at thumbnail size
- No text overlays, no logos, no visible UI chrome
- Brand-appropriate visual register (documentary, candid, UK, premium)
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
2026-W30-06.mp4
```

Drop it in: `brands/<brand>/inbox/`

`pair_media.py` will scan inbox/, match this packet by filename, move it to the right
post folder, and update the post's status to `media-ready`.
