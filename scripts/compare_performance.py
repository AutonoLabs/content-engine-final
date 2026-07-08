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

Usage:
    python scripts/compare_performance.py --brand allsquared
    python scripts/compare_performance.py --brand allsquared --json
    python scripts/compare_performance.py --brand allsquared --metric engagement_rate
    python scripts/compare_performance.py --brand allsquared --by theme --top 5
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional


def parse_content_mix(path: Path) -> list[dict]:
    """Parse content-mix.md into list of post dicts."""
    if not path.exists():
        return []

    content = path.read_text()
    posts = []

    # Match entries like "### YYYY-MM-DD — platform — theme"
    entries = re.split(r"\n### ", content)

    for entry in entries[1:]:
        lines = entry.split("\n")
        header = lines[0].strip()

        # Parse header: "YYYY-MM-DD — platform — theme"
        parts = re.split(r"\s+—\s+", header)
        if len(parts) < 3:
            continue
        date, platform, theme = parts[0], parts[1], parts[2]

        post = {
            "date": date.strip(),
            "platform": platform.strip(),
            "theme": theme.strip(),
        }

        # Parse fields (look for "- **Field:** value" OR "- Field: value")
        for line in lines[1:]:
            match = re.match(r"-\s+\*?\*?(.+?):\*?\*?\s+(.+)", line.strip())
            if match:
                field = match.group(1).strip().lower().replace(" ", "_")
                value = match.group(2).strip()
                post[field] = value

        posts.append(post)

    return posts


def parse_performance_log(path: Path) -> dict:
    """
    Parse performance-log.md into dict keyed by (date, platform) → engagement dict.

    Returns: {("2026-07-08", "linkedin"): {"impressions": N, "likes": N, ...}, ...}
    """
    if not path.exists():
        return {}

    content = path.read_text()
    log = {}

    entries = re.split(r"\n### ", content)

    for entry in entries[1:]:
        lines = entry.split("\n")
        header = lines[0].strip()

        # Parse header: "YYYY-MM-DD — platform — theme"
        parts = re.split(r"\s+—\s+", header)
        if len(parts) < 3:
            continue
        date, platform = parts[0].strip(), parts[1].strip()

        engagement = {}
        for line in lines[1:]:
            # Match "- **Field:** value" OR "- Field: value"
            match = re.match(r"-\s+\*?\*?(.+?):\*?\*?\s+(.+)", line.strip())
            if match:
                field = match.group(1).strip().lower()
                value_str = match.group(2).strip()

                # Try to parse as number
                value_clean = re.sub(r"[^\d.]", "", value_str)
                if value_clean and value_str != "N/A":
                    try:
                        if "%" in value_str:
                            engagement[field] = float(value_clean) / 100
                        else:
                            engagement[field] = float(value_clean) if "." in value_clean else int(value_clean)
                    except ValueError:
                        engagement[field] = value_str
                else:
                    engagement[field] = None

        log[(date, platform)] = engagement

        # Normalize common metric aliases
        if "engagement_rate" in engagement:
            pass  # already correct
        elif "engagement rate" in {k.lower() for k in engagement}:
            for k in list(engagement.keys()):
                if k.lower() == "engagement rate":
                    engagement["engagement_rate"] = engagement.pop(k)

    return log


def correlate_posts(posts: list[dict], log: dict) -> list[dict]:
    """Merge content-mix entries with performance-log engagement."""
    enriched = []
    for post in posts:
        key = (post["date"], post["platform"])
        engagement = log.get(key, {})
        post["engagement"] = engagement
        enriched.append(post)
    return enriched


def aggregate_by_field(posts: list[dict], field: str, metric: str) -> list[dict]:
    """Aggregate engagement by a field (theme, narrative_style, etc.)."""
    buckets = defaultdict(list)
    for post in posts:
        key = post.get(field, "").strip()
        value = post.get("engagement", {}).get(metric)
        if key and value is not None and isinstance(value, (int, float)):
            buckets[key].append(value)

    return [
        {
            "field": field,
            "value": key,
            "n": len(values),
            "avg": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "total": sum(values),
        }
        for key, values in buckets.items()
    ]


def print_report(by_field: str, results: list[dict], metric: str, top_n: int = 5):
    """Print formatted report."""
    print(f"\n=== Performance by {by_field} (sorted by {metric}, n={sum(r['n'] for r in results)} posts) ===\n")

    # Sort by avg metric desc
    sorted_results = sorted(results, key=lambda r: r["avg"], reverse=True)

    if not sorted_results:
        print(f"  No data yet for {by_field}.")
        return

    print(f"{by_field:30s}  {'posts':>6s}  {'avg':>10s}  {'min':>8s}  {'max':>8s}")
    print("-" * 70)

    print("\nTOP:")
    for r in sorted_results[:top_n]:
        print(f"  {r['value']:28s}  {r['n']:>6d}  {r['avg']:>10.4f}  {r['min']:>8.4f}  {r['max']:>8.4f}")

    if len(sorted_results) > top_n:
        print(f"\nBOTTOM (of {len(sorted_results)}):")
        for r in sorted_results[-min(top_n, len(sorted_results)):]:
            print(f"  {r['value']:28s}  {r['n']:>6d}  {r['avg']:>10.4f}  {r['min']:>8.4f}  {r['max']:>8.4f}")


def print_summary(enriched: list[dict], metric: str):
    """Print overall summary."""
    with_metric = [p for p in enriched if p.get("engagement", {}).get(metric) is not None]

    if not with_metric:
        print(f"\nNo posts have '{metric}' data yet.")
        print(f"Total posts tracked: {len(enriched)}")
        print(f"\n💡 To populate engagement data:")
        print(f"   python scripts/performance_pull.py --brand <brand> --days 30")
        print(f"   Or manually fill in brands/<brand>/performance-log.md")
        return

    values = [p["engagement"][metric] for p in with_metric]
    print(f"\n=== Overall Summary ===\n")
    print(f"  Posts with {metric}: {len(with_metric)}")
    print(f"  Average: {sum(values) / len(values):.4f}")
    print(f"  Best: {max(values):.4f}")
    print(f"  Worst: {min(values):.4f}")
    print(f"  Median: {sorted(values)[len(values) // 2]:.4f}")

    # By platform
    platform_buckets = defaultdict(list)
    for p in with_metric:
        platform_buckets[p["platform"]].append(p["engagement"][metric])

    print(f"\n=== By Platform ===\n")
    for platform, vals in sorted(platform_buckets.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
        print(f"  {platform:20s}  n={len(vals):>3d}  avg={sum(vals)/len(vals):.4f}")


def main():
    parser = argparse.ArgumentParser(description="Compare past posts, surface winning patterns")
    parser.add_argument("--brand", required=True, help="Brand name")
    parser.add_argument("--by", action="append",
                        choices=["theme", "narrative_style", "hook_pattern", "visual_style",
                                 "audience_segment", "format", "platform"],
                        help="Aggregate by field (can repeat)")
    parser.add_argument("--metric", default="engagement_rate",
                        choices=["impressions", "reach", "likes", "reactions", "comments",
                                 "shares", "reposts", "engagement_rate", "saves", "click_throughs"],
                        help="Engagement metric to compare (default: engagement_rate)")
    parser.add_argument("--top", type=int, default=5, help="Show top N")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    brand_path = Path(f"brands/{args.brand}")
    content_mix = brand_path / "content-mix.md"
    perf_log = brand_path / "performance-log.md"

    if not content_mix.exists():
        print(f"❌ {content_mix} not found", file=sys.stderr)
        sys.exit(1)

    posts = parse_content_mix(content_mix)
    log = parse_performance_log(perf_log)
    enriched = correlate_posts(posts, log)

    if args.json:
        output = {
            "brand": args.brand,
            "total_posts": len(enriched),
            "posts_with_metric": sum(1 for p in enriched if p.get("engagement", {}).get(args.metric) is not None),
            "by_field": {}
        }
        for field in (args.by or ["theme", "narrative_style", "hook_pattern", "visual_style"]):
            output["by_field"][field] = aggregate_by_field(enriched, field, args.metric)
        print(json.dumps(output, indent=2))
        return

    print(f"\n=== Comparing past posts for '{args.brand}' ===")
    print(f"Metric: {args.metric}")

    print_summary(enriched, args.metric)

    fields_to_check = args.by or ["theme", "narrative_style", "hook_pattern", "visual_style"]
    for field in fields_to_check:
        results = aggregate_by_field(enriched, field, args.metric)
        print_report(field, results, args.metric, args.top)

    # Actionable suggestions
    print(f"\n=== Actionable Suggestions ===\n")
    for field in ["theme", "narrative_style", "hook_pattern", "visual_style"]:
        results = aggregate_by_field(enriched, field, args.metric)
        if not results:
            continue
        sorted_results = sorted(results, key=lambda r: r["avg"], reverse=True)
        if len(sorted_results) >= 2 and sorted_results[0]["n"] >= 2:
            top = sorted_results[0]
            bottom = sorted_results[-1]
            if top["avg"] > bottom["avg"] * 1.5:  # 50%+ better
                print(f"  ✓ Lean into '{top['value']}' for {field} (avg {top['avg']:.4f}, n={top['n']})")
                print(f"  ✗ Reduce '{bottom['value']}' for {field} (avg {bottom['avg']:.4f}, n={bottom['n']})")

    print(f"\n=== Next steps ===\n")
    print(f"  - Run weekly: python scripts/compare_performance.py --brand {args.brand}")
    print(f"  - Use winning patterns to inform next batch")
    print(f"  - Update brands/{args.brand}/content-mix.md with new theme tags as you iterate")
    print(f"  - If no engagement data: python scripts/performance_pull.py --brand {args.brand}")


if __name__ == "__main__":
    main()