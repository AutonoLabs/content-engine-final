#!/usr/bin/env python3
"""
Validate a draft post against:
- Anti-AI-feel rules (banned phrases)
- Diversity rules (rotation)
- Claim verification (verified-facts.md)

Usage:
    python scripts/validate_post.py --brand allsquared --platform linkedin --caption-file brands/allsquared/weeks/2026-W28/captions.md
    python scripts/validate_post.py --brand allsquared --platform linkedin --text "Caption text here"
"""

import argparse
import os
import re
import sys
from pathlib import Path


# Universal AI tells (from docs/anti-ai-feel.md)
BANNED_PHRASES = [
    "delve", "tapestry", "navigate the landscape", "in today's fast-paced world",
    "leverage", "holistic", "it's not .*, it's", "in the realm of",
    "comprehensive", "robust", "unlock the power of", "elevate your",
    "streamline your", "in an era of", "master the art of", "comprehensive solution",
    "dynamic", "seamless", "empower", "navigate the", "in the ever-evolving"
]


def load_brand_voice(brand: str) -> dict:
    """Load voice profile + verified facts + content mix."""
    brand_path = Path(f"brands/{brand}")
    if not brand_path.exists():
        return {}

    voice = {}
    voice["voice_profile"] = (brand_path / "voice-profile.md").read_text() if (brand_path / "voice-profile.md").exists() else ""
    voice["verified_facts"] = (brand_path / "verified-facts.md").read_text() if (brand_path / "verified-facts.md").exists() else ""
    voice["content_mix"] = (brand_path / "content-mix.md").read_text() if (brand_path / "content-mix.md").exists() else ""

    # Extract brand-specific banned phrases
    ban_match = re.search(r"### Brand-specific\n(.+?)(?=##|\Z)", voice["voice_profile"], re.DOTALL)
    if ban_match:
        for phrase in ban_match.group(1).split("\n"):
            phrase = phrase.strip("- ").strip()
            if phrase:
                BANNED_PHRASES.append(phrase.lower())

    return voice


def check_anti_ai(text: str) -> list:
    """Check for banned AI tells."""
    text_lower = text.lower()
    issues = []
    for phrase in BANNED_PHRASES:
        if re.search(rf"\b{re.escape(phrase)}\b", text_lower):
            issues.append(f"Banned AI phrase: '{phrase}'")
    return issues


def check_em_dash_chains(text: str) -> list:
    """Check for excessive em-dash usage."""
    issues = []
    em_dash_count = text.count("—")
    if em_dash_count > 3:
        issues.append(f"Em-dash chain: {em_dash_count} em-dashes (max 3 recommended)")
    return issues


def check_exclamation_marks(text: str) -> list:
    """Check for exclamation marks (often banned)."""
    issues = []
    if "!" in text:
        issues.append(f"Exclamation mark(s) present: {text.count('!')} found")
    return issues


def check_claims(text: str, verified_facts: str) -> list:
    """Check for unverifiable claims (very basic — flags numbers/percentages)."""
    issues = []

    # Look for percentages
    percentages = re.findall(r"\d+%|\d+\s*percent", text)
    for pct in percentages:
        if pct not in verified_facts:
            issues.append(f"Unverified percentage: '{pct}' (not in verified-facts.md)")

    # Look for years (founded, launched, etc.)
    years = re.findall(r"\b(19|20)\d{2}\b", text)
    for year in years:
        if year not in verified_facts:
            issues.append(f"Unverified year reference: '{year}'")

    return issues


def check_diversity(content_mix: str, proposed_format: str = None, proposed_theme: str = None) -> list:
    """Check diversity rules (basic — checks recent entries)."""
    issues = []

    if not content_mix:
        return issues

    # Extract recent entries (last 10)
    entries = re.findall(r"### \d{4}-\d{2}-\d{2}.+?(?=###|\Z)", content_mix, re.DOTALL)[-10:]

    # Check format repetition
    formats: list = []
    for e in entries:
        match = re.search(r"Format:\s*(.+)", e)
        if match:
            formats.append(match.group(1).strip())
    if proposed_format and formats:
        if formats[-1] == proposed_format:
            issues.append(f"Format repetition: last post used '{proposed_format}'")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate draft post")
    parser.add_argument("--brand", required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--text", help="Post text")
    parser.add_argument("--caption-file", help="File containing caption(s)")
    parser.add_argument("--format", help="Proposed format (for diversity check)")

    args = parser.parse_args()

    if not args.text and not args.caption_file:
        print("❌ Either --text or --caption-file required", file=sys.stderr)
        sys.exit(1)

    # Get text
    if args.caption_file:
        text = Path(args.caption_file).read_text()
    else:
        text = args.text

    # Load brand context
    brand = load_brand_voice(args.brand)

    # Run checks
    all_issues = []
    all_issues.extend(check_anti_ai(text))
    all_issues.extend(check_em_dash_chains(text))
    all_issues.extend(check_exclamation_marks(text))
    all_issues.extend(check_claims(text, brand.get("verified_facts", "")))
    all_issues.extend(check_diversity(brand.get("content_mix", ""), args.format))

    # Report
    if all_issues:
        print(f"\n❌ Found {len(all_issues)} issue(s):\n")
        for issue in all_issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print(f"\n✅ Passed all checks for {args.platform} post")
        sys.exit(0)


if __name__ == "__main__":
    main()