# Threads Caption Prompt

> Platform-specific generation rules for Threads (Meta). Inherits from anti-ai-feel.md, platform-hooks.md, narrative-styles.md.

---

## System context

You're writing a Threads post for **[brand name]**. Voice profile: see `brands/<brand>/voice-profile.md`. Verified facts: `brands/<brand>/verified-facts.md`. Anti-AI rules: `docs/anti-ai-feel.md`.

**Audience (from `docs/audience-demographics.md`):** 25-34 (~30%) + 18-24 (~20-37%), 58-68% male, consumer casual. Most casual of all platforms — like talking to a smart friend.

---

## Threads-specific rules

### Hook (first 0.5-1s)

First line shows ~250 chars on mobile before "...more". Strong hook density here.

**Threads-specific hooks (less polished than LinkedIn):**
- Casual questions ("anyone else...?", "do you guys...")
- Strong opinions stated plainly
- Short observations
- Multi-post threads for storytelling

**Banned:** Hashtags in main post (Threads algo doesn't weight them). External links in main post (pushes reach to comments only).

### Length

**300-500 chars target. 150-500 acceptable.** Threads rewards tight, conversational writing.

### Format

- Casual register, sentence fragments ok
- No hashtags
- Links ok in replies (or comments), not main post
- Multi-post threads work well for storytelling

### Voice

**Most casual of all platforms.** Like talking to a smart friend. Less polished = more reach.

### Narrative style rotation

Pick 1 from `docs/narrative-styles.md`. Recommended for Threads:
- The Personal Reckoning
- The Observation
- The Open Loop
- The Builder's Log (casual version)

If same style used last week, switch.

### Closing rule

End on a genuine thought. No engagement-bait closers. If a question fits naturally, ok.

---

## Verified-facts gate (HARD)

Pull only from `brands/<brand>/verified-facts.md`.

---

## Generation template

```
You are writing a Threads post for [brand].

Voice profile: [paste]
Verified facts available: [paste]

Theme: [one sentence]
Narrative style: [from narrative-styles.md]

Write the post:
- 300-500 chars
- Casual register (most casual of all platforms)
- No hashtags
- No banned openers or closers
- No fabricated stats
- 1 narrative style

Output only the post.
```

---

## Example (good)

> a friend told me about a kitchen refit last year.
>
> builder took £12k deposit. did two weeks of work. disappeared. client wanted money back. platform said "dispute filed, please wait 6-8 weeks."
>
> six weeks later, half the money was returned. the other half — fees, admin, "dispute resolution costs" — gone.
>
> that's what unregulated escrow looks like in practice. not the marketing version.
>
> we built allsquared because the regulated version of this shouldn't be the exception. it should be the default.
>
> FCA-regulated. client money rules. money held in trust, not on a balance sheet.

**Why it works:**
- Casual register (lowercase, fragments)
- Real story (specific numbers from verified context if any)
- Specific details (£12k, 6-8 weeks)
- Ends on strong statement, no engagement-bait
- Length: ~540 chars ✓

---

## Update protocol

When Threads algorithm changes — update this doc.