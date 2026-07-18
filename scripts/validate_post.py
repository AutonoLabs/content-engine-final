#!/usr/bin/env python3
"""
Validate a draft post against:
- Anti-AI-feel rules (banned phrases) — with sector whitelists
- Diversity rules (rotation)
- Claim verification (verified-facts.md) — with proper year + percent handling
- Multi-post file support (split on ### headers)

Usage:
    python scripts/validate_post.py --brand allsquared --platform linkedin --text "Caption text here"
    python scripts/validate_post.py --brand allsquared --platform linkedin --caption-file weeks/2026-W28/captions.md
    python scripts/validate_post.py --brand allsquared --platform linkedin --text "..." --format image-square

Robustness (v1.3):
- Sector-aware banned phrases (fintech whitelists "leverage" with risk-language caveat)
- AI-tell regex works correctly (no more re.escape() dead string)
- Year check returns full 4-digit year, substring-checks against verified facts
- Multi-post files split on ### headers before validation
- Brand-specific banned phrases scoped per-call (no global mutation across brands)
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional


# Universal AI tells (from docs/anti-ai-feel.md)
# Removed: "leverage", "dynamic", "comprehensive", "robust" — moved to sector lists
# Note: phrases may contain .* as a wildcard
UNIVERSAL_BANNED = [
    "delve", "tapestry", "navigate the landscape", "in today's fast-paced world",
    "holistic", "in the realm of", "unlock the power of", "elevate your",
    "streamline your", "in an era of", "master the art of", "comprehensive solution",
    "seamless", "empower", "navigate the", "in the ever-evolving",
    "it's not .*, it's",  # classic AI hedging pattern
    "in a world of",       # AI tell
    "where .* meets .*",   # "where ambition meets execution"
]

# Sector-specific phrase policies
# Each entry: phrase -> sectors where it's banned.
# "leverage" is banned in consumer-facing copy but allowed in regulated fintech
# ONLY with risk-language caveat (presence of "risk", "exposure", "caution" within 80 chars).
PHRASE_POLICIES = {
    "leverage": {
        "banned_sectors": ["consumer_health", "creative", "education"],
        "conditional_sectors": {
            "fintech": {
                "needs_risk_language": True,
                "window_chars": 80,
                "risk_terms": ["risk", "exposure", "caution", "downside",
                               "loss", "volatile", "hedge"],
            },
            "legal": {
                "needs_risk_language": True,
                "window_chars": 80,
                "risk_terms": ["risk", "exposure", "caution", "downside",
                               "loss", "liable"],
            },
            "professional": {
                "needs_risk_language": False,
            },
        },
    },
    "dynamic": {
        "banned_sectors": ["consumer_health", "education", "creative"],
        "conditional_sectors": {},
    },
    "comprehensive": {
        "banned_sectors": ["consumer_health", "creative"],
        "conditional_sectors": {},
    },
    "robust": {
        "banned_sectors": ["consumer_health", "creative", "education"],
        "conditional_sectors": {},
    },
}


def load_brand_voice(brand: str) -> dict:
    """
    Load voice profile + verified facts + content mix.
    Returns dict with .get() safety. Brand-specific bans returned in result,
    not mutated into a global.
    """
    repo_root = Path(__file__).resolve().parent.parent
    brand_path = repo_root / "brands" / brand
    if not brand_path.exists():
        return {
            "exists": False,
            "voice_profile": "",
            "verified_facts": "",
            "content_mix": "",
            "sector": None,
            "brand_specific_bans": [],
        }

    voice = {"exists": True, "brand_path": brand_path}
    voice["voice_profile"] = (
        (brand_path / "voice-profile.md").read_text()
        if (brand_path / "voice-profile.md").exists() else ""
    )
    voice["verified_facts"] = (
        (brand_path / "verified-facts.md").read_text()
        if (brand_path / "verified-facts.md").exists() else ""
    )
    voice["content_mix"] = (
        (brand_path / "content-mix.md").read_text()
        if (brand_path / "content-mix.md").exists() else ""
    )

    # Sector: brand.yaml is the machine source of truth; voice-profile prose
    # is the legacy fallback.
    voice["sector"] = None
    voice["compliance"] = None
    try:
        import brand_config
        cfg = brand_config.load_brand(brand)
        voice["sector"] = cfg.get("sector")
        voice["compliance"] = brand_config.load_compliance(brand)
    except Exception:
        pass
    if not voice["sector"]:
        sector_match = re.search(r"\*\*Sector:\*\*\s*(\w+)", voice["voice_profile"])
        voice["sector"] = sector_match.group(1) if sector_match else None

    # Extract brand-specific banned phrases (scoped, not global)
    voice["brand_specific_bans"] = []
    ban_match = re.search(
        r"### Brand-specific(?:ly)? banned.*?\n(.+?)(?=##|\Z)",
        voice["voice_profile"],
        re.DOTALL,
    )
    if ban_match:
        for phrase in ban_match.group(1).split("\n"):
            phrase = phrase.strip("- ").strip()
            if phrase:
                voice["brand_specific_bans"].append(phrase.lower())

    return voice


def _phrase_allowed_for_sector(phrase: str, sector: Optional[str], text: str) -> tuple[bool, str]:
    """
    Returns (allowed, reason). If not allowed, reason explains why.
    """
    if phrase not in PHRASE_POLICIES:
        # No sector policy — fall back to universal check (caller handles)
        return True, ""

    policy = PHRASE_POLICIES[phrase]

    if not sector:
        # No sector info — default to banned if in any banned list
        return False, f"'{phrase}' requires sector context for evaluation"

    if sector in policy["banned_sectors"]:
        return False, f"'{phrase}' banned in {sector} sector"

    if sector in policy["conditional_sectors"]:
        cond = policy["conditional_sectors"][sector]
        if cond.get("needs_risk_language"):
            window = cond.get("window_chars", 80)
            terms = cond.get("risk_terms", [])
            # Check if any risk term appears within window chars of the phrase
            for m in re.finditer(rf"\b{re.escape(phrase)}\b", text, re.IGNORECASE):
                start = max(0, m.start() - window)
                end = min(len(text), m.end() + window)
                surrounding = text[start:end].lower()
                if any(t in surrounding for t in terms):
                    return True, "risk-language caveat present"
            return False, (
                f"'{phrase}' in {sector} requires risk-language caveat "
                f"(risk/exposure/caution/etc.) within {window} chars"
            )
        return True, ""

    return True, ""


def _phrase_to_regex(phrase: str) -> str:
    """
    Convert a phrase (with optional .* wildcards) to a regex.
    Escapes special chars EXCEPT for explicit .* which is treated as wildcard.
    """
    # Split on .* first (escape order matters)
    parts = phrase.split(".*")
    escaped_parts = [re.escape(p) for p in parts]
    return ".*".join(escaped_parts)


def check_anti_ai(text: str, sector: Optional[str] = None,
                  brand_specific_bans: Optional[list] = None) -> list:
    """Check for banned AI tells. Sector-aware."""
    text_lower = text.lower()
    issues = []

    # Check universal bans
    for phrase in UNIVERSAL_BANNED:
        pattern = _phrase_to_regex(phrase)
        if re.search(rf"\b{pattern}\b", text_lower):
            issues.append(f"Banned AI phrase: '{phrase}'")

    # Check sector-policy phrases
    for phrase in PHRASE_POLICIES:
        pattern = _phrase_to_regex(phrase)
        if re.search(rf"\b{pattern}\b", text_lower):
            allowed, reason = _phrase_allowed_for_sector(phrase, sector, text)
            if not allowed:
                issues.append(reason)

    # Check brand-specific bans (scoped, not global)
    if brand_specific_bans:
        for phrase in brand_specific_bans:
            pattern = _phrase_to_regex(phrase)
            if re.search(rf"\b{pattern}\b", text_lower):
                issues.append(f"Brand-banned phrase: '{phrase}'")

    return issues


def check_em_dash_chains(text: str) -> list:
    """Check for excessive em-dash usage (>3 in a single post)."""
    issues = []
    em_dash_count = text.count("—")
    if em_dash_count > 3:
        issues.append(
            f"Em-dash chain: {em_dash_count} em-dashes (max 3 recommended)"
        )
    return issues


def check_exclamation_marks(text: str) -> list:
    """Check for exclamation marks."""
    issues = []
    if "!" in text:
        issues.append(f"Exclamation mark(s) present: {text.count('!')} found")
    return issues


def check_claims(text: str, verified_facts: str) -> list:
    """
    Check for unverifiable claims.
    Returns full 4-digit years (not captured group).
    Substring-checks the year against verified facts content.
    """
    issues = []

    # Percentages
    percentages = re.findall(r"\d+(?:\.\d+)?\s*%|\d+(?:\.\d+)?\s*percent", text)
    for pct in percentages:
        if pct not in verified_facts:
            issues.append(
                f"Unverified percentage: '{pct}' (not in verified-facts.md)"
            )

    # Years — capture the FULL 4-digit year, not just the prefix
    years = re.findall(r"\b(?:19|20)\d{2}\b", text)
    for year in years:
        if year not in verified_facts:
            issues.append(
                f"Unverified year reference: '{year}' (not in verified-facts.md)"
            )

    # Specific large numbers (claims like "10,000 builders")
    big_numbers = re.findall(r"\b\d{1,3}(?:,\d{3})+\b", text)
    for num in big_numbers:
        if num not in verified_facts:
            issues.append(
                f"Unverified large number: '{num}' (not in verified-facts.md)"
            )

    return issues


def check_diversity(content_mix: str, proposed_format: str = None,
                    proposed_theme: str = None) -> list:
    """Check diversity rules. Last-format check only (other rules are honor-system per docs)."""
    issues = []

    if not content_mix:
        return issues

    # Extract last entry only (other rules are documented in diversity-rules.md,
    # not mechanically enforced here)
    entries = re.findall(
        r"###\s+\d{4}-\d{2}-\d{2}.+?(?=###|\Z)", content_mix, re.DOTALL
    )
    if not entries:
        return issues

    last = entries[-1]
    last_format_match = re.search(r"Format:\s*(.+)", last)
    if last_format_match and proposed_format:
        last_format = last_format_match.group(1).strip()
        if last_format == proposed_format:
            issues.append(
                f"Format repetition: last post used '{proposed_format}'"
            )

    return issues


def split_multi_post(text: str) -> list:
    """
    Split a captions.md file into individual posts.
    Splits on '### ' headers that start with a date.
    For each block, extract ONLY the caption body (between `## Caption` and
    the next `## Metadata` / `## Note` / `## Higgsfield packet` section).
    This prevents metadata like "Length: 1,043 chars" or "Week 2026-W29"
    from being validated as caption text.
    """
    parts = re.split(r"(?=^###\s+\d{4}-\d{2}-\d{2})", text, flags=re.MULTILINE)
    result = []
    for part in parts:
        if not part.strip():
            continue
        # Extract the caption body: between "## Caption" and the next "## " section
        caption_match = re.search(
            r"^##\s+Caption\s*\n(.*?)(?=^##\s+(?:Metadata|Note|Higgsfield|Cross|$)|\Z)",
            part,
            re.MULTILINE | re.DOTALL,
        )
        if caption_match:
            body = caption_match.group(1).strip()
            if body:
                result.append(body)
                continue
        # Fallback: no ## Caption section found — validate whole block
        result.append(part.strip())
    return result


def check_compliance(text: str, platform: str, compliance: Optional[dict]) -> list:
    """
    Enforce brands/<brand>/compliance.yaml (locked spine, human-curated).
    - banned_claim_patterns: case-insensitive regexes that block the post
    - mandatory_disclaimers: per-platform (or 'default') string that MUST appear
    """
    if not compliance:
        return []
    issues = []
    for pattern in compliance.get("banned_claim_patterns") or []:
        try:
            if re.search(pattern, text, re.IGNORECASE):
                issues.append(f"COMPLIANCE: banned claim pattern matched: /{pattern}/")
        except re.error:
            issues.append(f"COMPLIANCE: invalid regex in compliance.yaml: /{pattern}/")
    disclaimers = compliance.get("mandatory_disclaimers") or {}
    required = disclaimers.get(platform, disclaimers.get("default"))
    if required and required.lower() not in text.lower():
        issues.append(f"COMPLIANCE: missing mandatory disclaimer: '{required}'")
    return issues


def validate_one(text: str, platform: str, brand: dict,
                 proposed_format: Optional[str] = None) -> list:
    """Run all checks against a single post. Returns list of issues."""
    all_issues: list = []
    brand_bans = brand.get("brand_specific_bans") or []
    all_issues.extend(check_anti_ai(text, sector=brand.get("sector"),
                                     brand_specific_bans=brand_bans))
    all_issues.extend(check_em_dash_chains(text))
    all_issues.extend(check_exclamation_marks(text))
    all_issues.extend(check_claims(text, brand.get("verified_facts", "") or ""))
    all_issues.extend(check_diversity(brand.get("content_mix", "") or "",
                                       proposed_format))
    all_issues.extend(check_compliance(text, platform, brand.get("compliance")))
    return all_issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate draft post")
    parser.add_argument("--brand", required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--text", help="Post text")
    parser.add_argument("--caption-file",
                        help="File containing caption(s); split on ### headers")
    parser.add_argument("--format", help="Proposed format (for diversity check)")
    args = parser.parse_args()

    if not args.text and not args.caption_file:
        print("ERROR: Either --text or --caption-file required", file=sys.stderr)
        sys.exit(1)

    # Load brand context
    brand = load_brand_voice(args.brand)
    if not brand.get("exists"):
        print(f"WARN: brands/{args.brand}/ not found — running with no sector context",
              file=sys.stderr)

    # Get text(s) to validate
    if args.caption_file:
        raw_text = Path(args.caption_file).read_text()
        posts = split_multi_post(raw_text)
        if not posts:
            # No ### headers found — treat whole file as one post
            posts = [raw_text]
    else:
        posts = [args.text]

    total_issues = 0
    for i, post_text in enumerate(posts, 1):
        issues = validate_one(post_text, args.platform, brand, args.format)
        if issues:
            print(f"\nFAIL: Post {i}/{len(posts)}:")
            for issue in issues:
                print(f"  - {issue}")
            total_issues += len(issues)
        else:
            preview = post_text[:60].replace("\n", " ")
            print(f"OK: Post {i}/{len(posts)} — '{preview}...'")

    if total_issues:
        print(f"\nFAIL: {total_issues} issue(s) across {len(posts)} post(s)")
        sys.exit(1)
    print(f"\nPASS: {len(posts)} post(s) validated for {args.platform}")


if __name__ == "__main__":
    main()