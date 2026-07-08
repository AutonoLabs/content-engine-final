#!/usr/bin/env python3
"""
Generate video media via Higgsfield.

Usage:
    python scripts/higgsfield_generate.py \
        --model kling-3.0 \
        --prompt "A founder explaining escrow on a construction site" \
        --output brands/yapper/inbox/w28-post1.mp4 \
        --duration 15 \
        --aspect-ratio 9:16

    # From a media brief file:
    python scripts/higgsfield_generate.py \
        --brief brands/yapper/weeks/2026-W28/media-briefs.md

    # List available models:
    python scripts/higgsfield_generate.py --list-models
"""

import argparse
import os
import sys
import requests
from typing import Optional
from dotenv import load_dotenv  # noqa: E402


AVAILABLE_MODELS = {
    "kling-3.0": {"credit_cost_per_sec": 2, "max_duration": 30, "supports_4k": False},
    "seedance-2.0-4k": {"credit_cost_per_sec": 4, "max_duration": 30, "supports_4k": True},
    "veo-3.1": {"credit_cost_per_sec": 3, "max_duration": 60, "supports_4k": False},
    "sora-2-max": {"credit_cost_per_sec": 5, "max_duration": 60, "supports_4k": False},
    "grok-video": {"credit_cost_per_sec": 1, "max_duration": 15, "supports_4k": False},
    "hailuo-2.3": {"credit_cost_per_sec": 2, "max_duration": 30, "supports_4k": False},
}


def generate_video(
    api_key: str,
    model: str,
    prompt: str,
    duration: int,
    aspect_ratio: str,
    output_path: str,
    credit_mode: bool = True
) -> str:
    """
    Call Higgsfield API to generate video.

    Returns: URL of generated video (then downloaded to output_path).
    """
    if model not in AVAILABLE_MODELS:
        raise ValueError(f"Unknown model: {model}. Use --list-models.")

    model_info = AVAILABLE_MODELS[model]
    if duration > model_info["max_duration"]:
        print(f"⚠️  Duration {duration}s exceeds model max {model_info['max_duration']}s. Clamping.")
        duration = model_info["max_duration"]

    if not credit_mode:
        print("⚠️  WARNING: --credit-mode false violates Higgsfield ToS for automation.")
        print("    Unlimited features are gated against automation. Use --credit-mode true.")
        sys.exit(1)

    estimated_credits = duration * model_info["credit_cost_per_sec"]
    print(f"Generating with {model} (duration={duration}s, ratio={aspect_ratio})")
    print(f"Estimated cost: {estimated_credits} credits")

    # Higgsfield API call (placeholder — adjust to actual API spec)
    response = requests.post(
        "https://api.higgsfield.ai/v1/generate",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "credit_mode": True  # Always true for automation
        },
        timeout=300
    )
    response.raise_for_status()
    result = response.json()

    video_url = result.get("video_url")
    if not video_url:
        raise RuntimeError(f"No video_url in response: {result}")

    # Download to output path
    video_response = requests.get(video_url, timeout=120)
    video_response.raise_for_status()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(video_response.content)

    print(f"✅ Saved to {output_path}")
    print(f"   Credits used: {result.get('credits_used', 'unknown')}")
    return output_path


def parse_brief(brief_path: str) -> list:
    """Parse a media-briefs.md file and return list of brief dicts."""
    # Simple parser — looks for ## headers + structured fields
    import re
    with open(brief_path) as f:
        content = f.read()

    briefs = []
    sections = re.split(r"\n## ", content)

    for section in sections[1:]:  # skip preamble
        lines = section.split("\n")
        title = lines[0].strip()

        brief = {"title": title}
        for line in lines[1:]:
            if ":" in line:
                key, _, value = line.partition(":")
                key = key.strip("- ").strip().lower().replace(" ", "_")
                brief[key] = value.strip()

        briefs.append(brief)

    return briefs


def main():
    parser = argparse.ArgumentParser(description="Generate video via Higgsfield")
    parser.add_argument("--model", help="Model name (e.g., kling-3.0)")
    parser.add_argument("--prompt", help="Generation prompt")
    parser.add_argument("--duration", type=int, default=15, help="Duration in seconds")
    parser.add_argument("--aspect-ratio", default="9:16", help="e.g., 9:16, 16:9, 1:1")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--brief", help="Path to media-briefs.md file")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--credit-mode", type=lambda x: x.lower() == "true", default=True,
                        help="Use credit mode (MUST be true for automation)")

    args = parser.parse_args()

    if args.list_models:
        print("\n=== Available Models ===\n")
        for name, info in AVAILABLE_MODELS.items():
            cost = info["credit_cost_per_sec"]
            max_dur = info["max_duration"]
            four_k = "4K" if info["supports_4k"] else "HD"
            print(f"  {name}: {cost} credits/sec, max {max_dur}s, {four_k}")
        print("\nNOTE: Automation workflows MUST use credit mode. Unlimited features are gated.")
        return

    # Only load .env when actually generating (not for --list-models)
    load_dotenv()

    api_key = os.getenv("HIGGSFIELD_API_KEY")
    if not api_key:
        print("❌ HIGGSFIELD_API_KEY not found in .env", file=sys.stderr)
        sys.exit(1)

    if args.brief:
        # Batch mode: generate all briefs in file
        briefs = parse_brief(args.brief)
        print(f"Found {len(briefs)} briefs in {args.brief}\n")

        for i, brief in enumerate(briefs, 1):
            print(f"[{i}/{len(briefs)}] {brief.get('title', 'untitled')}")
            try:
                generate_video(
                    api_key=api_key,
                    model=brief.get("model", args.model or "kling-3.0"),
                    prompt=brief.get("prompt", brief.get("description", "")),
                    duration=int(brief.get("duration", 15)),
                    aspect_ratio=brief.get("aspect_ratio", "9:16"),
                    output_path=brief.get("output_path", f"output_{i}.mp4"),
                    credit_mode=args.credit_mode
                )
            except Exception as e:
                print(f"  ❌ Failed: {e}")
            print()

    elif args.prompt and args.output:
        # Single generation
        try:
            generate_video(
                api_key=api_key,
                model=args.model or "kling-3.0",
                prompt=args.prompt,
                duration=args.duration,
                aspect_ratio=args.aspect_ratio,
                output_path=args.output,
                credit_mode=args.credit_mode
            )
        except Exception as e:
            print(f"❌ Failed: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()