#!/usr/bin/env python3
"""
Compare past posts to surface winning patterns.

Reads:
- brands/<brand>/content-mix.md (per-post metadata: theme, narrative, hook, visual, audience)
- brands/<brand>/performance-log.md (per-post engagement: impressions, likes, comments, shares, rate)

Outputs:
- Top performing themes / narrative styles / hook patterns / visual styles / audience segments / formats
- Bottom performing (consider cutting)
- Engagement distribution + trends
- Unmatched warnings (loud, to stderr)

Robustness (v1.3):
- Case-insensitive platform join (Twitter==twitter, LinkedIn==linkedin, IG==instagram)
- Accepts multiple date formats: 2026-07-01, 01/07/2026, 1 July 2026, July 1 2026, 01.07.2026
- Accepts em-dash, en-dash, or hyphen as header separator
- Accepts ## or ### headers
- Does NOT swallow the first entry
- Full field-name canonicalization (17 metric aliases)
- Units normalized: 5.6%, 0.056, 5.6 all become 0.056; 1.2k becomes 1200
- Median computed correctly for even n
- Loud unmatched warnings to stderr

Usage:
    python scripts/compare_performance.py --brand allsquared
    python scripts/compare_performance.py --brand allsquared --json
    python scripts/compare_performance.py --brand allsquared --metric engagement_rate
    python scripts/compare_performance.py --brand allsquared --by theme --top 5
"""

import argparse
import datetime
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional


# Robust date parsing — accept multiple human formats
DATE_FORMATS = [
    "%Y-%m-%d",       # 2026-07-01
    "%Y/%m/%d",       # 2026/07/01
    "%d/%m/%Y",       # 01/07/2026 (UK/EU)
    "%m/%d/%Y",       # 07/01/2026 (US)
    "%d.%m.%Y",       # 01.07.2026 (DE)
    "%d %B %Y",       # 1 July 2026
    "%B %d, %Y",      # July 1, 2026
    "%d %b %Y",       # 1 Jul 2026
    "%d-%m-%Y",       # 01-07-2026
]

# Platform aliases — normalize to canonical name
PLATFORM_ALIASES = {
    "twitter": "x",
    "x/twitter": "x",
    "x": "x",
    "ig": "instagram",
    "insta": "instagram",
    "instagram": "instagram",
    "li": "linkedin",
    "linkedin": "linkedin",
    "yt": "youtube",
    "youtube": "youtube",
    "youtube shorts": "youtube",
    "fb": "facebook",
    "facebook": "facebook",
    "tiktok": "tiktok",
    "threads": "threads",
    "bsky": "bluesky",
    "bluesky": "bluesky",
    "pin": "pinterest",
    "pinterest": "pinterest",
}

# Field name canonicalization (metric name → canonical key)
FIELD_CANON = {
    # Engagement rate
    "engagement_rate": "engagement_rate",
    "engagement rate": "engagement_rate",
    "engagement": "engagement_rate",
    "eng rate": "engagement_rate",
    "er": "engagement_rate",
    # Impressions / reach (often interchangeable)
    "impressions": "impressions",
    "impression": "impressions",
    "impressions / reach": "impressions",
    "impressions/reach": "impressions",
    "reach": "impressions",
    "views": "impressions",
    "view": "impressions",
    # Likes
    "likes": "likes",
    "like": "likes",
    "likes / reactions": "likes",
    "likes/reactions": "likes",
    "reactions": "likes",
    "reaction": "likes",
    # Comments
    "comments": "comments",
    "comment": "comments",
    "replies": "comments",
    "reply": "comments",
    # Shares
    "shares": "shares",
    "share": "shares",
    "shares / reposts": "shares",
    "shares/reposts": "shares",
    "reposts": "shares",
    "repost": "shares",
    "retweets": "shares",
    "retweet": "shares",
    # Saves
    "saves": "saves",
    "save": "saves",
    "saves (ig/linkedin)": "saves",
    # Click-throughs
    "click_throughs": "click_throughs",
    "click-throughs": "click_throughs",
    "clicks": "click_throughs",
    "click": "click_throughs",
}

# Robust header separator — em-dash, en-dash, or hyphen
HEADER_SEP = re.compile(r"\s+[—–-]\s+")
# Match ## or ### headers
ENTRY_SPLIT = re.compile(r"^#{2,3}\s+", re.MULTILINE)


def normalize_date(s: str) -> Optional[str]:
    """Try multiple date formats, return ISO YYYY-MM-DD or None."""
    s = s.strip().strip("[]()")
    for fmt in DATE_FORMATS:
        try:
            return datetime.datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def normalize_platform(s: str) -> Optional[str]:
    """Normalize platform name to canonical (lowercase)."""
    s = s.strip().strip("[]()").lower()
    return PLATFORM_ALIASES.get(s, s)


def normalize_field(s: str) -> str:
    """Normalize field name to canonical key."""
    s = s.strip().lower()
    return FIELD_CANON.get(s, s.replace(" ", "_"))


def normalize_rate(raw: str) -> Optional[float]:
    """
    Parse engagement rate with unit handling.
    5.6%, 0.056, 5.6 → all 0.056
    """
    m = re.match(r"^([\d.,]+)\s*(%|percent)?\s*$", raw.strip(), re.I)
    if not m:
        return None
    num = float(m.group(1).replace(",", ""))
    if m.group(2):  # explicit % sign
        return num / 100
    # Heuristic: bare >1 means "5.6" not "0.056" — treat as percent
    return num / 100 if num > 1 else num


def normalize_count(raw: str) -> Optional[float]:
    """
    Parse count metric with k/m suffix.
    1.2k → 1200, 1.2m → 1,200,000, 1,200 → 1200
    """
    m = re.match(r"^([\d.,]+)\s*([km])?\s*$", raw.strip(), re.I)
    if not m:
        return None
    num = float(m.group(1).replace(",", ""))
    suffix = (m.group(2) or "").lower()
    multiplier = {"k": 1_000, "m": 1_000_000}.get(suffix, 1)
    return num * multiplier


def _split_entries(content: str) -> list[str]:
    """
    Split file into per-entry blocks.
    Handles ## or ### headers; does not swallow the first entry.
    """
    # Find all matches with positions
    matches = list(ENTRY_SPLIT.finditer(content))
    if not matches:
        return []
    entries = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        entries.append(content[start:end])
    return entries


def parse_content_mix(path: Path) -> list[dict]:
    """Parse content-mix.md into list of post dicts."""
    if not path.exists():
        return []

    content = path.read_text()
    posts = []

    entries = _split_entries(content)
    for entry in entries:
        lines = entry.split("\n")
        header = lines[0].lstrip("#").strip()

        # Parse header: "YYYY-MM-DD — platform — theme" (or hyphen/en-dash variants)
        parts = HEADER_SEP.split(header, maxsplit=2)
        if len(parts) < 3:
            continue

        raw_date, raw_platform, theme = parts[0], parts[1], parts[2]
        date = normalize_date(raw_date)
        platform = normalize_platform(raw_platform)
        if date is None or platform is None:
            # Loud warning — caller logs
            continue

        post = {
            "date": date,
            "platform": platform,
            "theme": theme.strip(),
        }

        # Parse fields: "- **Field:** value" OR "- Field: value"
        for line in lines[1:]:
            match = re.match(r"-\s+\*?\*?(.+?):\*?\*?\s+(.+)", line.strip())
            if match:
                field = normalize_field(match.group(1))
                value = match.group(2).strip()
                post[field] = value

        posts.append(post)

    return posts


def parse_performance_log(path: Path) -> dict[tuple[str, str], dict]:
    """Parse performance-log.md into dict keyed by (date, platform)."""
    if not path.exists():
        return {}

    content = path.read_text()
    log: dict[tuple[str, str], dict] = {}

    entries = _split_entries(content)
    for entry in entries:
        lines = entry.split("\n")
        header = lines[0].lstrip("#").strip()

        parts = HEADER_SEP.split(header, maxsplit=2)
        if len(parts) < 3:
            continue

        raw_date, raw_platform = parts[0], parts[1]
        date = normalize_date(raw_date)
        platform = normalize_platform(raw_platform)
        if date is None or platform is None:
            continue

        engagement = {}
        for line in lines[1:]:
            match = re.match(r"-\s+\*?\*?(.+?):\*?\*?\s+(.+)", line.strip())
            if match:
                field = normalize_field(match.group(1))
                value_str = match.group(2).strip()

                # Try to parse as count metric first
                count = normalize_count(value_str)
                if count is not None and field != "engagement_rate":
                    engagement[field] = count
                    continue

                # Try as rate metric (engagement_rate is the main one)
                rate = normalize_rate(value_str)
                if rate is not None:
                    engagement[field] = rate
                    continue

                # Otherwise store as string
                if value_str and value_str != "N/A":
                    engagement[field] = value_str
                else:
                    engagement[field] = None

        log[(date, platform)] = engagement

    return log


def correlate_posts(posts: list[dict], log: dict) -> list[dict]:
    """
    Join posts with their engagement. WARN LOUDLY if any post lacks a match.
    """
    enriched = []
    unmatched_posts = []
    unmatched_perf = set(log.keys())

    for post in posts:
        key = (post["date"], post["platform"])
        if key in log:
            post["engagement"] = log[key]
            unmatched_perf.discard(key)
        else:
            post["engagement"] = {}
            unmatched_posts.append(post)
        enriched.append(post)

    if unmatched_posts:
        print(f"\n⚠️  {len(unmatched_posts)} content-mix post(s) have NO performance match:",
              file=sys.stderr)
        for p in unmatched_posts:
            print(f"    ({p['date']}, {p['platform']}) — theme: {p.get('theme', '?')}",
                  file=sys.stderr)

    if unmatched_perf:
        print(f"\n⚠️  {len(unmatched_perf)} performance-log entry(ies) match NO post:",
              file=sys.stderr)
        for k in sorted(unmatched_perf):
            print(f"    {k}", file=sys.stderr)

    return enriched


def aggregate_by_field(posts: list[dict], field: str, metric: str) -> list[dict]:
    """Group posts by `field`, compute aggregate `metric` (avg/min/max/n/total)."""
    groups = defaultdict(list)
    for p in posts:
        value = p.get(field, "")
        eng = p.get("engagement", {})
        if value and metric in eng and isinstance(eng[metric], (int, float)):
            groups[value].append(eng[metric])

    results = []
    for value, values in groups.items():
        if values:
            results.append({
                "field": field,
                "value": value,
                "n": len(values),
                "avg": statistics.mean(values),
                "min": min(values),
                "max": max(values),
                "total": sum(values),
                "median": statistics.median(values),
            })
    results.sort(key=lambda r: r["avg"], reverse=True)
    return results


def print_summary(enriched: list[dict], metric: str) -> None:
    """Print overall summary."""
    values = [p["engagement"][metric] for p in enriched
              if isinstance(p.get("engagement", {}).get(metric), (int, float))]
    if not values:
        print("\nNo posts have metric data yet.")
        return

    print(f"\n=== Overall Summary ===\n")
    print(f"  Posts with {metric}: {len(values)}")
    print(f"  Average: {statistics.mean(values):.4f}")
    print(f"  Best:    {max(values):.4f}")
    print(f"  Worst:   {min(values):.4f}")
    print(f"  Median:  {statistics.median(values):.4f}")


def print_by_platform(enriched: list[dict], metric: str) -> None:
    """Break down by platform."""
    groups = defaultdict(list)
    for p in enriched:
        v = p.get("engagement", {}).get(metric)
        if isinstance(v, (int, float)):
            groups[p["platform"]].append(v)

    if not groups:
        return

    print(f"\n=== By Platform ===\n")
    for platform, values in sorted(groups.items(), key=lambda x: -statistics.mean(x[1])):
        print(f"  {platform:18s}  n={len(values):>3d}  avg={statistics.mean(values):.4f}")


def print_field_breakdown(posts: list[dict], field: str, metric: str, top_n: int = 5) -> None:
    """Print top + bottom performers for a field."""
    results = aggregate_by_field(posts, field, metric)
    if not results:
        return

    print(f"\n=== Performance by {field} (sorted by {metric}, n={len(results)} groups) ===\n")
    print(f"  {field:28s}  {'posts':>6s}  {'avg':>10s}  {'min':>8s}  {'max':>8s}  {'median':>8s}")
    print(f"  {'-'*28}  {'-'*6}  {'-'*10}  {'-'*8}  {'-'*8}  {'-'*8}")

    print("\nTOP:")
    for r in results[:top_n]:
        print(f"  {r['value']:28s}  {r['n']:>6d}  {r['avg']:>10.4f}  "
              f"{r['min']:>8.4f}  {r['max']:>8.4f}  {r['median']:>8.4f}")

    if len(results) > top_n:
        print(f"\nBOTTOM (of {len(results)}):")
        for r in results[-top_n:]:
            print(f"  {r['value']:28s}  {r['n']:>6d}  {r['avg']:>10.4f}  "
                  f"{r['min']:>8.4f}  {r['max']:>8.4f}  {r['median']:>8.4f}")


def print_suggestions(posts: list[dict], field: str, metric: str, top_n: int = 5) -> None:
    """
    Print 'lean into X, reduce Y' suggestions.
    Hard guardrail (per fable's review): require n≥3 for any pattern-weight move.
    Single-post wins are noise; do not amplify them.
    """
    results = aggregate_by_field(posts, field, metric)
    if len(results) < 2:
        return

    # Filter to groups with n>=3 (statistical signal, not noise)
    significant = [r for r in results if r["n"] >= 3]
    if len(significant) < 2:
        # Not enough data yet — say so explicitly rather than noise-amplifying
        max_n = max(r["n"] for r in results)
        print(f"  (no {field} pattern has n>=3 yet; max n={max_n}. "
              f"Need more posts before pattern weights move.)")
        return

    top = significant[0]
    bottom = significant[-1]
    if top["avg"] > bottom["avg"] * 1.3:  # 30%+ better (was 1.5x — too noisy at small n)
        print(f"  ✓ Lean into '{top['value']}' for {field} "
              f"(avg {top['avg']:.4f}, n={top['n']})")
        print(f"  ✗ Reduce '{bottom['value']}' for {field} "
              f"(avg {bottom['avg']:.4f}, n={bottom['n']})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare past posts to surface winning patterns")
    parser.add_argument("--brand", required=True, help="Brand folder name")
    parser.add_argument("--metric", default="engagement_rate",
                        choices=["engagement_rate", "likes", "shares", "comments",
                                 "impressions", "saves", "click_throughs"],
                        help="Metric to rank by (default: engagement_rate)")
    parser.add_argument("--by", default=None,
                        choices=["theme", "narrative_style", "hook_pattern",
                                 "visual_style", "audience_segment", "format"],
                        help="Field to break down by (default: all)")
    parser.add_argument("--top", type=int, default=5, help="Top N to show (default: 5)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of human-readable")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    brand_dir = repo_root / "brands" / args.brand
    if not brand_dir.exists():
        print(f"❌ Brand folder not found: {brand_dir}", file=sys.stderr)
        sys.exit(1)

    content_mix_path = brand_dir / "content-mix.md"
    perf_log_path = brand_dir / "performance-log.md"

    if not content_mix_path.exists():
        print(f"❌ {content_mix_path} not found", file=sys.stderr)
        sys.exit(1)
    if not perf_log_path.exists():
        print(f"❌ {perf_log_path} not found", file=sys.stderr)
        sys.exit(1)

    posts = parse_content_mix(content_mix_path)
    log = parse_performance_log(perf_log_path)
    enriched = correlate_posts(posts, log)

    if args.json:
        output = {
            "brand": args.brand,
            "metric": args.metric,
            "total_posts": len(enriched),
            "posts_with_metric": sum(
                1 for p in enriched
                if isinstance(p.get("engagement", {}).get(args.metric), (int, float))
            ),
            "by_field": {},
        }
        for field in ["theme", "narrative_style", "hook_pattern",
                      "visual_style", "audience_segment", "format"]:
            output["by_field"][field] = aggregate_by_field(enriched, field, args.metric)
        print(json.dumps(output, indent=2))
        return

    print(f"=== Comparing past posts for '{args.brand}' ===")
    print(f"Metric: {args.metric}")

    print_summary(enriched, args.metric)
    print_by_platform(enriched, args.metric)

    fields = [args.by] if args.by else [
        "theme", "narrative_style", "hook_pattern", "visual_style", "audience_segment", "format"
    ]
    for field in fields:
        print_field_breakdown(enriched, field, args.metric, top_n=args.top)

    print(f"\n=== Actionable Suggestions ===\n")
    for field in fields:
        print_suggestions(enriched, field, args.metric, top_n=args.top)

    print(f"\n=== Next steps ===\n")
    print(f"  - Run weekly: python scripts/compare_performance.py --brand {args.brand}")
    print(f"  - Use winning patterns to inform next batch")
    print(f"  - Update brands/{args.brand}/content-mix.md with new theme tags as you iterate")


if __name__ == "__main__":
    main()