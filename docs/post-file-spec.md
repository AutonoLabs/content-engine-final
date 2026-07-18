# Post File Spec

> One file per post: `brands/<brand>/weeks/<YYYY-W##>/post-NN-<platform>.md`.
> YAML frontmatter is the machine state; the markdown body is the human draft.
> Every script reads/writes the frontmatter — no more `--text "..."` on the
> shell and no manual content-mix logging.

---

## Format

```markdown
---
platform: linkedin          # blotato platform key
format: text-only           # docs/content-type-taxonomy.md
theme: retention
narrative: specific-number
hook: statement
visual: ""                  # visual style, if any
audience: uk-project-owners
status: draft               # draft | validated | approved | scheduled | published | rejected
schedule: "2026-07-21T09:00:00Z"   # optional; blank = publish on `engine schedule`
media:                      # optional; local paths or URLs
  - weeks/2026-W30/assets/01.png
post_url: ""                # filled by engine after publish
submission_id: ""           # filled by engine after publish
---

# W30 — Post 1 — LinkedIn

## Caption

The caption text goes here...
```

## Status lifecycle

```
draft → validated → approved → scheduled → published
                 ↘ rejected
```

- `engine validate` — draft → validated (runs validate_post.py incl. compliance.yaml)
- **Human approval** — validated → approved. In the automated flow this is the
  PR review: approving/merging the week PR marks posts approved.
- `engine schedule` — approved → scheduled/published via Blotato, resolves the
  account ID from `brand.yaml`, writes `submission_id`/`post_url` back, and
  appends the content-mix entry automatically.

## Legacy files

Files without frontmatter still parse (platform inferred from filename,
status `draft`). The first `engine` write promotes them to frontmatter.
