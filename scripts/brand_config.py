#!/usr/bin/env python3
"""
brand_config — machine-readable config layer for the engine.

Sources of truth:
- portfolio.yaml                (portfolio manifest: brands, relationships, scheduling, notion)
- brands/<brand>/brand.yaml     (sector, platform->account wiring, defaults)
- brands/<brand>/compliance.yaml (optional; hard rules enforced by validate_post.py)
- post files with YAML frontmatter (docs/post-file-spec.md)

Markdown files remain the human knowledge layer; nothing here parses prose.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
BRANDS_DIR = REPO_ROOT / "brands"
PORTFOLIO_FILE = REPO_ROOT / "portfolio.yaml"

POST_FILE_RE = re.compile(r"^post-\d+.*\.md$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)

POST_STATUSES = ["draft", "validated", "approved", "scheduled", "published", "rejected"]


def load_portfolio() -> dict:
    if not PORTFOLIO_FILE.exists():
        return {"brands": {}}
    data = yaml.safe_load(PORTFOLIO_FILE.read_text()) or {}
    data.setdefault("brands", {})
    return data


def portfolio_brands() -> list[str]:
    return sorted(load_portfolio()["brands"].keys())


def load_brand(brand: str) -> dict:
    """Merged view: portfolio entry + brand.yaml (brand.yaml wins)."""
    entry = dict(load_portfolio()["brands"].get(brand) or {})
    brand_yaml = BRANDS_DIR / brand / "brand.yaml"
    if brand_yaml.exists():
        entry.update(yaml.safe_load(brand_yaml.read_text()) or {})
    entry.setdefault("name", brand)
    entry.setdefault("platforms", {})
    entry.setdefault("defaults", {})
    return entry


def load_compliance(brand: str) -> dict | None:
    path = BRANDS_DIR / brand / "compliance.yaml"
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text()) or {}


def account_for(brand: str, platform: str) -> dict:
    """Platform wiring for a brand ({} if unwired)."""
    cfg = load_brand(brand)
    return dict(cfg["platforms"].get(platform) or {})


# ─── Post files ──────────────────────────────────────────────────────────────

def week_dir(brand: str, week: str) -> Path:
    return BRANDS_DIR / brand / "weeks" / week


def list_weeks(brand: str) -> list[str]:
    weeks = BRANDS_DIR / brand / "weeks"
    if not weeks.exists():
        return []
    return sorted(d.name for d in weeks.iterdir()
                  if d.is_dir() and re.match(r"^\d{4}-W\d{2}$", d.name))


def parse_post_file(path: Path) -> dict:
    """
    Parse a post file into {meta, caption, path}.
    Frontmatter posts (docs/post-file-spec.md) are canonical; legacy files
    (no frontmatter) get platform inferred from filename and status 'draft'.
    """
    text = path.read_text()
    meta: dict = {}
    body = text
    m = FRONTMATTER_RE.match(text)
    if m:
        meta = yaml.safe_load(m.group(1)) or {}
        body = text[m.end():]
    else:
        meta["legacy"] = True
    if not meta.get("platform"):
        plat = re.search(r"post-\d+-([a-z-]+)\.md$", path.name)
        if plat:
            meta["platform"] = plat.group(1)
    meta.setdefault("status", "draft")

    cap = re.search(r"^## Caption\s*\n(.*?)(?=^## |\Z)", body, re.MULTILINE | re.DOTALL)
    caption = (cap.group(1) if cap else body).strip()
    return {"meta": meta, "caption": caption, "path": path}


def list_posts(brand: str, week: str) -> list[dict]:
    wd = week_dir(brand, week)
    if not wd.exists():
        return []
    return [parse_post_file(p) for p in sorted(wd.glob("*.md"))
            if POST_FILE_RE.match(p.name)]


def all_posts(brand: str) -> list[dict]:
    out = []
    for week in list_weeks(brand):
        for post in list_posts(brand, week):
            post["meta"].setdefault("week", week)
            out.append(post)
    return out


def update_post_meta(path: Path, updates: dict) -> None:
    """Rewrite a post file's frontmatter with updates merged in.
    Legacy files gain frontmatter (promoting them to the new spec)."""
    text = path.read_text()
    m = FRONTMATTER_RE.match(text)
    if m:
        meta = yaml.safe_load(m.group(1)) or {}
        body = text[m.end():]
    else:
        meta, body = {}, text
    meta.update(updates)
    meta.pop("legacy", None)
    fm = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip()
    path.write_text(f"---\n{fm}\n---\n{body}")
