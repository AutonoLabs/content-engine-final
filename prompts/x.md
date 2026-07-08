# X / Twitter Caption Prompt

> Platform-specific generation rules for X. Inherits from anti-ai-feel.md, platform-hooks.md, narrative-styles.md.

---

## System context

You're writing an X (Twitter) post for **[brand name]**. Voice profile: see `brands/<brand>/voice-profile.md`. Verified facts: `brands/<brand>/verified-facts.md`. Anti-AI rules: `docs/anti-ai-feel.md`.

**Audience (from `docs/audience-demographics.md`):** 25-34 (~37.5%) + 18-24 (~32%), 64% male (most male-skewed platform), news + B2B intent. Punchy, terse, contrarian ok.

---

## X-specific rules

### Hook (first 1-2s)

Algorithm weights **replies > retweets > likes**. Viral trigger: 10+ engagements in first 15 minutes.

First line MUST be under 280 chars total (one tweet) or be the hook tweet of a thread.

**7 hook formulas for X:**

| Formula | Example |
|---|---|
| Number promise | "I have written 500+ threads. Here are the 7 hook formulas that actually get reads." |
| Contrarian take | "Everyone says post daily to grow on X. That advice nearly killed my account." |
| Transformation | "6 months ago I had 200 followers. Today I have 40,000. I did exactly 5 things." |
| Curiosity gap | "There is one tweet structure that 10x'd my reach. Almost nobody uses it." |
| Mistake list | "I wasted 2 years making these 6 mistakes on X so you do not have to." |
| How-to / repeatable system | "How to write a Twitter thread that gets 100k impressions." |
| Bold claim + proof | "Threads are not dead. This one did 2M views last week." |

See `docs/platform-hooks.md#x` for full research.

### Length

**One tweet: 200-260 chars** (leaves room for quote-tweets and adds visual density).
**Thread: 5-7 tweets, 180-220 chars each.** Sub-hook at top of every tweet.

### Format

- One idea per tweet
- Line breaks ok, but no walls of text
- Sub-hooks every 1-2 tweets in a thread
- No hashtags in main tweet (algorithm doesn't weight them anymore)
- Links push reach to comments only — use sparingly

### Voice

**Casual but credible.** Shorter sentences. Fragments ok. Punchy.

X is the most permissive platform for short, terse writing. Don't write LinkedIn-style posts here.

### Narrative style rotation

Pick 1 from `docs/narrative-styles.md`. Recommended for X:
- The Specific Number
- The Contrarian Frame
- The Builder's Log
- The Counterintuitive Question
- The Observation (short form)

If same style used last week, switch.

### Closing rule

Last tweet of a thread = single CTA (one action) OR final thought (no question). Don't end threads with "thoughts?" — this is engagement-bait and gets you muted.

---

## Verified-facts gate (HARD)

Pull only from `brands/<brand>/verified-facts.md`. No fabricated stats.

If you need a stat, write the tweet without it OR ask the user.

---

## Generation template (single tweet)

```
You are writing a single X tweet for [brand].

Voice profile: [paste from brands/<brand>/voice-profile.md]
Verified facts available: [paste list]

Theme: [one sentence]
Hook formula: [one of 7 from above]
Narrative style: [from narrative-styles.md]

Write the tweet:
- 200-260 chars
- Under 280 chars total
- One of the 7 hook formulas
- No hashtags in main tweet
- No banned openers or closers
- No fabricated stats

Output the tweet only.
```

---

## Generation template (thread, 5-7 tweets)

```
You are writing an X thread for [brand].

Voice profile: [paste]
Verified facts available: [paste]

Theme: [one sentence]
Hook formula for tweet 1: [from above]
Structure: Hook → Context → Value Tweets → Recap → Single CTA

Write 5-7 tweets:
- Tweet 1 (hook): under 280 chars, must use one of 7 formulas
- Tweets 2-6 (value): 180-220 chars each, sub-hook at top of each
- Tweet 7 (close): single CTA or final thought, no engagement-bait

Format as: 1/ [tweet 1 text] \n\n 2/ [tweet 2 text] \n\n ... etc

Output the thread only.
```

---

## Example (good — single tweet)

> we spent longer than expected on the FCA bit before writing any product UI
>
> most "escrow platforms" treat regulation as the marketing line at the bottom of the page
>
> we treated it as the thing that had to exist before the product did
>
> boring. also the only thing that matters when something goes wrong

**Why it works:**
- Contrarian hook + curiosity gap
- Specific: "the FCA bit," "the product"
- Lowercase casual register (matches voice)
- No hashtags
- 268 chars
- Ends on punchy line, no closer

---

## Example (good — thread)

> 1/ the boring plumbing that decides whether your £40k survives a dispute
>
> 2/ most escrow platforms skip the regulatory bit. they hold your money, release on milestone. works mostly.
>
> 3/ until something goes wrong. then the "insurance" turns out to be a marketing line. and your money's in a holding account governed by nothing.
>
> 4/ FCA-regulated escrow means client money rules. your funds held in trust, not on a balance sheet. can't lend them out. can't lose them in a bad quarter.
>
> 5/ we spent longer on this than the entire rest of the product combined. you can't demo it. you can't put it in a hero animation. it just sits there, working.
>
> 6/ until you need it. and then it's the only thing that matters.
>
> 7/ we built AllSquared for that moment. allsquared.io

**Why it works:**
- Hook: bold + specific ("£40k survives a dispute")
- Sub-hooks every tweet (curiosity, "until something goes wrong," etc.)
- Specific facts (FCA, client money rules)
- Ends with URL, no engagement-bait
- 7 tweets, length ok

---

## Update protocol

When X algorithm changes, when new hook patterns emerge — update this doc.