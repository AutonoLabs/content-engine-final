#!/usr/bin/env python3
"""
Onboard a new brand to the content engine.

Usage:
    python scripts/onboard_brand.py --name yapper --sector consumer_health

This will:
1. Create brands/<name>/ folder structure
2. Copy templates
3. Print next-step checklist
"""

import argparse
import os
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Onboard new brand")
    parser.add_argument("--name", required=True, help="Brand name (lowercase, no spaces)")
    parser.add_argument("--sector", required=True,
                        choices=["consumer_health", "fintech", "legal", "professional",
                                 "education", "creative", "other"],
                        help="Industry sector")
    args = parser.parse_args()

    brand_name = args.name.lower().replace(" ", "-")
    brand_path = Path(f"brands/{brand_name}")

    if brand_path.exists():
        print(f"❌ brands/{brand_name}/ already exists")
        return

    print(f"\n=== Onboarding brand: {brand_name} ===\n")

    # Create folder structure
    (brand_path / "weeks").mkdir(parents=True)
    (brand_path / "exemplars/edits").mkdir(parents=True)
    (brand_path / "inbox").mkdir(parents=True)

    # Copy templates
    templates = [
        ("voice-profile.template.md", "voice-profile.md"),
        ("target-audience.template.md", "target-audience.md"),
        ("verified-facts.template.md", "verified-facts.md"),
        ("content-mix.template.md", "content-mix.md"),
        ("performance-log.template.md", "performance-log.md"),
        ("brand-brief.template.md", "brand-brief.md"),
        ("blotato-accounts.template.md", "blotato-accounts.md"),
    ]

    for src, dst in templates:
        src_path = Path(f"brands/{src}")
        if src_path.exists():
            shutil.copy(src_path, brand_path / dst)
            print(f"  ✓ Copied {src} → {brand_path / dst}")

    # Print next steps
    print(f"\n=== Next steps for {brand_name} ===\n")
    print("1. Fill in brand brief:")
    print(f"   - Edit brands/{brand_name}/brand-brief.md")
    print()
    print("2. Run voice-from-brief skill:")
    print(f"   - Read skills/voice-from-brief.md")
    print(f"   - Apply to fill in brands/{brand_name}/voice-profile.md")
    print()
    print("3. Fill target audience:")
    print(f"   - Use docs/audience-demographics.md as baseline")
    print(f"   - Override for {brand_name}-specific segments in target-audience.md")
    print()
    print("4. Set up verified-facts.md sector rules:")
    print(f"   - Read skills/claim-verifier.md")
    print(f"   - Apply {args.sector} sector rules to verified-facts.md")
    print()
    print("5. Wire Blotato accounts:")
    print(f"   - Connect accounts in Blotato dashboard")
    print(f"   - Run: python scripts/blotato_list_accounts.py")
    print(f"   - Document IDs in brands/{brand_name}/blotato-accounts.md")
    print()
    print("6. Plan first batch:")
    print(f"   - Read docs/WEEKLY-BATCH-FLOW.md")
    print(f"   - Pick theme, draft 3-5 posts across platforms")
    print(f"   - Run validate_post.py before each publish:")
    print(f"     python scripts/validate_post.py --brand {brand_name} --platform <platform> --text '...'")
    print()
    print("=== Done! Brand folder ready. ===\n")


if __name__ == "__main__":
    main()