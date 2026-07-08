# Voice Profile Template

> Schema for voice profiles. Per brand × platform. Locked after extraction, refined over time.

---

## How this works

For each brand × platform, extract a voice profile from 5–10 real past posts on that platform. The profile locks:
- **Voice + rhythm** (via few-shot exemplars — actual posts)
- **Hard constraints** (length, banned patterns, structure)
- **Anti-AI-feel rules** (structural tells we engineer against)

The agent conditions on all three at generation time.

---

## Profile schema (per brand × platform)

```yaml
brand: eli-founder
platform: linkedin
seed_posts_count: 7
extracted_at: 2026-07-07

# TONE (free text, not pseudo-quantified)
tone: |
  Casual-credible. Drops commas. Uses fragments.
  Opens with hot takes. Specific over abstract.
  Names things. Mentions proper nouns.
  No preamble, no "let me share."

rhythm:
  sentence_length:
    min: 4  # words
    max: 35
    target_variance: high
  fragments_per_post: 2-4  # encourage
  paragraphs: tight_blocks  # not single-sentence per line
  paragraph_length: 2-5 sentences

# FEW-SHOT EXEMPLARS (verbatim from real posts)
# This is the strongest voice conditioner. LLM learns from these.
exemplars:
  - |
    [actual post 1, verbatim]
  - |
    [actual post 2, verbatim]
  - |
    [actual post 3, verbatim]

# ANTI-AI-FEEL HARD RULES (structural, not phrase-level)
anti_ai_rules:
  banned_structures:
    - contrast_frame: "it's not X, it's Y" → rewrite as either X or Y
    - triadic_parallelism: "fast, cheap, and good" → pick two
    - rhetorical_question_hook: "what if I told you" / "have you ever wondered" → banned as opener
    - let_me_preamble: "let me share" / "let me explain" → banned
    - sentence_per_line: no single-sentence paragraphs separated by blank lines
    - empty_intensifier: "really" / "absolutely" / "fundamentally" / "truly" / "genuinely" → use sparingly
    - closing_cta_engagement_bait: "what do you think? 👇" / "agree?" → banned
    - emoji_as_punctuation: max 1 emoji per post, never as sentence-end punctuation
  density_rule: 1.3 ideas per sentence. if a sentence is one obvious thought, cut it or add the next.
  specificity_rule: name things. if you can't name the thing, don't write the post.

# HARD CONSTRAINTS (length, structure, format)
constraints:
  length:
    min: 600
    max: 1200
    target: 800
  structure:
    closing: question_or_observation  # NOT engagement bait
    uses_lists: rarely
  emoji: never
  hashtags:
    count: 3-5
    placement: end
  banned_openers:
    - "let's dive in"
    - "in today's fast-paced world"
    - "the future is now"
    - "imagine a world where"
    - "have you ever wondered"
    - "what if i told you"
  banned_closers:
    - "what do you think?"
    - "drop a 💡 if you agree"
    - "like and share if you found this useful"
  banned_terms:
    - "delve"
    - "tapestry"
    - "realm"
    - "leverage"
    - "unleash"
    - "game-changer"
    - "seamlessly"
    - "elevate"
    - "cutting-edge"
    - "really"
    - "absolutely"
    - "fundamentally"
    - "truly"
    - "genuinely"
  banned_topics:
    - politics
    - religion
    - crypto_specifics

# REFINEMENTS (added over time from edit patterns)
refinements: []
```

---

## Anti-AI-feel rule rationale

These come from observed 2026 patterns, not folklore:

- **contrast_frame (it's not X, it's Y)** — appears in 40%+ of AI linkedin posts. structural, not phrasal. regex won't catch it; pattern rule will.
- **triadic parallelism** — humans do this too, but AI does it reflexively. limiting to 2-of-3 forces the writer to actually mean the third.
- **rhetorical question hooks** — over-deployed as AI's go-to opener pattern.
- **let_me_preamble** — almost exclusively AI.
- **sentence_per_line** — visual signature of AI generation. humans write tighter.
- **empty intensifiers** — filler. AI over-uses; humans use for actual emphasis.
- **engagement_bait closers** — not just annoying; they're a known AI signal.
- **emoji_as_punctuation** — pattern, not presence. one 🎯 per line is AI; one emoji per post is human.

Per Fable's review: regex filter theater doesn't work. These are GENERATION rules, not filter rules. The fix happens at the prompt level, not at the output level.

---

## Extraction process

For each brand × platform:

1. Read 5–10 actual past posts from `brands/<brand>/seed-posts.md`
2. Identify the dominant voice (not the average — pick the mode)
3. Pull 3 strongest exemplars verbatim
4. Note specific patterns observed:
   - Openings (how does this person actually start?)
   - Closings (how do they land?)
   - Sentence length variance (high/medium/low)
   - Use of fragments (yes/no/how often)
   - Use of specifics (proper nouns, numbers, named things)
5. Map observed patterns to tone description (free text, 2-3 sentences)
6. Lock hard constraints based on what's CONSISTENT across exemplars
7. Anti-AI rules always on (per above)

---

## Refinement loop

When Eli taps ✏️ Edit, the diff is saved. After 3+ same-pattern edits:
- Pattern auto-added to `refinements` array
- Applied to all future generations

Example convergence after 10 edits:
```yaml
refinements:
  - pattern: "Eli always cuts hooks longer than 80 chars"
    rule: "max 80 chars per hook"
    occurrences: 4
  - pattern: "Eli always removes 'just' "
    rule: "avoid 'just' as filler"
    occurrences: 6
  - pattern: "Eli adds proper nouns in 80% of edits"
    rule: "name at least one company/product/person per post"
    occurrences: 9
```

---

## Privacy

Per Fable: voice profiles + seed posts are private. Repo is private. Files in `brands/` are internal-only.

Seed posts can be deleted from repo after profile built. Git history persists — use `git filter-repo` if you really need to scrub.

---

## Why this works

The LLM gets three conditioning signals:
1. **Few-shot exemplars** — learns actual rhythm + vocabulary (strongest signal)
2. **Anti-AI rules** — prevents the structural patterns AI defaults to
3. **Hard constraints** — enforces format (length, banned phrases, structure)

Combined: the output sounds like the person, with the boring bits pre-filled, and the AI tells engineered out.

The human edit pass then catches what the model misses — and those edits feed back into the profile.

---

## Open questions

- Voice profile refresh cadence: quarterly automatic, or only on drift detection?
- How to handle a brand with no past posts (new venture)? Bootstrap from 1-paragraph description + 3 typed example posts?
- Voice drift detection: at what edit rate do we trigger profile refresh?