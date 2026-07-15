#!/usr/bin/env python3
"""
Onboard a new brand to the content engine.

Usage:
    python scripts/onboard_brand.py --name yapper --sector fintech

This will:
1. Validate brand name (no path traversal, no punctuation leaks)
2. Create brands/<name>/ folder structure (anchored to repo root)
3. Copy templates (verified present before any creation)
4. Print next-step checklist

Robustness (v1.3):
- Anchored to REPO_ROOT via Path(__file__).resolve().parent.parent
  (works from any cwd)
- Brand name validated against regex (lowercase letters, digits, hyphens)
- Path traversal refused: --name "../evil" exits with error
- Refuses to create if brand folder already exists
- Verifies ALL templates exist BEFORE creating any folders (no half-onboarded husks)
- Drops .gitkeep into inbox + exemplars/edits so they survive git
"""

import argparse
import re
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BRANDS_DIR = REPO_ROOT / "brands"

# Templates live in brands/<template>.md
TEMPLATES = [
    "voice-profile.template.md",
    "target-audience.template.md",
    "verified-facts.template.md",
    "content-mix.template.md",
    "performance-log.template.md",
    "brand-brief.template.md",
    "blotato-accounts.template.md",
]


def validate_brand_name(raw: str) -> str:
    """
    Lowercase, hyphens, alphanumerics only. No path separators.
    Returns canonical name; raises SystemExit on bad input.
    """
    name = raw.lower().strip().replace(" ", "-")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,40}", name):
        sys.exit(
            f"❌ Invalid brand name '{raw}'.\n"
            "   Use lowercase letters, digits, and hyphens only.\n"
            "   Must start with a letter or digit. Max 41 chars."
        )
    return name


def main() -> None:
    parser = argparse.ArgumentParser(description="Onboard new brand")
    parser.add_argument("--name", required=True,
                        help="Brand name (lowercase, digits, hyphens)")
    parser.add_argument("--sector", required=True,
                        choices=["consumer_health", "fintech", "legal",
                                 "professional", "education", "creative", "other"],
                        help="Industry sector")
    args = parser.parse_args()

    brand_name = validate_brand_name(args.name)

    if not BRANDS_DIR.exists():
        sys.exit(f"❌ Brands directory not found: {BRANDS_DIR}\n"
                 f"   Are you in the content-engine-final repo root?")

    brand_path = (BRANDS_DIR / brand_name).resolve()

    # Path-traversal guard: brand_path must be inside BRANDS_DIR
    if BRANDS_DIR.resolve() not in brand_path.parents:
        sys.exit(f"❌ Brand path escapes brands/ — refusing.\n"
                 f"   Resolved: {brand_path}")

    if brand_path.exists():
        sys.exit(f"❌ {brand_path} already exists.\n"
                 f"   Delete it or pick a different name.")

    # Verify ALL templates exist BEFORE creating anything (no husks)
    missing = [t for t in TEMPLATES if not (BRANDS_DIR / t).exists()]
    if missing:
        sys.exit(f"❌ Missing templates in {BRANDS_DIR}:\n"
                 f"   {missing}\n"
                 f"   Are you in a clean checkout of the repo?")

    print(f"\n=== Onboarding brand: {brand_name} ===\n")
    print(f"  Sector: {args.sector}")
    print(f"  Repo root: {REPO_ROOT}\n")

    # Create folder structure
    for sub in ["weeks", "exemplars/edits", "inbox"]:
        d = brand_path / sub
        d.mkdir(parents=True, exist_ok=True)
        # .gitkeep so the folder survives git without committing real files
        (d / ".gitkeep").touch()
        print(f"  ✓ Created {brand_path / sub}/")

    # Copy templates
    for template in TEMPLATES:
        src = BRANDS_DIR / template
        dst_name = template.replace(".template.md", ".md")
        dst = brand_path / dst_name
        shutil.copy(src, dst)
        print(f"  ✓ Copied {template} → {dst_name}")

    # Print next steps
    print(f"\n=== Next steps for {brand_name} ===\n")
    print(f"  1. Edit brand brief: brands/{brand_name}/brand-brief.md")
    print(f"  2. Apply voice-from-brief skill (skills/voice-from-brief.md)")
    print(f"     → fills in brands/{brand_name}/voice-profile.md")
    print(f"  3. Fill target audience:")
    print(f"     → use docs/audience-demographics.md as baseline")
    print(f"     → override for {brand_name}-specific segments in target-audience.md")
    print(f"  4. Set up verified-facts.md sector rules:")
    print(f"     → read skills/claim-verifier.md")
    print(f"     → apply '{args.sector}' sector rules to verified-facts.md")
    print(f"  5. Wire Blotato accounts:")
    print(f"     → connect accounts in Blotato dashboard")
    print(f"     → run: python scripts/blotato_list_accounts.py")
    print(f"     → document IDs in brands/{brand_name}/blotato-accounts.md")
    print(f"  6. Plan first batch:")
    print(f"     → read docs/WEEKLY-BATCH-FLOW.md")
    print(f"     → pick theme, draft 3-5 posts across platforms")
    print(f"     → validate before each publish:")
    print(f"       python scripts/validate_post.py --brand {brand_name} "
          f"--platform <platform> --text '...'")
    print()
    print(f"=== Done! Brand folder ready. ===\n")


if __name__ == "__main__":
    main()