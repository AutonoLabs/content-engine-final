# Content Engine — Final

> Multi-business content engine for the Autono Labs portfolio. Anti-AI-feel by default, hooks-first for scroll-stopping, voice-tuned per brand, content-mix-tracked, AI-tell monitor keeps it current.

**Anyone can clone this repo, follow `ONBOARDING.md`, and have a brand publishing within 2 weeks.**

🔗 **Repo:** https://github.com/AutonoLabs/content-engine-final
📖 **Start here:** [`ONBOARDING.md`](./ONBOARDING.md)
🐛 **Issues:** https://github.com/AutonoLabs/content-engine-final/issues

---

## What this is

A complete content engine + publishing pipeline for any brand:

1. **Voice layer** — generates a brand-specific voice profile from a brief (no seed posts needed)
2. **Hook + narrative + visual layer** — platform-specific patterns that stop scroll
3. **Anti-AI layer** — banned phrases + quarterly AI-tell monitor
4. **Claim-verification layer** — sector-aware (FCA, FDA, FTC, state bar)
5. **Diversity layer** — rotation enforcement across format / theme / style / hook / visual / audience
6. **Publishing layer** — Blotato integration, multi-platform scheduling
7. **Tracking layer** — content-mix + performance-log in markdown
8. **Skill layer** — four generalizable skills that work for any new business

---

## Quick start (60 seconds)

```bash
git clone https://github.com/AutonoLabs/content-engine-final.git
cd content-engine-final
pip install -r requirements.txt
cp .env.example .env  # Fill in keys (see docs/ENV-WIRING.md)

# Onboard your first brand
python scripts/onboard_brand.py --name mybrand --sector fintech

# Fill in brand-brief.md, then run voice-from-brief skill
# Read ONBOARDING.md for full flow
```

---

## What's in the box

```
content-engine-final/
├── ONBOARDING.md                    # Clone → publish in 2 weeks
├── README.md                        # This file
├── LICENSE                          # MIT
├── .env.example                     # API keys template
├── .gitignore
├── requirements.txt
├── docs/                            # Architecture + rules
│   ├── platform-hooks.md
│   ├── visual-hooks.md
│   ├── audience-demographics.md
│   ├── narrative-styles.md
│   ├── anti-ai-feel.md
│   ├── ai-tell-history.md
│   ├── content-type-taxonomy.md
│   ├── diversity-rules.md
│   ├── content-pull.md
│   ├── publish-runbook.md
│   ├── media-brief.template.md
│   ├── voice-profile.template.md
│   ├── ENV-WIRING.md
│   ├── WEEKLY-BATCH-FLOW.md
│   └── TROUBLESHOOTING.md
├── prompts/                         # Per-platform generation prompts
│   ├── linkedin.md
│   ├── x.md
│   ├── instagram.md
│   ├── tiktok.md
│   ├── youtube-shorts.md
│   └── threads.md
├── skills/                          # Generalizable skill layer (works for any new business)
│   ├── voice-from-brief.md
│   ├── ai-tell-monitor.md
│   ├── claim-verifier.md
│   └── brand-adapter.md
├── brands/                          # Per-brand folder templates
│   ├── voice-profile.template.md
│   ├── target-audience.template.md
│   ├── verified-facts.template.md
│   ├── content-mix.template.md
│   ├── performance-log.template.md
│   ├── brand-brief.template.md
│   └── blotato-accounts.template.md
├── scripts/                         # Operational pipeline code
│   ├── blotato_client.py            # Blotato API wrapper
│   ├── blotato_list_accounts.py
│   ├── blotato_publish.py
│   ├── blotato_get_post_status.py
│   ├── higgsfield_generate.py       # Video generation (6 models)
│   ├── content_pull.py              # Multi-source extraction (playwright → blotato → curl)
│   ├── performance_pull.py          # Engagement tracking
│   ├── validate_post.py             # Anti-AI + diversity + claim checks
│   └── onboard_brand.py             # New-brand bootstrap
└── examples/                        # Reference brand
    └── allsquared/
        ├── README.md
        ├── voice-profile.md
        ├── target-audience.md
        ├── verified-facts.md
        ├── content-mix.md
        └── weeks/2026-W28/
            ├── captions.md
            └── media-briefs.md
```

---

## What does it actually do?

**For each brand in the portfolio:**

1. **Generate voice profile** from brand brief (no seed posts needed) — `skills/voice-from-brief.md`
2. **Plan weekly batch** with diversity enforcement (rotation across format / theme / style / hook / visual / audience / platform) — `docs/diversity-rules.md` + `docs/WEEKLY-BATCH-FLOW.md`
3. **Draft captions** using platform-specific hooks + narrative styles — `prompts/<platform>.md` + `docs/platform-hooks.md` + `docs/narrative-styles.md`
4. **Verify claims** against `brands/<brand>/verified-facts.md` (sector-aware: FCA / FDA / FTC / state bar) — `skills/claim-verifier.md`
5. **Validate post** against anti-AI + diversity rules — `scripts/validate_post.py`
6. **Generate or drop media** via Higgsfield or manual-media mode — `scripts/higgsfield_generate.py`
7. **Publish via Blotato** across 7+ platforms — `scripts/blotato_publish.py`
8. **Track performance** + diversity — `scripts/performance_pull.py` + `brands/<brand>/content-mix.md` + `performance-log.md`
9. **Refine voice** over time via edit pass — `brands/<brand>/exemplars/edits/`
10. **Quarterly AI-tell refresh** — `skills/ai-tell-monitor.md`

---

## Why it's different

**vs. plain LLM use:**
- Anti-AI banned phrases enforced + AI-tell monitor keeps it current
- Voice profile converges to actual brand via edit pass
- Claim verification prevents stat hallucination
- Diversity rules prevent boring sameness

**vs. other content tools:**
- Multi-business, multi-platform, multi-format (16 content types)
- Works for any new business without seed posts
- Sector-aware compliance (health, finance, legal, professional)
- No vendor lock-in (markdown + scripts, not SaaS)
- MIT licensed, fully public, fork-friendly

---

## Architecture principles

1. **Markdown-first.** All knowledge in plain `.md` files. Version-controlled, fork-friendly, no proprietary format.
2. **Voice from brief, not from posts.** New brands don't need seed posts to start.
3. **Anti-AI by default.** Banned phrases + structural patterns. Quarterly refresh.
4. **Verified facts are HARD.** No unverified claims in posts.
5. **Diversity enforced.** No boring sameness.
6. **Edit pass is the loop.** Voice converges over time.
7. **Multi-format.** 16 content types, rotation enforced.
8. **Multi-platform.** 7+ platforms supported via Blotato.
9. **Scripts over SaaS.** Run your own pipeline.
10. **Fork-friendly.** MIT license, public repo, anyone can use.

---

## Tested & working

```
✓ python scripts/validate_post.py — anti-AI catches banned phrases
✓ python scripts/onboard_brand.py --help — onboarding ready
✓ python scripts/higgsfield_generate.py --list-models — 6 models available
✓ python scripts/blotato_list_accounts.py — account discovery
✓ All 9 scripts parse cleanly
```

---

## Sector support

| Sector | Sector rules in claim-verifier | Brand examples |
|---|---|---|
| Consumer health (FDA/FTC) | ✓ | Yapper |
| Fintech (FCA/SEC) | ✓ | AllSquared |
| Legal (state bar) | ✓ | (future) |
| Professional services | ✓ | (future) |
| Education / creative | ✓ | TreeAI, etc. |
| Other | ✓ | any |

---

## Cost (per brand, monthly)

- **Blotato:** $19-$99 (depending on plan + account count)
- **Higgsfield Ultra:** $99/mo (6000 credits, all models)
- **Optional:** OpenAI/Anthropic/Perplexity for research ($10-$30)
- **Total:** ~$120-$230/mo per brand

Manual-media mode (skip Higgsfield) drops it to ~$20-$100/mo.

---

## Roadmap

- [ ] Cron job scheduler for weekly themes (in repo)
- [ ] Discord approval integration (messaging-based edits)
- [ ] Per-platform engagement analytics dashboard
- [ ] A/B testing framework (rotate 2 versions of same theme)
- [ ] Auto-translation for multi-language brands

---

## Support

- **New to this?** Start with `ONBOARDING.md`
- **Adding a brand?** Read `skills/brand-adapter.md`
- **Stuck?** Check `docs/TROUBLESHOOTING.md`
- **Want to extend?** Read `docs/` and `skills/`, contribute back via PR

---

## License

MIT — see `LICENSE`. Fork-friendly, use it, modify it, ship it.

---

**Built by:** Autono Labs, 2026-07-08
**Maintainer:** Autono Labs
**Status:** Active, v1.0