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
MODELS = {
    "veo-3.1": {
        "credit_cost_8s": 50,
        "max_duration_s": 60,
        "supports_audio": True,
        "best_for": "Cinematic 8s shots, documentary-style, default video model",
    },
    "seedance-2.0-4k": {
        "credit_cost_15s": 200,
        "max_duration_s": 30,
        "supports_audio": False,
        "best_for": "Premium 4K footage, hero shots, high-fidelity product shots",
    },
    "kling-3.0": {
        "credit_cost_15s": 150,
        "max_duration_s": 30,
        "supports_audio": False,
        "best_for": "Strong human motion, image-to-video with keyframe control",
    },
    "sora-2-max": {
        "credit_cost_15s": 250,
        "max_duration_s": 30,
        "supports_audio": True,
        "best_for": "Physics consistency, complex scenes (use sparingly)",
    },
    "grok-video": {
        "credit_cost_15s": 80,
        "max_duration_s": 15,
        "supports_audio": False,
        "best_for": "Quick drafts, 16:9 only (NOT for vertical)",
    },
    "hailuo-2.3": {
        "credit_cost_15s": 100,
        "max_duration_s": 30,
        "supports_audio": False,
        "best_for": "Strong human motion/expression (when humans are in frame)",
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
}


def select_pattern(brief: dict) -> str:
    """Pick a base pattern from the brief's pattern hint or platform."""
    hint = brief.get("pattern", "").strip().lower()
    if hint in BASE_PATTERNS:
        return hint

    # Default selection by platform
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
    return brief.get("model", "veo-3.1")


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

    fields = {
        "duration": val("duration", "15"),
        "trade_activity": action or "tiling work in progress",
        "building_type": val("building_type", "Victorian terraced house"),
        "time_of_day": val("time_of_day", "natural afternoon"),
        "person_description": val("person_description",
                                          "UK founder in their 30s, smart-casual"),
        "location": val("location", "small London office"),
        "celebration_action": action or "hand signing a milestone document",
        "surface": val("surface", "matte wooden desk"),
        "direction": val("direction", "upper-left"),
        "product_description": val("product_description",
                                           "laptop showing escrow dashboard"),
        "scene_description": val("scene_description",
                                          val("scene", "active construction site")),
        "surface_material": val("surface_material", val("material", "weathered brick")),
    }

    return pattern["template"].format(**fields)


def build_packet(brief: dict, model: str, post_num: int, week: str) -> str:
    """Build a single packet file's contents."""
    pattern_name = select_pattern(brief)
    pattern = BASE_PATTERNS[pattern_name]
    model_info = MODELS.get(model, MODELS["veo-3.1"])
    platform = brief.get("platform", "linkedin").lower()
    theme = brief.get("theme", "general").lower().replace(" ", "-")
    aspect = brief.get("aspect_ratio", "1:1" if platform == "linkedin" else
                       "9:16" if platform in ("tiktok", "instagram", "youtube") else
                       "16:9")

    duration = str(brief.get("duration", 15))
    prompt = render_prompt(brief, pattern_name)

    # Audio clause: only if model supports audio
    audio_block = ""
    if model_info["supports_audio"]:
        audio_block = f"\n**Audio:** {pattern['audio_clause']}\n"

    # Return filename contract
    return_filename = f"{week}-{post_num:02d}.{brief.get('extension', 'mp4')}"

    packet = f"""# Packet {post_num:02d} — {platform} — {theme}

> **Paste the prompt block into Higgsfield model: `{model}`**
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
- Brand-appropriate visual register ({brief.get('visual_register', 'documentary, candid, UK')})
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
    return packet


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

    out_dir = Path(args.out) if args.out else week_dir / "media-packets"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== Generating {len(briefs)} packet(s) for {args.brand} {args.week} ===\n")

    for i, brief in enumerate(briefs, 1):
        post_num = brief.get("post_num", i)
        model = select_model(brief, args.model)
        packet = build_packet(brief, model, post_num, args.week)

        platform = brief.get("platform", "linkedin").lower()
        theme = brief.get("theme", "general").lower().replace(" ", "-")
        out_path = out_dir / f"{post_num:02d}-{platform}-{theme}.md"
        out_path.write_text(packet)
        print(f"  ✓ {out_path.relative_to(REPO_ROOT)}  (model: {model})")

    print(f"\n=== Done. {len(briefs)} packets ready. ===\n")
    print("Next: paste each packet into Higgsfield UI → download → rename → drop in inbox/")
    print(f"Then run: python scripts/pair_media.py --brand {args.brand}")


if __name__ == "__main__":
    main()