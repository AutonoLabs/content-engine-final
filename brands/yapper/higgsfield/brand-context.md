# Yapper Higgsfield Brand Context

> This is the master brand context for all Higgsfield generations. Two usage methods below.

---

## METHOD 1: Reference Images (do this once)

Higgsfield has a "Reference" button on generated images. Upload these as reference images and use them for every Yapper generation:

1. **Brand color reference** — `refs/03-color-palette.png`, the verified six-swatch Brand Pack v4 palette
2. **Product reference** — the rotary phone image at `refs/04-rotary-phone.jpeg`
3. **Environment reference** — the phone-booth image at `refs/05-phone-booth-hallway.png`
4. **Logo references** — `refs/01-logo.png` and `refs/02-icon.png`

To use: when generating, click "Reference" and select these images. Higgsfield will use them as visual style guides.

---

## METHOD 2: Brand Prompt Prefix (save this, paste at the start of every prompt)

Copy the block below and save it in your notes/clipboard. Paste it at the START of every Higgsfield prompt, then add your specific scene description after it.

```
BRAND CONTEXT: Yapper (yapper.care) — AI companionship for senior care. Visual style: documentary, warm, lived-in, dignified. NOT clinical, NOT stock photo, NOT AI-generated looking. Looks like an iPhone photo taken by a staff member. Color palette: lavender (#7B61AD), lavender 700 (#4E3E71, depth only), ink plum (#241C36, use instead of black for dark surfaces), mint (#98FFD9, accent only), mint deep (#3ECF9B), lavender mist (#F4F0FA, light backgrounds). Every image must include 1-2 brand colors naturally placed in the scene. No pure black backgrounds. No purple-blue gradients. No violet glows. BANNED: stock hand-holding, hospital beds, robots, brains, circuit textures, cartoon elders, anyone baffled by technology, clinical/medical imagery, perfect studio lighting. For VIDEO: final 2-3 seconds transition to ink plum with the authentic Yapper dial-dots mark and wordmark; ten lavender dots follow the official 270-degree rotary geometry and the mint finger stop lands in the lower-right gap. Soft room tone, then a restrained warm chime.
```

---

## How briefs will work going forward

When I write Higgsfield briefs for you, every prompt will already include:
- The brand context prefix (above)
- The specific scene description
- The brand color placement for that specific image
- The logo ending (for videos)
- The audio specification (for videos)

So you just copy-paste the full prompt and generate. No thinking required.

---

## Quick reference: brand colors

| Name | Hex | Use in images |
|---|---|---|
| Lavender | #7B61AD | Brand anchor, throws, scarves, accent walls |
| Lavender 700 | #4E3E71 | Depth and hover tones only |
| Ink Plum | #241C36 | Dark walls, furniture, backgrounds (NOT black) |
| Mint | #98FFD9 | Small accents, highlights, the logo stop |
| Mint Deep | #3ECF9B | Mugs, plant pots, accessible mint on light grounds |
| Lavender Mist | #F4F0FA | Wall paint, light backgrounds, ambient tint |

## Quick reference: logo ending for videos

Describe it in prompts as:
"authentic Yapper dial-dots mark and wordmark on ink plum (#241C36): ten lavender dots on the official 270-degree rotary arc, dots graduating in size, with the mint finger stop landing in the lower-right gap; hold 2 seconds with a restrained warm chime"
