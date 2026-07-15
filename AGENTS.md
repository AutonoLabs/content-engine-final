# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **Python 3 CLI toolkit** (`content-engine-final`) — a multi-brand
social-content generation/validation/publishing pipeline. There is **no web
server, database, or container**; everything is standalone scripts in `scripts/`
operating on markdown files under `brands/`, `docs/`, `prompts/`, `skills/`.
See `README.md` and `ONBOARDING.md` for the full workflow.

### Running scripts
- Dependencies live in a virtualenv at `.venv/` (git-ignored). The startup update
  script creates it and installs `requirements.txt` + the Playwright Chromium
  browser. Run scripts with `.venv/bin/python scripts/<name>.py` (or activate with
  `source .venv/bin/activate` first).
- All scripts are `argparse`-based; pass `--help` to any of them for usage.

### What runs fully offline (no keys/network)
- `scripts/doctor.py` — preflight/health check.
- `scripts/onboard_brand.py --name <name> --sector <sector>` — bootstraps a brand.
- `scripts/validate_post.py` — the core content engine (anti-AI + claim + diversity checks).
- `scripts/higgsfield_generate.py --list-models` — model registry.

### What needs secrets + network (cannot run offline)
- The **Blotato publishing path** (`blotato_*.py`, `performance_pull.py`,
  `content_pull.py` blotato fallback) requires a real `BLOTATO_API_KEY` and
  outbound network. With a placeholder key these fail on DNS/HTTP — that is
  expected, not a setup bug.
- Optional providers (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `XAI_API_KEY`,
  `REPLICATE_API_TOKEN`, `HIGGSFIELD_API_KEY`) are read from `.env`. See
  `docs/ENV-WIRING.md`.

### Non-obvious gotchas
- `.env` is git-ignored and does **not** exist on a fresh checkout. Create it with
  `cp .env.example .env` before running `doctor.py`; otherwise `doctor.py` reports
  a non-fatal `MISSING required env var: BLOTATO_API_KEY` and the summary shows
  "1 issue(s) found" instead of "All checks passed" (it still exits 0 unless
  `--strict`). The placeholder value in `.env.example` is enough to make offline
  checks green.
- There is **no lint/test/build system** (no pytest, Makefile, pyproject, or CI).
  The closest checks are `python scripts/doctor.py` (add `--strict` to fail on any
  issue) and `python -m py_compile scripts/*.py` to confirm all scripts parse.
- Brand folders created under `brands/<name>/` are git-tracked — delete scratch
  brands before committing (e.g. `rm -rf brands/<name>`).
