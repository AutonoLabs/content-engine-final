#!/usr/bin/env python3
"""
Doctor — preflight check that catches silent failures before a human hits them.

Verifies:
1. Repo structure intact (scripts/, docs/, brands/ exist with key files)
2. ONBOARDING.md and docs/ don't reference missing files
3. .env keys present (BLOTATO_API_KEY etc) — only warns if missing
4. Brand folders have all 7 expected files
5. Content-mix + performance-log entries parse cleanly (using same parser as compare_performance.py)
6. Template files have at least one entry to use as format spec

Usage:
    python scripts/doctor.py
    python scripts/doctor.py --brand allsquared
    python scripts/doctor.py --strict  # exit 1 on any warning
"""

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
DOCS_DIR = REPO_ROOT / "docs"
BRANDS_DIR = REPO_ROOT / "brands"

# Files every brand folder must have
BRAND_REQUIRED_FILES = [
    "brand-brief.md",
    "voice-profile.md",
    "target-audience.md",
    "verified-facts.md",
    "content-mix.md",
    "performance-log.md",
    "blotato-accounts.md",
]

# Files that MUST exist at repo root for the engine to function
REPO_REQUIRED_FILES = [
    "portfolio.yaml",
    "scripts/engine.py",
    "scripts/brand_config.py",
    "scripts/notion_sync.py",
    "docs/post-file-spec.md",
    "ONBOARDING.md",
    "README.md",
    "LICENSE",
    "requirements.txt",
    ".env.example",
    ".gitignore",
    "scripts/compare_performance.py",
    "scripts/onboard_brand.py",
    "scripts/validate_post.py",
    "scripts/media_packet.py",
    "scripts/pair_media.py",
    "scripts/blotato_client.py",
    "scripts/blotato_publish.py",
    "scripts/blotato_list_accounts.py",
    "scripts/blotato_get_post_status.py",
    "scripts/higgsfield_generate.py",
    "scripts/doctor.py",
    "docs/WEEKLY-BATCH-FLOW.md",
    "docs/diversity-rules.md",
    "docs/higgsfield-prompts.md",
    "docs/compare-performance.md",
    "docs/SELF-IMPROVEMENT.md",
    "docs/media-brief.template.md",
    "brands/brand-brief.template.md",
    "brands/content-mix.template.md",
    "brands/performance-log.template.md",
    "brands/voice-profile.template.md",
    "brands/target-audience.template.md",
    "brands/verified-facts.template.md",
    "brands/blotato-accounts.template.md",
]


def check_repo_structure() -> list[str]:
    """Check that every file ONBOARDING.md and docs reference actually exists."""
    issues = []
    for f in REPO_REQUIRED_FILES:
        if not (REPO_ROOT / f).exists():
            issues.append(f"Missing required file: {f}")
    return issues


def check_doc_references() -> list[str]:
    """
    Scan ONBOARDING.md + docs/*.md for path-like references and warn if
    the referenced file doesn't exist.
    """
    issues = []
    docs_to_scan = [
        REPO_ROOT / "ONBOARDING.md",
        REPO_ROOT / "README.md",
    ] + list(DOCS_DIR.glob("*.md"))

    # Match references like `scripts/foo.py`, `docs/foo.md`, `brands/foo.md`
    # Skip URLs and image markdown
    path_re = re.compile(r"`?((?:scripts|docs|brands)/[a-zA-Z0-9_./-]+\.[a-z]+)`?")

    for doc in docs_to_scan:
        if not doc.exists():
            continue
        text = doc.read_text()
        for match in path_re.finditer(text):
            ref = match.group(1)
            # Strip trailing punctuation that might be part of a sentence
            ref = ref.rstrip(".,;:!?)")
            if not (REPO_ROOT / ref).exists():
                issues.append(f"{doc.relative_to(REPO_ROOT)} references missing file: {ref}")

    return issues


def check_env_keys() -> list[str]:
    """Warn (don't fail) if common API keys are missing."""
    issues = []
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(REPO_ROOT / ".env")
    except ImportError:
        issues.append("python-dotenv not installed (run: pip install -r requirements.txt)")
        return issues

    keys_expected = [
        ("BLOTATO_API_KEY", "Multi-platform publishing"),
    ]
    # Don't fail on HIGGSFIELD/XAI/REPLICATE — they're manual-paste workflows
    keys_optional = ["HIGGSFIELD_API_KEY", "XAI_API_KEY", "REPLICATE_API_TOKEN"]

    import os
    for key, purpose in keys_expected:
        if not os.getenv(key):
            issues.append(f"MISSING required env var: {key} ({purpose})")

    return issues


def check_brand(brand: str) -> list[str]:
    """Check a single brand folder."""
    issues = []
    brand_path = BRANDS_DIR / brand
    if not brand_path.exists():
        return [f"Brand folder not found: brands/{brand}"]

    # Required files
    for f in BRAND_REQUIRED_FILES:
        if not (brand_path / f).exists():
            issues.append(f"brands/{brand}/ missing: {f}")

    # Machine config (brand.yaml) — required by engine.py / notion_sync.py
    try:
        import brand_config
        if not (brand_path / "brand.yaml").exists():
            issues.append(f"brands/{brand}/ missing: brand.yaml (engine can't schedule)")
        else:
            cfg = brand_config.load_brand(brand)
            wired = [k for k, v in cfg.get("platforms", {}).items()
                     if v.get("account_id")]
            if not wired:
                issues.append(
                    f"brands/{brand}/brand.yaml: no platform has an account_id "
                    f"(fill from blotato_list_accounts.py before scheduling)")
        if brand not in brand_config.portfolio_brands():
            issues.append(f"brands/{brand}/ not listed in portfolio.yaml")
        # Portfolio brands with an author must have the overlay + author profile
        entry = brand_config.load_brand(brand)
        if entry.get("author"):
            if not (brand_path / "voice-overlay.md").exists():
                issues.append(f"brands/{brand}/ missing: voice-overlay.md "
                              f"(author '{entry['author']}' declared)")
            portfolio = brand_config.load_portfolio()
            ap = portfolio.get("owner", {}).get("author_profile")
            if ap and not (REPO_ROOT / ap).exists():
                issues.append(f"portfolio.yaml author_profile missing: {ap}")
        if entry.get("compliance_file"):
            if not (brand_path / entry["compliance_file"]).exists():
                issues.append(f"brands/{brand}/ missing: {entry['compliance_file']}")
    except Exception as e:
        issues.append(f"brands/{brand}/: brand.yaml check failed ({e})")

    # Content-mix + performance-log parse check
    from compare_performance import parse_content_mix, parse_performance_log
    cm_path = brand_path / "content-mix.md"
    if cm_path.exists():
        posts = parse_content_mix(cm_path)
        if not posts:
            issues.append(f"brands/{brand}/content-mix.md: no parseable entries")

    pl_path = brand_path / "performance-log.md"
    if pl_path.exists():
        log = parse_performance_log(pl_path)
        if not log:
            issues.append(f"brands/{brand}/performance-log.md: no parseable entries")

    return issues


def check_templates_have_examples() -> list[str]:
    """Templates should have inline 'delete me' examples carrying the format spec."""
    issues = []
    templates = [
        "brand-brief.template.md",
        "content-mix.template.md",
        "performance-log.template.md",
    ]
    for t in templates:
        path = BRANDS_DIR / t
        if not path.exists():
            continue
        text = path.read_text()
        if "DELETE ME" not in text and "delete me" not in text.lower():
            issues.append(f"brands/{t}: no 'DELETE ME' example block (format spec missing)")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Preflight check")
    parser.add_argument("--brand", help="Check a specific brand folder")
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 on any issue (default: warn only)")
    args = parser.parse_args()

    print(f"=== Doctor — preflight check ===\n")
    print(f"Repo root: {REPO_ROOT}\n")

    all_issues = []

    print("→ Repo structure")
    issues = check_repo_structure()
    for i in issues:
        print(f"  ✗ {i}")
    all_issues.extend(issues)
    if not issues:
        print("  ✓ All required files present")

    print("\n→ Doc references")
    issues = check_doc_references()
    for i in issues[:20]:  # cap output
        print(f"  ✗ {i}")
    if len(issues) > 20:
        print(f"  ... and {len(issues) - 20} more")
    all_issues.extend(issues)
    if not issues:
        print("  ✓ All doc references resolve")

    print("\n→ Env keys")
    issues = check_env_keys()
    for i in issues:
        print(f"  ✗ {i}")
    all_issues.extend(issues)
    if not issues:
        print("  ✓ All required env keys present")

    print("\n→ Templates have inline examples")
    issues = check_templates_have_examples()
    for i in issues:
        print(f"  ✗ {i}")
    all_issues.extend(issues)
    if not issues:
        print("  ✓ All templates carry format spec")

    if args.brand:
        print(f"\n→ Brand: {args.brand}")
        issues = check_brand(args.brand)
        for i in issues:
            print(f"  ✗ {i}")
        all_issues.extend(issues)
        if not issues:
            print(f"  ✓ brands/{args.brand}/ looks healthy")
    else:
        # Check all brands declared in portfolio.yaml (plus any stray folders)
        if BRANDS_DIR.exists():
            try:
                import brand_config
                brands = brand_config.portfolio_brands()
                strays = [d.name for d in BRANDS_DIR.iterdir()
                          if d.is_dir() and d.name not in brands]
                for s in strays:
                    all_issues.append(f"brands/{s}/ exists but not in portfolio.yaml")
                    print(f"  ✗ brands/{s}/ exists but not in portfolio.yaml")
            except Exception:
                brands = [d.name for d in BRANDS_DIR.iterdir() if d.is_dir()]
            for brand in sorted(brands):
                print(f"\n→ Brand: {brand}")
                issues = check_brand(brand)
                for i in issues:
                    print(f"  ✗ {i}")
                all_issues.extend(issues)
                if not issues:
                    print(f"  ✓ brands/{brand}/ looks healthy")

    print(f"\n=== Summary ===\n")
    if not all_issues:
        print("All checks passed.")
        sys.exit(0)
    print(f"{len(all_issues)} issue(s) found.")
    if args.strict:
        sys.exit(1)
    print("(Run with --strict to exit non-zero on any issue.)")
    sys.exit(0)


if __name__ == "__main__":
    main()