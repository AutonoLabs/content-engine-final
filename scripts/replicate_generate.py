#!/usr/bin/env python3
"""
replicate_generate — automated image path (no human in the loop).

Higgsfield stays the manual packet/inbox flow for video; images and carousel
slides route through the Replicate HTTP API so image-format posts are fully
automated end to end.

Env: REPLICATE_API_TOKEN

Usage:
    python scripts/replicate_generate.py --brand allsquared --week 2026-W31 \
        --prompt "..." --slug 01-linkedin-hero
    # writes brands/<brand>/weeks/<week>/assets/<slug>.png

    # Or batch from a media-briefs.md (uses each brief's Scene description):
    python scripts/replicate_generate.py --brand allsquared --week 2026-W31 --from-briefs
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time

import requests

from brand_config import REPO_ROOT, week_dir

DEFAULT_MODEL = "black-forest-labs/flux-1.1-pro"
API = "https://api.replicate.com/v1"


def _headers() -> dict:
    token = os.getenv("REPLICATE_API_TOKEN")
    if not token:
        sys.exit("ERROR: REPLICATE_API_TOKEN not set (see docs/ENV-WIRING.md)")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def generate(prompt: str, model: str, aspect_ratio: str = "1:1") -> bytes:
    r = requests.post(
        f"{API}/models/{model}/predictions",
        headers={**_headers(), "Prefer": "wait=60"},
        json={"input": {"prompt": prompt, "aspect_ratio": aspect_ratio,
                        "output_format": "png"}},
        timeout=120,
    )
    r.raise_for_status()
    pred = r.json()
    while pred["status"] in ("starting", "processing"):
        time.sleep(2)
        pred = requests.get(f"{API}/predictions/{pred['id']}",
                            headers=_headers(), timeout=30).json()
    if pred["status"] != "succeeded":
        sys.exit(f"ERROR: prediction {pred['status']}: {pred.get('error')}")
    output = pred["output"]
    url = output[0] if isinstance(output, list) else output
    img = requests.get(url, timeout=60)
    img.raise_for_status()
    return img.content


def briefs_prompts(brand: str, week: str) -> list[tuple[str, str, str]]:
    """(slug, prompt, aspect_ratio) per image-format brief in media-briefs.md."""
    path = week_dir(brand, week) / "media-briefs.md"
    if not path.exists():
        sys.exit(f"ERROR: {path} not found")
    out = []
    blocks = re.split(r"(?=^### )", path.read_text(), flags=re.MULTILINE)
    for block in blocks:
        head = re.match(r"### \d+\.\s*(.+)", block)
        fmt = re.search(r"- Format:\s*(\S+)", block)
        scene = re.search(r"- Scene description:\s*(.+)", block)
        ar = re.search(r"- Aspect ratio:\s*(\S+)", block)
        if not (head and fmt and scene):
            continue
        if "image" not in fmt.group(1) and "carousel" not in fmt.group(1):
            continue  # video formats stay on the Higgsfield packet path
        slug = re.sub(r"[^a-z0-9]+", "-", head.group(1).lower()).strip("-")
        out.append((slug, scene.group(1).strip(), ar.group(1) if ar else "1:1"))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Automated image generation")
    parser.add_argument("--brand", required=True)
    parser.add_argument("--week", required=True)
    parser.add_argument("--prompt")
    parser.add_argument("--slug", help="Output filename (without extension)")
    parser.add_argument("--from-briefs", action="store_true",
                        help="Generate all image-format briefs in media-briefs.md")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--aspect-ratio", default="1:1")
    args = parser.parse_args()

    try:
        from dotenv import load_dotenv
        load_dotenv(REPO_ROOT / ".env")
    except ImportError:
        pass

    assets = week_dir(args.brand, args.week) / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    jobs: list[tuple[str, str, str]] = []
    if args.from_briefs:
        jobs = briefs_prompts(args.brand, args.week)
        if not jobs:
            print("No image-format briefs found.")
            return
    else:
        if not args.prompt or not args.slug:
            sys.exit("ERROR: --prompt and --slug required (or use --from-briefs)")
        jobs = [(args.slug, args.prompt, args.aspect_ratio)]

    for slug, prompt, ar in jobs:
        print(f"→ {slug} ({ar}) via {args.model}")
        data = generate(prompt, args.model, ar)
        out = assets / f"{slug}.png"
        out.write_bytes(data)
        print(f"  ✓ {out.relative_to(REPO_ROOT)} ({len(data) // 1024} KB)")


if __name__ == "__main__":
    main()
