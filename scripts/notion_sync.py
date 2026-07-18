#!/usr/bin/env python3
"""
notion_sync — push portfolio + post pipeline state to the Notion dashboard.

The dashboard is two Notion databases (created once, IDs stored in
portfolio.yaml under `notion:`):
- Brands DB: one row per brand (group, sector, cadence, post counts, wiring)
- Posts DB:  one row per post file (brand, week, platform, format, status, URL)

Rows are upserted by a unique Key property, so this is safe to run on a cron
(the daily-measure workflow runs it after performance pull).

Env: NOTION_API_KEY (integration token with access to the dashboard page).

Usage:
    python scripts/notion_sync.py            # sync everything
    python scripts/notion_sync.py --brand allsquared
"""

from __future__ import annotations

import argparse
import os
import sys

import requests

import brand_config

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def _headers() -> dict:
    key = os.getenv("NOTION_API_KEY")
    if not key:
        sys.exit("ERROR: NOTION_API_KEY not set (see docs/ENV-WIRING.md)")
    return {
        "Authorization": f"Bearer {key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _find_by_key(db_id: str, key: str) -> str | None:
    r = requests.post(
        f"{NOTION_API}/databases/{db_id}/query",
        headers=_headers(),
        json={"filter": {"property": "Key", "rich_text": {"equals": key}}},
        timeout=30,
    )
    r.raise_for_status()
    results = r.json().get("results", [])
    return results[0]["id"] if results else None


def _upsert(db_id: str, key: str, properties: dict) -> None:
    properties["Key"] = {"rich_text": [{"text": {"content": key}}]}
    page_id = _find_by_key(db_id, key)
    if page_id:
        r = requests.patch(f"{NOTION_API}/pages/{page_id}", headers=_headers(),
                           json={"properties": properties}, timeout=30)
    else:
        r = requests.post(f"{NOTION_API}/pages", headers=_headers(),
                          json={"parent": {"database_id": db_id},
                                "properties": properties}, timeout=30)
    r.raise_for_status()


def _title(text: str) -> dict:
    return {"title": [{"text": {"content": text}}]}


def _select(value: str | None) -> dict:
    return {"select": {"name": value or "unset"}}


def _rich(text: str) -> dict:
    return {"rich_text": [{"text": {"content": text[:2000]}}]}


def sync_brand(brands_db: str, posts_db: str, brand: str) -> int:
    cfg = brand_config.load_brand(brand)
    posts = brand_config.all_posts(brand)
    counts: dict[str, int] = {}
    for p in posts:
        s = p["meta"].get("status", "draft")
        counts[s] = counts.get(s, 0) + 1
    wired = [k for k, v in cfg["platforms"].items() if v.get("account_id")]

    _upsert(brands_db, brand, {
        "Name": _title(cfg.get("display_name", brand)),
        "Group": _select(cfg.get("group")),
        "Sector": _select(cfg.get("sector")),
        "Cadence": _select(cfg.get("cadence", "weekly")),
        "Weeks": {"number": len(brand_config.list_weeks(brand))},
        "Posts": {"number": len(posts)},
        "Pipeline": _rich(", ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
                          or "no posts yet"),
        "Wired platforms": _rich(", ".join(wired) or "none"),
    })

    for p in posts:
        meta = p["meta"]
        week = meta.get("week", "?")
        key = f"{brand}/{week}/{p['path'].name}"
        props = {
            "Post": _title(f"{brand} · {week} · {p['path'].stem}"),
            "Brand": _select(brand),
            "Week": _rich(week),
            "Platform": _select(meta.get("platform")),
            "Format": _select(meta.get("format")),
            "Status": _select(meta.get("status", "draft")),
        }
        if meta.get("post_url"):
            props["URL"] = {"url": meta["post_url"]}
        _upsert(posts_db, key, props)

    return len(posts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync repo state to Notion dashboard")
    parser.add_argument("--brand", help="Sync one brand only")
    args = parser.parse_args()

    try:
        from dotenv import load_dotenv
        load_dotenv(brand_config.REPO_ROOT / ".env")
    except ImportError:
        pass

    notion = brand_config.load_portfolio().get("notion") or {}
    brands_db = os.getenv("NOTION_BRANDS_DB_ID") or notion.get("brands_db_id")
    posts_db = os.getenv("NOTION_POSTS_DB_ID") or notion.get("posts_db_id")
    if not brands_db or not posts_db:
        sys.exit("ERROR: Notion DB IDs missing. Fill portfolio.yaml `notion:` "
                 "(or set NOTION_BRANDS_DB_ID / NOTION_POSTS_DB_ID).")

    brands = [args.brand] if args.brand else brand_config.portfolio_brands()
    total = 0
    for brand in brands:
        n = sync_brand(brands_db, posts_db, brand)
        print(f"  ✓ {brand}: brand row + {n} post row(s)")
        total += n
    url = notion.get("dashboard_page_url")
    print(f"\nSynced {len(brands)} brand(s), {total} post(s)."
          + (f"\nDashboard: {url}" if url else ""))


if __name__ == "__main__":
    main()
