#!/usr/bin/env python3
"""
Generate prompt packets for Higgsfield media generation.

Reads a week's media briefs and emits one packet per post — a copy-paste-ready
file that contains:
- The exact prompt to paste into the Higgsfield model
- The model + aspect ratio + duration settings
- An audio clause (where the model supports native audio)
- An accept/reject gate (what good looks like, what to reject)
- A return filename contract (the human's job is to rename the file)

This is the outbound half of the human-in-the-loop media workflow.
The human pastes the prompt, downloads the result, renames to the contract,
and drops in brands/<brand>/inbox/. The inbound half (pair_media.py) does the rest.

Usage:
    python scripts/media_packet.py --brand allsquared --week 2026-W30
    python scripts/media_packet.py --brand allsquared --week 2026-W30 --model veo-3.1
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


REPO_ROOT = Path(__file__).resolve().parent.parent

# Model registry — what's available + their audio support
# Audio: True means the model generates native audio (veo/sora); False means silent video
# Format: 'video' or 'image' — drives aspect_ratio handling and packet structure
MODELS = {
    "veo-3.1": {
        "credit_cost_8s": 50,
        "max_duration_s": 60,
        "supports_audio": True,
        "format": "video",
        "best_for": "Cinematic 8s shots, documentary-style, default video model",
    },
    "seedance-2.0-4k": {
        "credit_cost_15s": 200,
        "max_duration_s": 30,
        "supports_audio": False,
        "format": "video",
        "best_for": "Premium 4K footage, hero shots, high-fidelity product shots",
    },
    "kling-3.0": {
        "credit_cost_15s": 150,
        "max_duration_s": 30,
        "supports_audio": False,
        "format": "video",
        "best_for": "Strong human motion, image-to-video with keyframe control",
    },
    "sora-2-max": {
        "credit_cost_15s": 250,
        "max_duration_s": 30,
        "supports_audio": True,
        "format": "video",
        "best_for": "Physics consistency, complex scenes (use sparingly)",
    },
    "grok-video": {
        "credit_cost_15s": 80,
        "max_duration_s": 15,
        "supports_audio": False,
        "format": "video",
        "best_for": "Quick drafts, 16:9 only (NOT for vertical)",
    },
    "hailuo-2.3": {
        "credit_cost_15s": 100,
        "max_duration_s": 30,
        "supports_audio": False,
        "format": "video",
        "best_for": "Strong human motion/expression (when humans are in frame)",
    },
    # Image models — Higgsfield's image generation runs through these
    "nano-banana-pro": {
        "credit_cost_per_image": 8,
        "max_resolution": "2k",
        "supports_text_overlay": True,
        "format": "image",
        "best_for": "Photoreal stills, inpainting, text overlay, product shots. Best default for LinkedIn images.",
    },
    "seedream-4.0": {
        "credit_cost_per_image": 10,
        "max_resolution": "2k",
        "supports_text_overlay": True,
        "format": "image",
        "best_for": "Editorial compositions, brand-styled stills, architectural work",
    },
    "flux-2-klein": {
        "credit_cost_per_image": 4,
        "max_resolution": "1k",
        "supports_text_overlay": False,
        "format": "image",
        "best_for": "Quick drafts, low-fidelity exploration, 4×4 grid comps",
    },
}

# Base prompt patterns from docs/higgsfield-prompts.md
# Each is a template that takes brand-specific variables
BASE_PATTERNS = {
    "tradesperson-broll": {
        "description": "Construction/tradesperson work footage",
        "template": (
            "Cinematic {duration}s shot of {trade_activity} on a UK {building_type}. "
            "{time_of_day} lighting. Handheld steadicam feel. "
            "Ambient construction sounds, no speech, no music. "
            "Worker shown only as hands/arms/tools — no full faces."
        ),
        "audio_clause": "Ambient construction sounds: distant hammering, power tools, no speech, no music.",
        "reject_if": [
            "Melted hand geometry",
            "Stock-photo studio lighting",
            "Non-UK building details (US-style suburb, tropical)",
            "AI-tell visual artifacts (uncanny stillness, smoothed textures)",
        ],
    },
    "founder-portrait": {
        "description": "Founder/team portrait for trust signals",
        "template": (
            "Documentary-style {duration}s portrait of {person_description}. "
            "{location}. Natural {time_of_day} light. "
            "Eye contact with camera, slight smile, candid feel. "
            "No speech — ambient environment sounds only."
        ),
        "audio_clause": "Ambient office/cafe sounds, no speech, no music.",
        "reject_if": [
            "Melted facial features",
            "Generic LinkedIn-headshot pose",
            "Overproduced studio backdrop",
            "Uncanny-valley eye contact",
        ],
    },
    "milestone-celebration": {
        "description": "Milestone payment/celebration moment",
        "template": (
            "{duration}s shot of {celebration_action}. "
            "{location}. Warm natural light. "
            "Hands, documents, or screen — no full faces. "
            "Sense of quiet satisfaction, not staged joy."
        ),
        "audio_clause": "Quiet ambient sound, no music, no speech.",
        "reject_if": [
            "Staged stock-photo high-five",
            "Visible corporate logos (unless brand-verified)",
            "Over-saturated colors",
            "Any visible text overlay",
        ],
    },
    "product-mockup": {
        "description": "Product/screen mockup shot",
        "template": (
            "Clean {duration}s shot of {product_description} on {surface}. "
            "Soft directional light from {direction}. Subtle depth of field. "
            "Screen content visible if applicable. "
            "No people in frame."
        ),
        "audio_clause": "Silent or quiet UI feedback clicks, no speech.",
        "reject_if": [
            "Garbled screen text",
            "Visible browser chrome / OS UI",
            "Stock mockup lighting feel",
            "Visible fake UI elements",
        ],
    },
    "workflow-cinematic": {
        "description": "Cinematic process/workflow shot",
        "template": (
            "Slow cinematic {duration}s dolly through {scene_description}. "
            "Available light. Handheld or steadicam. "
            "Sense of purposeful work in progress. "
            "No speech. Ambient environment sounds only."
        ),
        "audio_clause": "Ambient sounds appropriate to scene, no music.",
        "reject_if": [
            "Obvious green-screen compositing",
            "CGI-smooth motion",
            "Visible camera crew / equipment",
            "AI-tell artifacts",
        ],
    },
    "abstract-texture": {
        "description": "Abstract texture / detail shot",
        "template": (
            "Macro {duration}s shot of {surface_material}. "
            "Raking light from {direction}. Shallow depth of field. "
            "Camera slowly pulls back to reveal context. "
            "No people, no text, no logos."
        ),
        "audio_clause": "Silent or subtle ambient.",
        "reject_if": [
            "Stock-photo bokeh",
            "Visible watermarks",
            "AI-generated surface artifacts",
            "Over-sharpened details",
        ],
    },
    # Campaign / TV spot patterns — for branded video ads (not social posts).
# These have a richer structure: segmented action script, explicit
# negative-prompt lists, multi-layer audio architecture, end-card.
    "documentary-tv-spot": {
        "description": "Documentary-style branded TV spot (15-30s, segmented script)",
        # The pattern's template is rendered in _build_tv_spot_packet(),
        # NOT through the standard render_prompt() — the segmented script,
        # negatives, audio, and end-card come from structured brief fields.
        "template": "{placeholder}",
        "audio_clause": None,  # multi-layer audio rendered separately
        "reject_if": [
            "Visible uniforms, badges, medical equipment",
            "Sentimental framing (crying, dramatic music swell)",
            "Visible AI-tell artifacts (uncanny stillness, smoothed skin)",
            "Pure black backgrounds (use brand slate instead)",
            "Speech, voiceover, captions, on-screen text, watermarks",
        ],
    },
# Image / still patterns — for static posts + carousels
    "single-image": {
        "description": "Single LinkedIn-style still image",
        "template": (
            "Photoreal still image of {scene_description}. "
            "{location}. {time_of_day} lighting. "
            "Editorial composition, clean negative space, "
            "{aspect_ratio_phrase} frame. "
            "{visual_register}. UK architectural details. "
            "{text_overlay_clause}"
        ),
        "audio_clause": None,  # images have no audio
        "reject_if": [
            "Stock-photo lighting",
            "Visible watermarks / UI chrome",
            "Non-UK building details",
            "Over-saturated colors",
            "Generic LinkedIn stock-photo aesthetic",
        ],
    },
    "carousel-slide": {
        "description": "Single slide in a multi-slide LinkedIn carousel",
        "template": (
            "Photoreal still image. "
            "Subject: {scene_description}. "
            "{location}. {time_of_day} lighting. "
            "Editorial composition, clean negative space, "
            "{aspect_ratio_phrase} frame (LinkedIn carousel). "
            "{visual_register}. UK architectural details. "
            "Visual style must feel cohesive across all slides."
        ),
        "audio_clause": None,
        "reject_if": [
            "Stock-photo lighting",
            "Visual style inconsistent with a carousel series",
            "Visible watermarks / UI chrome",
            "Non-UK building details",
        ],
    },
}


def select_pattern(brief: dict) -> str:
    """Pick a base pattern from the brief's pattern hint or platform."""
    hint = brief.get("pattern", "").strip().lower()
    if hint in BASE_PATTERNS:
        return hint

    # Default selection by format + platform
    fmt = brief.get("format", "").lower()
    if fmt == "tv-spot" or fmt == "tv_spot" or fmt == "tvspot":
        return "documentary-tv-spot"
    if fmt == "carousel":
        return "carousel-slide"
    if fmt == "image":
        return "single-image"
    platform = brief.get("platform", "").lower()
    if platform == "tiktok":
        return "tradesperson-broll"
    if platform == "linkedin":
        return "milestone-celebration"
    if platform == "instagram":
        return "product-mockup"
    return "workflow-cinematic"


def select_model(brief: dict, override: Optional[str] = None) -> str:
    """Select model from brief or override."""
    if override:
        return override
    # Default by format: image + carousel (image-based) → nano-banana-pro, video → veo-3.1
    fmt = brief.get("format", "").lower()
    if fmt in ("image", "carousel"):
        return "nano-banana-pro"
    return brief.get("model", "veo-3.1")


def _aspect_phrase(aspect: str) -> str:
    """Human-readable phrase for aspect ratio."""
    return {
        "1:1": "square",
        "4:5": "portrait",
        "9:16": "vertical",
        "16:9": "landscape",
        "1.91:1": "wide",
    }.get(aspect, aspect)


def load_brand_context(brand: str) -> str:
    """
    Load the brand-context prefix block from
    brands/<brand>/higgsfield/brand-context.md.

    Looks for a fenced code block marked with `BRAND CONTEXT:` and returns
    the contents. Returns empty string if not found (caller renders packet
    without prefix in that case, with a warning).
    """
    paths_to_try = [
        REPO_ROOT / "brands" / brand / "higgsfield" / "brand-context.md",
        REPO_ROOT / "brands" / brand / "higgsfield-brand-context.md",
        REPO_ROOT / "brands" / brand / "brand-context.md",
    ]
    for p in paths_to_try:
        if p.exists():
            text = p.read_text()
            # Pull out the first fenced block that starts with "BRAND CONTEXT:"
            match = re.search(
                r"```\s*\n(BRAND CONTEXT:[^`]+?)```",
                text,
                re.DOTALL,
            )
            if match:
                return match.group(1).strip()
    return ""


def render_prompt(brief: dict, pattern_name: str) -> str:
    """Render the full prompt with brand-specific variables substituted."""
    pattern = BASE_PATTERNS.get(pattern_name, BASE_PATTERNS["workflow-cinematic"])

    # Fill template with brief fields, with sensible defaults.
    # Prefer brief-provided values; only use defaults if brief didn't supply them.
    def val(key: str, default: str) -> str:
        # Check both raw key and lowercase variants
        return brief.get(key) or brief.get(key.lower()) or default

    # Smart mapping: brief's "Trade activity" or "Action" can fill either
    # trade_activity (for tradesperson-broll) or celebration_action
    # (for milestone-celebration), depending on what the pattern needs.
    action = val("action", val("trade_activity", val("celebration_action", "")))

    # Image-specific fields
    aspect = brief.get("aspect_ratio", "1:1")
    aspect_phrase = _aspect_phrase(aspect)
    text_overlay_clause = ""
    if brief.get("text_overlay"):
        text_overlay_clause = f"Include legible text: {brief['text_overlay']}"

    # De-dupe location/time of day when the brief includes both in location
    # Read raw values; if the brief supplied time_of_day, prefer it
    raw_time_of_day = brief.get("time_of_day") or brief.get("time of day")
    default_time = "natural afternoon"
    time_of_day = raw_time_of_day if raw_time_of_day else default_time
    location = val("location", "small London office").rstrip(".").strip()

    # Only de-dupe if the FULL time_of_day value (minus filler words like
    # "lighting", "light") is contained in location. A 2-word substring match
    # is too aggressive — drops meaningful info like "golden hour".
    cleaned_time = re.sub(r"\b(lighting|light)\b", "", time_of_day.lower()).strip()
    if cleaned_time and cleaned_time in location.lower():
        time_of_day = ""

    # De-dupe scene_description: if scene ends with "." and location starts with
    # the same content, strip the trailing period + space to avoid "..." duplication
    scene_description = val("scene_description", val("scene", "active construction site")).rstrip(".").strip()

    fields = {
        "duration": val("duration", "15"),
        "trade_activity": action or "tiling work in progress",
        "building_type": val("building_type", "Victorian terraced house"),
        "time_of_day": time_of_day or "natural afternoon",
        "person_description": val("person_description",
                                          "UK founder in their 30s, smart-casual"),
        "location": location,
        "celebration_action": action or "hand signing a milestone document",
        "surface": val("surface", "matte wooden desk"),
        "direction": val("direction", "upper-left"),
        "product_description": val("product_description",
                                           "laptop showing escrow dashboard"),
        "scene_description": scene_description,
        "surface_material": val("surface_material", val("material", "weathered brick")),
        # Image-specific
        "aspect_ratio_phrase": aspect_phrase,
        "text_overlay_clause": text_overlay_clause,
        "slide_num": val("slide_num", "1"),
        "slide_total": val("slide_total", "3"),
        "visual_register": val("visual_register", "documentary register, candid, no stock-photo feel"),
    }

    return pattern["template"].format(**fields)


def build_packet(brief: dict, model: str, post_num: int, week: str, brand: str = "") -> str:
    """Build a single packet file's contents. Format-aware (video vs image vs tv-spot)."""
    pattern_name = select_pattern(brief)
    pattern = BASE_PATTERNS[pattern_name]
    model_info = MODELS.get(model, MODELS["veo-3.1"])
    platform = brief.get("platform", "linkedin").lower()
    theme = brief.get("theme", "general").lower().replace(" ", "-")
    fmt = model_info.get("format", "video")
    aspect = brief.get("aspect_ratio",
                       "1:1" if platform == "linkedin" and fmt == "image" else
                       "9:16" if platform in ("tiktok", "instagram", "youtube") else
                       "16:9" if fmt == "video" else
                       "1:1")
    duration = str(brief.get("duration", 15))

    # TV-spot pattern takes its own renderer (richer structure)
    if pattern_name == "documentary-tv-spot":
        return _build_tv_spot_packet(
            brief, pattern, model, model_info, platform, theme, aspect, duration, post_num, week, brand
        )

    prompt = render_prompt(brief, pattern_name)

    # Image vs video packet structure
    if fmt == "image":
        return _build_image_packet(
            brief, pattern, model, model_info, platform, theme, aspect, prompt, post_num, week
        )
    return _build_video_packet(
        brief, pattern, model, model_info, platform, theme, aspect, duration, prompt, post_num, week
    )


def _build_image_packet(
    brief: dict, pattern: dict, model: str, model_info: dict,
    platform: str, theme: str, aspect: str, prompt: str,
    post_num: int, week: str,
) -> str:
    """Build a packet for a static image / carousel slide."""
    is_carousel = brief.get("format") == "carousel" or "carousel" in (brief.get("theme", "") or "").lower()
    slide_num = brief.get("slide_num", "1")
    slide_total = brief.get("slide_total", "3" if is_carousel else "1")
    file_ext = "jpg" if brief.get("format") != "carousel" else "png"
    return_filename = f"{week}-{post_num:02d}.{file_ext}"
    if is_carousel:
        return_filename = f"{week}-{post_num:02d}-slide-{slide_num}.{file_ext}"

    visual_register = brief.get("visual_register", "documentary, candid, UK")
    text_overlay_note = ""
    if brief.get("text_overlay") and model_info.get("supports_text_overlay"):
        text_overlay_note = (
            f"\n**Text overlay:** `{brief['text_overlay']}` — "
            f"render via `{model}` (supports text overlay)\n"
        )

    # Avoid "X register register holds" duplication if register is already in the value
    if "register" in visual_register.lower():
        accept_register = visual_register + " holds"
    else:
        accept_register = f"{visual_register} register holds"

    carousel_note = ""
    if is_carousel:
        carousel_note = (
            f"\n**Carousel:** Generate all {slide_total} slides. "
            "Keep visual style consistent across slides "
            "(same lighting, same register, same color temperature).\n"
        )

    accept_extra = []
    if is_carousel:
        accept_extra = [
            f"Slide {slide_num} of {slide_total} — visually consistent with sibling slides",
            "Reads correctly when stacked in LinkedIn carousel preview",
        ]

    return f"""# Packet {post_num:02d} — {platform} — {theme}{f' (carousel slide {slide_num}/{slide_total})' if is_carousel else ''}

> **Paste the prompt block into Higgsfield image model: `{model}`**
> **Settings: {aspect}, {brief.get("resolution", "2k")} resolution**
> **Your job: paste → download → rename to `{return_filename}` → drop in `brands/<brand>/inbox/`**
> **The agent handles everything else.**

---

## Settings

- **Model:** `{model}` ({model_info['best_for']})
- **Format:** {'carousel (single slide)' if is_carousel else 'single image'}
- **Aspect ratio:** {aspect}
- **Resolution:** {brief.get("resolution", "2k")}
- **Credit cost estimate:** ~{model_info.get('credit_cost_per_image', '?')} credits per image

## Prompt (copy everything below this line into the model's prompt field)

```
{prompt}
```
{text_overlay_note}{carousel_note}
## Accept if

- Clear focal point visible at thumbnail size
- {accept_register}
- No text overlays, no logos, no visible UI chrome (unless specified above)
- No AI-tell artifacts (uncanny stillness, smoothed textures, plastic skin)
- Reads correctly at LinkedIn feed size (~600px wide)
{chr(10).join(f"- {a}" for a in accept_extra)}

## Reject if

{chr(10).join(f"- {r}" for r in pattern['reject_if'])}
- Any visible watermark or AI-generation artifact
- Output doesn't match the prompt's setting (wrong location, wrong subject, etc.)
- Generic stock-photo aesthetic (this is the #1 tell)

## Return contract

Save the downloaded file as:

```
{return_filename}
```

Drop it in: `brands/{brief.get('brand', '<brand>')}/inbox/`

`pair_media.py` will scan inbox/, match this packet by filename, move it to the right
post folder, and update the post's status to `media-ready`.
"""


def _build_video_packet(
    brief: dict, pattern: dict, model: str, model_info: dict,
    platform: str, theme: str, aspect: str, duration: str, prompt: str,
    post_num: int, week: str,
) -> str:
    """Build a packet for a video asset."""
    audio_block = ""
    if model_info["supports_audio"]:
        audio_block = f"\n**Audio:** {pattern['audio_clause']}\n"

    return_filename = f"{week}-{post_num:02d}.{brief.get('extension', 'mp4')}"
    visual_register = brief.get("visual_register", "documentary, candid, UK")

    return f"""# Packet {post_num:02d} — {platform} — {theme}

> **Paste the prompt block into Higgsfield video model: `{model}`**
> **Settings: {aspect}, {duration}s**
> **Your job: paste → download → rename to `{return_filename}` → drop in `brands/<brand>/inbox/`**
> **The agent handles everything else.**

---

## Settings

- **Model:** `{model}` ({model_info['best_for']})
- **Aspect ratio:** {aspect}
- **Duration:** {duration}s
- **Credit cost estimate:** ~{model_info.get(f'credit_cost_{duration}s', '?')} credits

## Prompt (copy everything below this line into the model's prompt field)

```
{prompt}
```
{audio_block}
## Accept if

- Clear focal point visible in first frame
- Reads correctly at thumbnail size
- No text overlays, no logos, no visible UI chrome
- Brand-appropriate visual register ({visual_register})
- No speech (unless pattern explicitly allows)

## Reject if

{chr(10).join(f"- {r}" for r in pattern['reject_if'])}
- Any visible watermark or AI-generation artifact
- Output doesn't match the prompt's setting (wrong location, wrong action, etc.)

## Return contract

Save the downloaded file as:

```
{return_filename}
```

Drop it in: `brands/{brief.get('brand', '<brand>')}/inbox/`

`pair_media.py` will scan inbox/, match this packet by filename, move it to the right
post folder, and update the post's status to `media-ready`.
"""


def _build_compact_prompt(
    brand_prefix: str, scene_description: str, seg_block: str,
    negatives: list, end_card: str, max_chars: int = 2000,
) -> str:
    """
    Build a compact prompt that fits within Higgsfield's prompt-field char
    limit. Strategy:

    1. Compress the brand-prefix into a one-paragraph style brief.
    2. Compress negatives into a comma-separated inline list.
    3. Drop the verbose "DO NOT SHOW (negative prompts):" header —
       the inline list speaks for itself.
    4. Drop the verbose "ACTION SCRIPT:" header line — keep the
       bullet structure (model parses bullets just as well).
    5. Compress the end-card into a single line.
    6. If still too long, truncate the brand-prefix to fit.

    The full brand-context prefix and full negative list are preserved
    in the packet output (under "Brand context (reference only)" and
    "Full negative-prompt list"), so the human reviewer still sees them
    when running the accept/reject checklist.
    """
    # Step 1: compress brand-prefix to ~400-char style brief.
    # Extract palette hint, lighting hint, end-card hint, banned hint.
    style_brief = (
        "UK construction documentary, premium register, restrained "
        "handheld camera, shallow depth of field, natural window light. "
        "Warm clay + bone-white + slate charcoal + moss-green palette, "
        "no pure black, no purple-blue gradients. Final 2-3s: hard cut "
        "to a perfectly flat, motionless bone-white (#F2EDE5) frame, "
        "centre empty for AllSquared branding to be added in post."
    )
    # If brand_prefix is actually short enough, just use it as-is.
    # Otherwise fall back to the style_brief.
    brand_compact = brand_prefix if len(brand_prefix) <= 600 else style_brief

    # Step 2: negatives inline (drop header, keep list as one line)
    neg_inline = ", ".join(negatives) if negatives else ""

    # Step 3: end-card one-liner (drop the verbose "END-CARD FRAME" header)
    end_card_line = ""
    if end_card:
        # Pull just the first sentence
        first_sentence = end_card.split(".")[0].strip()
        end_card_line = (
            f"END-CARD: {first_sentence}. "
            f"Perfectly flat, motionless, centre empty for branding."
        )

    # Assemble
    parts = []
    parts.append(brand_compact)
    if scene_description:
        parts.append("")
        parts.append(f"SCENE: {scene_description}")
    if seg_block:
        parts.append("")
        # Step 4: drop the "ACTION SCRIPT:" header — model reads bullets fine.
        # The seg_block already contains "**0-3 seconds:** ..." lines.
        parts.append(seg_block)
    if neg_inline:
        parts.append("")
        # Step 4 (cont): drop "DO NOT SHOW" header, just inline the list.
        parts.append(f"NO: {neg_inline}.")
    if end_card_line:
        parts.append("")
        parts.append(end_card_line)

    compact = "\n".join(parts)

    # Step 5: if still over limit, hard-trim the brand_compact paragraph
    # to make room for the rest. Keep at least 200 chars of brand_compact
    # so the visual style still comes through.
    if len(compact) > max_chars:
        non_brand = "\n".join(parts[1:])  # everything except the first part
        # Reserve room for non_brand + a marker showing truncation
        marker = "\n\n[FULL BRAND CONTEXT IN PACKET — see 'Brand context (reference only)' below]"
        room_for_brand = max_chars - len(non_brand) - len(marker)
        if room_for_brand < 200:
            room_for_brand = 200  # never drop brand_compact below 200 chars
        brand_compact = brand_compact[:room_for_brand].rsplit(".", 1)[0] + "."
        parts[0] = brand_compact
        parts.append(marker)
        compact = "\n".join(parts)

    return compact


def _build_tv_spot_packet(
    brief: dict, pattern: dict, model: str, model_info: dict,
    platform: str, theme: str, aspect: str, duration: str,
    post_num: int, week: str, brand: str,
) -> str:
    """
    Build a packet for a documentary-style TV spot. Richer structure than
    a standard social video — renders segmented action script, explicit
    negative-prompt list, multi-layer audio architecture, end-card.

    The brief must carry:
      - segments: list of {start_s, end_s, description}
      - negative_prompts: list of strings (each is one "no X" item)
      - audio_layers: list of {layer, description} (e.g. Music, SFX, Room tone)
      - end_card: optional string describing the end-card frame

    The brand-context prefix is pulled from
    brands/<brand>/higgsfield/brand-context.md.
    """
    segments = brief.get("segments", [])
    negatives = brief.get("negative_prompts", [])
    audio_layers = brief.get("audio_layers", [])
    end_card = brief.get("end_card", "").strip()

    brand_prefix = load_brand_context(brand) if brand else ""

    # Render segmented action script
    if segments:
        seg_lines = []
        for seg in segments:
            start = seg.get("start_s", "?")
            end = seg.get("end_s", "?")
            desc = seg.get("description", "").strip()
            seg_lines.append(f"- **{start}-{end} seconds:** {desc}")
        seg_block = "\n".join(seg_lines)
    else:
        seg_block = "_No action-script segments provided in the brief. Add them under `- Action script:` with `0-3s: ...` sub-bullets._"

    # Render negative prompts
    if negatives:
        neg_block = "\n".join(f"- {n}" for n in negatives)
    else:
        neg_block = "_No negative-prompt list provided. Add `Negative prompts:` or `Do not show:` to the brief, with `- No X` lines._"

    # Render audio architecture
    if audio_layers:
        audio_lines = []
        for layer in audio_layers:
            lname = layer.get("layer", "Audio").capitalize()
            ldesc = layer.get("description", "").strip()
            audio_lines.append(f"- **{lname}:** {ldesc}")
        audio_block = "\n".join(audio_lines)
    else:
        audio_block = "_No audio architecture provided in the brief. Add `Audio:` with sub-bullets like `- Music: ...`, `- SFX: ...`, `- Room tone: ...`._"

    # Render end-card
    if end_card:
        end_card_block = (
            f"## End-card frame (final 2-3 seconds)\n\n"
            f"{end_card}\n\n"
            f"Generate the end-card as a STATIC frame. Hold it for the last 2-3 seconds of the video. "
            f"Leave the centre empty — the brand wordmark is added in post.\n"
        )
    else:
        end_card_block = (
            "## End-card frame (final 2-3 seconds)\n\n"
            "_No end-card specification in the brief. Add `End card:` with a description like "
            "'perfectly flat, motionless bone-white (#F2EDE5) background, no person, no logo, no text, centre empty for branding.'_\n"
        )

    # Optional subject description (if brief carries a `subject` or `scene_description`)
    scene_description = brief.get("scene_description") or brief.get("subject") or ""

    # Higgsfield's prompt field has a hard character limit (~2000 chars on most
    # video models). When the rendered full prompt exceeds the limit, fall back
    # to a compact form: condensed brand-context + scene + action script +
    # negatives joined inline. The full brand-context prefix remains in the
    # packet under "Brand context (reference only)" so the accept/reject
    # checklist can still enforce those rules.
    HIGGSFIELD_MAX_PROMPT = 2000

    full_prompt_lines = []
    if brand_prefix:
        full_prompt_lines.append(brand_prefix)
    if scene_description:
        full_prompt_lines.append("")
        full_prompt_lines.append(f"SCENE: {scene_description}")
    if seg_block:
        full_prompt_lines.append("")
        full_prompt_lines.append("ACTION SCRIPT:")
        full_prompt_lines.append(seg_block)
    if negatives:
        full_prompt_lines.append("")
        full_prompt_lines.append("DO NOT SHOW (negative prompts):")
        full_prompt_lines.append(neg_block)
    if end_card:
        full_prompt_lines.append("")
        full_prompt_lines.append("END-CARD FRAME (final 2-3 seconds):")
        full_prompt_lines.append(end_card)

    full_prompt = "\n".join(full_prompt_lines)

    # If full prompt exceeds the limit, build a compact version that fits
    use_compact = len(full_prompt) > HIGGSFIELD_MAX_PROMPT
    if use_compact:
        full_prompt = _build_compact_prompt(
            brand_prefix, scene_description, seg_block, negatives, end_card,
            max_chars=HIGGSFIELD_MAX_PROMPT,
        )

    return_filename = f"{week}-{post_num:02d}.{brief.get('extension', 'mp4')}"

    return f"""# Packet {post_num:02d} — {platform} — {theme} (TV spot)

> **Paste the prompt block into Higgsfield video model: `{model}`**
> **Settings: {aspect}, {duration}s**
> **Your job: paste → download → rename to `{return_filename}` → drop in `brands/{brand}/inbox/`**
> **The agent handles everything else.**

---

## Settings

- **Model:** `{model}` ({model_info['best_for']})
- **Format:** documentary TV spot (segmented action script)
- **Aspect ratio:** {aspect}
- **Duration:** {duration}s
- **Credit cost estimate:** ~{model_info.get(f'credit_cost_{duration}s', '?')} credits

## Brand context prefix (REFERENCE ONLY — already condensed into the pasted prompt)

{(brand_prefix if brand_prefix else "_⚠️ No brand-context prefix loaded. Add a fenced code block starting with `BRAND CONTEXT:` to `brands/" + brand + "/higgsfield/brand-context.md`._")}

## Scene description

{scene_description or "_No scene_description in brief. Add `- Scene description:` line._"}

## Action script (paste this with the prompt)

{seg_block}

## Negative prompts (REFERENCE ONLY — already condensed into the pasted prompt)

{neg_block}

## Audio architecture (paste this with the prompt)

{audio_block}

{end_card_block}

## Full prompt (copy everything below this line into the model's prompt field)

**Prompt length:** {len(full_prompt)} chars (Higgsfield limit: {HIGGSFIELD_MAX_PROMPT})
{f"**⚠️ COMPACT MODE** — full prompt exceeded the {HIGGSFIELD_MAX_PROMPT}-char Higgsfield limit, so brand-context and negatives are condensed. The full versions are preserved below for the accept/reject checklist." if use_compact else ""}

```
{full_prompt}
```

## Brand context (reference only — already condensed into the prompt above)

{(brand_prefix if brand_prefix else "_No brand-context prefix loaded._")}

## Full negative-prompt list (reference only — already condensed into the prompt above)

{neg_block}

## Accept if

- Reads as documentary, not stock-photo
- Each segment lands in its assigned N-Ns window
- Subject is consistent across all segments
- Audio layers land at the right moments (the phone ring at the start, the chime at the end, no random dialogue in the middle)
- The end-card frame is exactly as specified (flat, motionless, centred-empty)
- No speech, voiceover, captions, on-screen text, watermarks, or generated logos anywhere in the video
- Realistic skin, real hands, natural window light — no AI-tell artifacts

## Reject if

{chr(10).join(f"- {r}" for r in pattern['reject_if'])}
- Any segment is wrong / missing / out of order
- Any negative prompt appears in the output (medical equipment, uniforms, etc.)
- Audio has random dialogue, music swell, or notification sounds
- The end-card is not flat / has gradient / has shadow / has a generated logo
- Anything in the BANNED section of the brand-context prefix appears

## Return contract

Save the downloaded file as:

```
{return_filename}
```

Drop it in: `brands/{brand}/inbox/`

`pair_media.py` will scan inbox/, match this packet by filename, move it to the right
post folder, and update the post's status to `media-ready`.
"""


def parse_media_briefs(week_path: Path) -> list[dict]:
    """
    Parse the week's media-briefs.md into per-post dicts.

    Captures:
    - Top-level key-value fields (existing)
    - Negative-prompt lists under 'Negative prompts:' or 'Do not show:'
      or any 'no_*' field
    - Segmented action script under 'Action script:' or 'Segments:'
      with 'N-Ns:' sub-bullets
    - Multi-line Audio architecture
    - End-card placeholder
    """
    if not week_path.exists():
        return []
    text = week_path.read_text()

    # Split on ### post headers
    parts = re.split(r"(?=^###\s+\d+\.)", text, flags=re.MULTILINE)
    briefs = []
    for part in parts:
        if not part.strip():
            continue
        brief = {"raw": part}
        # Extract numbered post header
        m = re.match(r"^###\s+(\d+)\.\s+(.+)", part)
        if m:
            brief["post_num"] = int(m.group(1))
            brief["title"] = m.group(2).strip()
            # Extract theme from header if present (e.g. "1. LinkedIn retention")
            header_parts = m.group(2).strip().split(maxsplit=1)
            if len(header_parts) > 1:
                brief["theme"] = header_parts[1].strip()

        # Parse key-value fields (accept both "- **Field:** value" and "- Field: value")
        # Also capture negative-prompt lists and action-script segments below.
        in_action_script = False
        in_audio_block = False
        in_negatives_block = False
        in_end_card_block = False
        current_segment_seconds = None
        current_audio_layer = None
        for line in part.split("\n"):
            stripped = line.strip()
            if not stripped:
                in_action_script = False
                in_audio_block = False
                in_negatives_block = False
                in_end_card_block = False
                current_segment_seconds = None
                current_audio_layer = None
                continue

            # Detect section headers
            lower = stripped.lower()
            if re.match(r"-\s+\*?\*?(negative|do not show|avoid|never show)\s*(prompts?)?:\*?\*?\s*$", lower):
                in_negatives_block = True
                in_action_script = in_audio_block = in_end_card_block = False
                brief.setdefault("negative_prompts", [])
                continue
            if re.match(r"-\s+\*?\*?(action script|segments?|timeline|shot list):\*?\*?\s*$", lower):
                in_action_script = True
                in_audio_block = in_negatives_block = in_end_card_block = False
                brief.setdefault("segments", [])
                continue
            if re.match(r"-\s+\*?\*?(audio|sound|music):\*?\*?\s*$", lower):
                in_audio_block = True
                in_action_script = in_negatives_block = in_end_card_block = False
                brief.setdefault("audio_layers", [])
                continue
            if re.match(r"-\s+\*?\*?(end\s*card|endcard|branded\s*frame):\*?\*?\s*$", lower):
                in_end_card_block = True
                in_action_script = in_audio_block = in_negatives_block = False
                brief["end_card"] = ""
                continue

            # Action-script segment: "0-3s: ..." or "0–3 seconds: ..."
            # The optional unit (s/sec/seconds) is captured separately; the trailing
            # ":" is also optional. We strip the captured unit from the start of the
            # description so "0-3 seconds: foo" becomes start=0, end=3, desc="foo".
            if in_action_script:
                seg_match = re.match(
                    r"-\s*(\d+)\s*[-–]\s*(\d+)\s*(seconds|sec|s)?\s*:?\s*(.+)?$",
                    stripped,
                    re.IGNORECASE,
                )
                if seg_match:
                    start_s = int(seg_match.group(1))
                    end_s = int(seg_match.group(2))
                    desc = (seg_match.group(4) or "").strip()
                    # Strip a leading "s:" / "sec:" / "seconds:" prefix that
                    # may have been left when no colon was used
                    desc = re.sub(r"^(seconds|sec|s)\s*:?\s*", "", desc, flags=re.IGNORECASE).strip()
                    brief["segments"].append({
                        "start_s": start_s, "end_s": end_s, "description": desc
                    })
                    continue
                # Continuation of previous segment (line not starting with N-Ns)
                if brief["segments"]:
                    brief["segments"][-1]["description"] += " " + stripped.lstrip("-").strip()
                    continue

            # Audio layer: "Music: ..." or "SFX: ..." or "Voice: ..."
            if in_audio_block:
                layer_match = re.match(r"-\s*\*?\*?(.+?):\*?\*?\s*(.+)$", stripped)
                if layer_match:
                    current_audio_layer = layer_match.group(1).strip().lower()
                    brief["audio_layers"].append({
                        "layer": current_audio_layer,
                        "description": layer_match.group(2).strip()
                    })
                    continue
                # Continuation
                if brief["audio_layers"]:
                    brief["audio_layers"][-1]["description"] += " " + stripped.lstrip("-").strip()
                    continue

            # Negative prompt: "- No X" or "- Never show Y" or "- Do not include Z"
            if in_negatives_block:
                neg_match = re.match(r"-\s*(.+)$", stripped)
                if neg_match:
                    neg_text = neg_match.group(1).strip()
                    # Strip leading "No ", "Never show ", "Do not include "
                    neg_text = re.sub(r"^(no|never show|do not include|never)\s+", "", neg_text, flags=re.IGNORECASE)
                    brief["negative_prompts"].append(neg_text)
                    continue

            # End-card content
            if in_end_card_block:
                brief["end_card"] += (brief.get("end_card", "") + " " + stripped.lstrip("-").strip()).strip()
                continue

            # Default: key-value field
            kv = re.match(r"-\s+\*?\*?(.+?):\*?\*?\s+(.+)", stripped)
            if kv:
                key = kv.group(1).strip().lower().replace(" ", "_")
                brief[key] = kv.group(2).strip()
        briefs.append(brief)
    return briefs


def expand_carousel_briefs(briefs: list[dict]) -> list[dict]:
    """
    Expand a carousel brief into multiple per-slide briefs.
    Slides are listed under the brief's raw text starting with '- Slide N:'.
    Returns the original briefs list with carousel briefs replaced by
    one brief per slide.
    """
    expanded = []
    for brief in briefs:
        fmt = (brief.get("format") or "").lower()
        if fmt != "carousel":
            expanded.append(brief)
            continue
        # Find slide lines in the raw text
        slide_lines = re.findall(r"^-\s+Slide\s+(\d+):\s*(.+)$", brief.get("raw", ""), re.MULTILINE)
        if not slide_lines:
            expanded.append(brief)
            continue
        slide_total = len(slide_lines)
        for slide_num_str, slide_desc in slide_lines:
            slide_brief = dict(brief)
            slide_brief["slide_num"] = int(slide_num_str)
            slide_brief["slide_total"] = slide_total
            slide_brief["scene_description"] = slide_desc.strip()
            expanded.append(slide_brief)
    return expanded


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate prompt packets")
    parser.add_argument("--brand", required=True)
    parser.add_argument("--week", required=True, help="e.g., 2026-W30")
    parser.add_argument("--model", default=None, help="Override model for all packets")
    parser.add_argument("--out", default=None, help="Output directory (default: week folder)")
    args = parser.parse_args()

    brand_dir = REPO_ROOT / "brands" / args.brand
    if not brand_dir.exists():
        print(f"ERROR: brands/{args.brand}/ not found", file=sys.stderr)
        sys.exit(1)

    week_dir = brand_dir / "weeks" / args.week
    if not week_dir.exists():
        print(f"ERROR: {week_dir} not found", file=sys.stderr)
        sys.exit(1)

    briefs_path = week_dir / "media-briefs.md"
    if not briefs_path.exists():
        print(f"ERROR: {briefs_path} not found", file=sys.stderr)
        sys.exit(1)

    briefs = parse_media_briefs(briefs_path)
    if not briefs:
        print(f"ERROR: no briefs parsed from {briefs_path}", file=sys.stderr)
        sys.exit(1)

    # Expand carousel briefs into per-slide briefs
    briefs = expand_carousel_briefs(briefs)

    out_dir = Path(args.out) if args.out else week_dir / "media-packets"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== Generating {len(briefs)} packet(s) for {args.brand} {args.week} ===\n")

    for i, brief in enumerate(briefs, 1):
        post_num = brief.get("post_num", i)
        model = select_model(brief, args.model)
        packet = build_packet(brief, model, post_num, args.week, brand=args.brand)

        platform = brief.get("platform", "linkedin").lower()
        theme = brief.get("theme", "general").lower().replace(" ", "-")
        # Filename suffix for carousel slides
        if brief.get("slide_num"):
            out_path = out_dir / f"{post_num:02d}-{platform}-{theme}-slide-{brief['slide_num']}.md"
        else:
            out_path = out_dir / f"{post_num:02d}-{platform}-{theme}.md"
        out_path.write_text(packet)
        slide_marker = f" (slide {brief['slide_num']}/{brief.get('slide_total', '?')})" if brief.get("slide_num") else ""
        print(f"  ✓ {out_path.relative_to(REPO_ROOT)}  (model: {model}){slide_marker}")

    print(f"\n=== Done. {len(briefs)} packets ready. ===\n")
    print("Next: paste each packet into Higgsfield UI → download → rename → drop in inbox/")
    print(f"Then run: python scripts/pair_media.py --brand {args.brand}")


if __name__ == "__main__":
    main()