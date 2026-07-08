# Content Pull — Sources for Weekly Themes

> How the agent pulls material for content generation. Updated 2026-07-07 (added scraper fallback chain).

---

## Why this doc exists

Every post needs raw material — themes, stories, observations, facts. Without a content pull layer, the agent defaults to generic AI writing. This doc defines where material comes from and how to extract it.

---

## Source priority

1. **User-supplied** (paste from chat, notes, voice memo transcript) — highest signal
2. **Internal project repos** (GitHub: AutonoLabs org) — what's shipped, PRs, issues, milestones
3. **Internal vault** (`/Users/Shared/vaults/autonobrain/`) — decisions, ADRs, meeting notes
4. **Past posts** (this brand's social history) — performance data, what worked
5. **Saved links** (user's read-later, bookmarks) — outside articles of interest
6. **Public sources** (brand's own website, blog, press) — only when accessible
7. **News/perplexity** (current events, research) — last resort, time-sensitive

---

## Per-source extraction methods

### 1. User-supplied (chat paste)

**Best for:** Specific stories, recent events, opinions the user wants to share.

**How:**
- User pastes text or types in chat
- Agent extracts: the core claim, the story, the implication
- Asks clarifying questions if context is ambiguous
- Saves excerpt to `brands/<brand>/inbox/user-said-<date>.md`

**Pitfall:** User often pastes fragments. Ask for completion before extracting themes.

---

### 2. Internal project repos (GitHub)

**Best for:** Technical progress, product updates, "what we shipped" content.

**How:**
```python
# For each AutonoLabs repo:
- Recent merged PRs (last 7 days)
- Open issues with engagement
- Recent commits to main
- Release notes
```

**Tools:** `gh` CLI or GitHub MCP (`mcp_github_*`).

**Output:** List of shipped features, fixes, decisions. Feed into weekly theme.

**Pitfall:** Most PRs aren't post-worthy. Filter for: user-facing changes, novel decisions, technical milestones.

---

### 3. Internal vault

**Best for:** Strategic decisions, market positioning, "why we made this choice" content.

**How:**
- Read recent ADRs from `/Users/Shared/vaults/autonobrain/10 - Projects/`
- Read meeting notes from `/Users/Shared/vaults/autonobrain/30 - Resources/meetings/` (if exists)
- Pull quotes from design docs

**Pitfall:** Vault is opinionated and dense. Extract the "why" and "what changed," not the implementation details.

---

### 4. Past posts (memory db)

**Best for:** Understanding what worked, what didn't, voice convergence.

**How:**
```sql
SELECT platform, caption, impressions, engagement_rate, posted_at
FROM posts
WHERE brand = '<brand>' AND posted_at > date('now', '-90 days')
ORDER BY engagement_rate DESC;
```

**Pitfall:** Engagement rate is platform-specific. Don't compare absolute numbers across platforms.

---

### 5. Saved links (user's bookmarks)

**Best for:** Reacting to industry news, citing sources, positioning.

**How:**
- Read from user's bookmarking service (if accessible)
- Or user pastes links into chat

**Pitfall:** External content is ephemeral. Screenshot or quote carefully; never paraphrase in a way that misrepresents the source.

---

### 6. Public sources (brand's own site)

**Best for:** Pulling positioning, product details, founding story.

**How — fallback chain (CRITICAL):**

1. **Try `web_extract` via Blotato MCP first** (handles some JS rendering)
2. **Try `playwright` MCP** (full browser, handles all JS) — **if available**
3. **Try raw `curl`** (works for static HTML)
4. **Ask user to paste rendered text** — last resort, but reliable

**Pitfall:** Many modern brand sites are JS SPAs that return empty HTML to curl. Plan for this.

**Specific script for sites that fail curl:**

```bash
# Try playwright first
playwright-mcp scrape --url <url>

# If playwright unavailable, use blotato source extractor
mcp_blotato_blotato_create_source sourceType=article url=<url>

# Last resort: ask user
"Hey, that site is JS-rendered. Can you paste the homepage text?"
```

---

### 7. News / research (perplexity)

**Best for:** Time-sensitive posts (industry news, regulatory changes, trending topics).

**How:**
```python
mcp_blotato_blotato_create_source(
    sourceType="perplexity-query",
    text="<specific question>"
)
```

**Pitfall:** Perplexity sometimes hallucinates. For anything that goes into a verified-fact, get user confirmation before citing.

---

## Weekly theme generation

Once material is pulled, distill into a weekly theme:

**Theme components:**
1. **The core claim** (one sentence: "the boring plumbing that makes everything work")
2. **The angle** (3-5 angles to explore across platforms)
3. **The narrative style** (from `docs/narrative-styles.md`)
4. **The hook pattern** (from `docs/platform-hooks.md`)

**Example week:**
- Brand: AllSquared
- Theme: "Why FCA regulation is the boring foundation"
- Angles: [history of escrow scams, what FCA-regulated means in practice, why we took 8 months, what disputes look like]
- Style: Contrarian Frame + The Process Reveal
- Hooks: bold statement, specific number, question

---

## Output structure

Weekly content batch goes to:
```
brands/<brand>/weeks/<YYYY>-<W##>/
├── captions.md         # all platform captions
├── media-briefs.md     # all higgsfield prompts
└── notes.md            # source material, theme, why this week
```

---

## Source-attribution rule

**Every post must be traceable to a source.** If you can't point to where the claim came from, don't make the claim.

- ✅ "I spent 8 months on this" (lived experience)
- ✅ "FCA client money rules require X" (cite FCA handbook)
- ❌ "Studies show that 70% of escrow platforms..." (where's the study?)

This is the verified-facts gate enforced at generation time.

---

## When to ask the user for material

Default to pulling automatically. Ask the user only when:
- Public source is fully blocked (JS SPA + no playwright)
- Material is too recent to be in any archive
- User has a personal story only they can tell
- Voice exemplars are needed (paste 5-10 past posts)

---

## Updates to this doc

When new source types become available (new integrations, new MCPs), when extraction methods fail, when user prefers a different input mode — update here.