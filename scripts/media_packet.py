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


def build_packet(brief: dict, model: str, post_num: int, week: str) -> str:
    """Build a single packet file's contents. Format-aware (video vs image)."""
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


def parse_media_briefs(week_path: Path) -> list[dict]:
    """Parse the week's media-briefs.md into per-post dicts."""
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
        for line in part.split("\n"):
            kv = re.match(r"-\s+\*?\*?(.+?):\*?\*?\s+(.+)", line.strip())
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
        packet = build_packet(brief, model, post_num, args.week)

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