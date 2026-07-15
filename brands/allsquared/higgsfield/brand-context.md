# AllSquared Higgsfield Brand Context

> Master brand context for every Higgsfield generation. Paste the brand-context prefix at the START of every prompt, then add the specific scene description after it.
>
> **Status:** v0.1 DRAFT — palette + banned-imagery section needs review from Eli. Edit this file when brand visual identity solidifies.

---

## METHOD 1: Reference Images (upload once, reuse forever)

When you open a generation, click **Reference** and select these from `brands/allsquared/inbox/brand/refs/`:

1. **Logo / wordmark** (upload once we have a real logo)
2. **Brand color palette swatch** — `refs/01-color-palette.png`
3. **Reference environment** — a completed UK kitchen extension (golden hour, premium register)

Until we have a real logo, the brand-context prefix below carries the color information.

---

## METHOD 2: Brand Prompt Prefix (paste at the start of every prompt)

```
BRAND CONTEXT: AllSquared (allsquared.com) — escrow + milestone payments for UK construction projects. Visual style: documentary, premium, restrained, lived-in, UK trade register. NOT stock-photo, NOT American suburban, NOT AI-hype, NOT corporate SaaS. Looks like a still from a high-end UK property programme. Color palette: warm clay #B47B5C (primary accent, use sparingly — a paint swatch, a brass tap, a wood detail), bone white #F2EDE5 (light backgrounds, walls, linen), slate charcoal #2A2D33 (dark surfaces, NOT pure black — use for door frames, hinges, hardware), moss green #5C6B53 (the only saturated green — exterior doors, planters, mature hedging — use sparingly, this is the "garden after work" colour). Every image must include 1-2 brand colors naturally placed. No pure black backgrounds. No purple-blue gradients. No American flag colors. No construction PPE in frame (hats, hi-vis, steel toe caps). BANNED: drill-pointing-at-camera, before/after side-by-side cheap framing, motivational poster typography, stock handshakes, stock handshake-with-hardhat, anyone in hi-vis clothing, generic spreadsheet-on-laptop, finished interiors with a single bed sheet in frame (signals an estate photo), any UK house exterior with a "For Sale" or estate-agent sign, American suburbs, white picket fences, palm trees, distressed wood effects, "fixer upper" aesthetic. CAMERA: restrained handheld, shallow depth of field, natural window light, warm but not amber. Looks shot on a Cooke S4 32mm lens or similar documentary-prime. For VIDEO: 15s with no speech, no on-screen text, no captions, no UI. Final 2-3 seconds transition to a perfectly flat, motionless bone-white (#F2EDE5) frame; leave the center empty for the AllSquared logo to be added in post.
```

(Edit this block to match the actual AllSquared brand palette once it's defined. Keep the BANNED section exhaustive — it's the most valuable part.)

---

## Quick reference: brand colors

| Name             | Hex       | Use in images                                                              |
|------------------|-----------|----------------------------------------------------------------------------|
| Warm clay        | `#B47B5C` | Primary accent — paint swatch, brass tap, wood detail, leather sample       |
| Bone white       | `#F2EDE5` | Light backgrounds, walls, linen, end-card frame                            |
| Slate charcoal   | `#2A2D33` | Dark surfaces (door frames, hinges, hardware) — never pure black           |
| Moss green       | `#5C6B53` | The only saturated green — exterior doors, planters, mature hedging         |

## Quick reference: end-card for videos

15-second videos end the same way (consistent brand signature):

```
[at second 13 of a 15-second video]
  bone-white (#F2EDE5) background
  perfectly flat, motionless, no texture, no gradient, no shadow
  no furniture, no person, no logo, no text
  leave the centre empty for the AllSquared wordmark to be added in post
  hold 2 seconds, fade
```

Generate the end-card frame ONCE as a static image. Save to `brands/allsquared/inbox/brand/end-card-v1.png`. Reuse in every video's tail.

---

## What briefs will look like going forward

When the system writes a Higgsfield brief for you, every prompt will already include:
- The brand context prefix (above)
- The specific scene description (subject, setting, action)
- The action script with N-Ns segments
- The negative-prompt list ("no nurses, no badges, no medical equipment")
- The audio architecture (music layers + SFX + room tone)
- The end-card specification
- The accept / reject gates

You just copy-paste the full prompt into Higgsfield and generate. No thinking required.

---

## Banned-imagery checklist (read this BEFORE generating)

This is the most important section. Every prompt should carry these as explicit "do not" lines:

- ❌ Any medical / clinical equipment (beds, monitors, oxygen tanks, IV poles, wheelchairs, walking frames, raised toilet seats)
- ❌ Uniforms of any kind (nurse scrubs, hi-vis vests, hard hats, suits, ties, branded polos, name badges, lanyards)
- ❌ Caregivers, staff, doctors, nurses, family members, anyone OTHER than the person whose POV the post takes
- ❌ Children, babies, pets (unless brand explicitly says yes)
- ❌ Disabled / frailty cues (walkers, canes, mobility scooters, handrails on every wall) — frame the resident as a person, not a patient
- ❌ American anything (suburbs, flags, palm trees, picket fences, "ranch" houses, US dollar bills, US spelling)
- ❌ Generic stock-photo aesthetic (handshake, thumbs up, office whiteboard, puzzle pieces, lightbulb moments, infographic style)
- ❌ Construction PPE (hats, hi-vis, steel toe caps, gloves) — AllSquared sells a SOFTWARE product, not a building trade
- ❌ UK house exteriors with estate-agent signs ("For Sale", "Sold") — we are not an estate agent
- ❌ Drill-pointing-at-camera framing, before/after split frames, motivational text overlays
- ❌ Pure black backgrounds (use slate charcoal #2A2D33 instead)
- ❌ Purple-blue gradients (screams generic AI / generic SaaS)
- ❌ Speech, voiceover, captions, on-screen text in any VIDEO prompt — Yapper-style or documentary-style means SILENT visual storytelling

This list grows over time. Update it after every generation that produced an off-brand asset.