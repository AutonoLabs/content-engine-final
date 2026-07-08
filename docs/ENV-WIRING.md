# ENV — Wiring API Keys & Accounts

> Step-by-step: where to get each key, what it does, what breaks if it's missing.

---

## Required keys

### BLOTATO_API_KEY

**What it does:** Authenticate with Blotato for publishing + account management.

**Get it:**
1. Sign up at [blotato.com](https://blotato.com)
2. Dashboard → Settings → API
3. Generate new key
4. Copy to `.env`

**Without it:** Cannot publish posts. Cannot list accounts.

**Monthly cost:** $19-$99 depending on plan + account count.

---

### HIGGSFIELD_API_KEY (optional but recommended)

**What it does:** Generate video media (Kling 3.0, Seedance 2.0 4K, Veo 3.1, Sora 2 Max, Grok Video, Hailuo 2.3) from media briefs.

**Get it:**
1. Sign up at [higgsfield.ai](https://higgsfield.ai)
2. Subscribe (Ultra plan ~$99/mo gives access to all models + 6000 credits)
3. Dashboard → API → Generate key
4. Copy to `.env`

**Without it:** Cannot auto-generate video. Use manual-media mode (user generates in Higgsfield web UI, drops files in `inbox/`).

**Monthly cost:** $99/mo (Ultra plan).

**Important:** Automation workflows must use credit mode. Unlimited features are explicitly gated against automation per ToS. Don't route cron jobs through "unlimited" mode.

---

## Optional keys

### OPENAI_API_KEY

**What it does:** Backup research + voice profile refinement via Perplexity-style queries.

**Get it:** [platform.openai.com](https://platform.openai.com)

**Without it:** System uses Perplexity via Blotato for research.

**Monthly cost:** Pay-as-you-go ($5-$30 typical).

---

### XAI_API_KEY

**What it does:** X (Twitter) search for trend research + AI-tell monitoring.

**Get it:** [x.ai](https://x.ai)

**Without it:** X trends ignored. Other platforms unaffected.

**Monthly cost:** Pay-as-you-go ($10-$20 typical).

---

### ANTHROPIC_API_KEY

**What it does:** Optional — use Claude API for content generation instead of running this engine manually.

**Get it:** [console.anthropic.com](https://console.anthropic.com)

**Without it:** Use this engine manually (you run the skills yourself in your own LLM UI like Claude.ai, Cursor, etc.).

**Monthly cost:** $20+ depending on usage.

---

### PERPLEXITY_API_KEY

**What it does:** Research queries for trend monitoring + content-pull.

**Get it:** [perplexity.ai](https://perplexity.ai)

**Without it:** Use OpenAI or skip research.

---

## Blotato account wiring

For each platform you want to publish on, you must connect the account in Blotato first:

| Platform | Setup steps |
|---|---|
| **Twitter/X** | Blotato → Connect X → OAuth flow → Done |
| **LinkedIn** | Blotato → Connect LinkedIn → OAuth → Done |
| **Instagram** | Blotato → Connect IG Business → OAuth → Done (requires IG Business account) |
| **TikTok** | Blotato → Connect TikTok → OAuth → Done |
| **YouTube** | Blotato → Connect YT → OAuth → Done |
| **Threads** | Blotato → Connect Threads → OAuth → Done |
| **Facebook** | Blotato → Connect FB → OAuth → Done (requires FB Page) |
| **Pinterest** | Blotato → Connect Pinterest → OAuth → Done |

After connection, run:
```bash
python scripts/blotato_list_accounts.py
```

Save the IDs to `brands/<your-brand>/blotato-accounts.md`.

---

## File structure

`.env` (DO NOT COMMIT — it's in .gitignore):
```
BLOTATO_API_KEY=blat_xxxxxxxxxxxx
HIGGSFIELD_API_KEY=hf_xxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxx
XAI_API_KEY=xai-xxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxx
```

`.env.example` (committed — placeholder values):
```
BLOTATO_API_KEY=your_key_here
HIGGSFIELD_API_KEY=your_key_here
...
```

---

## Security best practices

1. **Never commit `.env`** — it's in `.gitignore`
2. **Use environment-specific keys** — different keys for dev/staging/prod
3. **Rotate keys quarterly** — Blotato + Higgsfield both support this
4. **Use scoped keys** — Blotato supports read-only + read-write; use read-only when possible
5. **Audit key usage** — Blotato dashboard shows usage by key

---

## What if a key leaks?

1. **Immediately rotate** — Blotato/Higgsfield dashboards
2. **Audit usage** — check for unexpected posts
3. **Document incident** — log in `docs/INCIDENTS.md`

---

**Last updated:** 2026-07-08