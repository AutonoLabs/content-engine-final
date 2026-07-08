# Narrative Styles — Storytelling Library

> Formats the agent rotates through so posts don't all sound the same. Pick 1-2 per post. Boring is the enemy. Each style has a hook formula, a structure, and an example.

---

## Why this doc exists

Anti-AI-feel isn't just about removing AI tells — it's about adding **range**. Same voice profile + same hook patterns = predictable content that trains the audience to skim.

Solution: rotate through narrative styles. Each post picks a different structural format. Same voice, different scaffolding. The reader doesn't notice the architecture but feels the variety.

**Rule per post:** pick ONE primary narrative style + ONE secondary structural device (rhetorical question, callback, contrast frame, etc.).

---

## Style 1 — The Builder's Log

**When to use:** Technical progress posts, behind-the-scenes, product updates.

**Hook formula:** Specific thing you just finished or broke.

**Structure:**
1. Hook: one concrete thing ("I shipped X today" or "X broke in production")
2. Context: what you were trying to do
3. What happened (the actual story, not the marketing version)
4. What you learned / what's next
5. Close with a question or invitation

**Example:**
> "Spent 4 hours today debugging why our payment flow failed silently on UK bank holidays."
>
> Turns out the FCA-regulated escrow entity's API treats bank holidays differently than the standard payments API. We'd assumed they'd sync. They don't.
>
> Now there's a 3-line fix in the queue, but the bigger lesson is: don't trust that two APIs from the same provider behave the same way on edge cases.
>
> Anyone else hit this with FCA-regulated payment providers?

**Voice fit:** Engineers, technical founders, product builders. AllSquared, TreeAI, technical Yapper content.

---

## Style 2 — The Contrarian Frame

**When to use:** When the mainstream take is wrong and you have evidence.

**Hook formula:** "Everyone says X. Here's why they're wrong."

**Structure:**
1. Hook: state the mainstream take (so reader recognizes it)
2. Pivot: "Here's why that's wrong" or "Here's what actually happens"
3. Evidence: data, experience, observation
4. Reframe: the correct take
5. Implication: what this means for the reader

**Example:**
> "Everyone says escrow platforms need to be fast."
>
> No. They need to be right.
>
> Speed is a feature when the underlying logic is solid. Speed is a liability when it's not. A 6-second escrow release that releases to the wrong party because the dispute logic was sloppy isn't fast. It's broken.
>
> We chose slower release flows for AllSquared because we wanted every release to survive a dispute. Speed was the second priority.
>
> Turns out the people who care about speed also care about not losing money. Same audience.

**Voice fit:** Opinionated founders, regulatory/compliance content, market positioning.

---

## Style 3 — The Specific Number

**When to use:** Posts that lead with one concrete statistic or measurement.

**Hook formula:** "[Number] [things] in [time period]" or "[Number]% of [population] [does X]"

**Structure:**
1. Hook: the number
2. Context: where it came from
3. Why it matters
4. What changes if you take it seriously
5. Close

**Example:**
> "8,400."
>
> That's how many lines of contract review code we've shipped to AllSquared in 6 months. About 50 lines per working day.
>
> Most of it is edge cases. Payment fails at milestone 3. Builder disputes the timeline. Client wants a refund after the deposit release. Each one a specific scenario.
>
> The interesting part: 70% of those edge cases came from 5 customer conversations, not from imagining what could go wrong.
>
> Real users break your assumptions in ways you can't predict. Talk to them.

**Voice fit:** Founder content, growth metrics, operational transparency.

---

## Style 4 — The Personal Reckoning

**When to use:** Vulnerability-driven posts. Earns trust fast, but use sparingly.

**Hook formula:** "I almost [did something drastic]" or "I was wrong about X"

**Structure:**
1. Hook: the moment of reckoning
2. What you thought was true
3. What changed your mind
4. What you did next
5. What you'd tell past-you

**Example:**
> "I almost killed AllSquared in month 3."
>
> I'd built it as a generic escrow platform. Freelancers, agencies, e-commerce, anyone. We were going to be the Stripe of escrow.
>
> Then a conversation with a UK builder changed everything. He didn't care about escrow for e-commerce or generic freelancing. He cared about whether the £40k deposit for his kitchen refit would be released on completion.
>
> That's when I realized: stop building for everyone. Build for the person with the specific problem.
>
> We rebuilt around UK project work. Boring, focused, and ten times more useful.

**Voice fit:** Founder stories, post-mortems, lessons learned.

---

## Style 5 — The Observation

**When to use:** Quiet posts that name something everyone has noticed but nobody has said.

**Hook formula:** "Have you noticed [specific pattern]" or "Watch what happens when [specific scenario]"

**Structure:**
1. Hook: the observation
2. Why it's interesting / what it means
3. Evidence or example
4. What it suggests about the broader trend
5. Close

**Example:**
> "Every UK escrow platform markets itself as 'protected.'"
>
> None of them explain what protected actually means.
>
> Try it. Go to any escrow site. Read the trust page. You'll find words like 'secure,' 'protected,' 'safe' — and almost no specific regulatory references. No FCA number. No client money rules. No link to the entity that holds the funds.
>
> The protection they're talking about is marketing copy. The protection that matters is statutory.
>
> Different things. Different commitments. Different prices.

**Voice fit:** Critical takes, market commentary, regulatory clarity.

---

## Style 6 — The Process Reveal

**When to use:** Showing how you do something. Demystifying the work.

**Hook formula:** "Here's exactly how we [do X]" or "The 5 steps we use to [accomplish Y]"

**Structure:**
1. Hook: promise of process visibility
2. Step 1
3. Step 2
4. Step 3
5. ... (3-7 steps)
6. Close with the result or what changed because of it

**Example:**
> "Here's exactly how AllSquared reviews an AI-drafted contract before a client signs it."
>
> 1. Pull the contract into our review queue (auto)
> 2. Run the AI clause checker against our risk library
> 3. Flag any clause that mirrors a previously disputed contract
> 4. Human reviewer reads any flagged clause (always human, not AI)
> 5. If a clause is too unusual, escalate to legal partner
> 6. Sign-off recorded with full audit trail
>
> Takes 90 minutes per contract. Most platforms do it in 8 seconds with no human in the loop.
>
> We chose 90 minutes because the contract is the document that decides what happens if everything goes wrong. We weren't going to let AI decide that alone.

**Voice fit:** Operations content, transparency posts, B2B audiences.

---

## Style 7 — The Counterintuitive Question

**When to use:** Posts that ask a question readers haven't considered.

**Hook formula:** "What if [conventional wisdom] is actually the problem?"

**Structure:**
1. Hook: the question
2. Why most people assume the opposite
3. Evidence for the contrarian answer
4. What changes if you accept it
5. Close

**Example:**
> "What if 'fast escrow release' is actually a feature for platforms, not for users?"
>
> Think about it. The platform that releases funds in 6 seconds looks great in a demo. The client sees their money move. The provider sees their money move. Everyone's happy.
>
> But the dispute mechanism — the thing that actually protects people when something goes wrong — needs time. You can't investigate a dispute in 6 seconds.
>
> So fast release + slow dispute resolution = happy demo, broken safety net.
>
> We picked slow release (24-72 hours) because it gives dispute resolution time to actually work. The demo is less impressive. The product is more honest.

**Voice fit:** Positioning content, contrarian takes, regulatory/market commentary.

---

## Style 8 — The Open Loop

**When to use:** Threads, multi-part posts, anything that creates a story that needs to be resolved.

**Hook formula:** "Here's what happened" (without the resolution)

**Structure:**
1. Hook: the setup (incomplete)
2. Build tension or context
3. New information that complicates the setup
4. Cliff-hanger or "and then"
5. Resolution in the next post OR a clear question

**Example:**
> "Three weeks ago a client asked us to handle a £95k payment."
>
> Standard milestone escrow. Builder deposit + 4 release stages. Should have been routine.
>
> It wasn't.
>
> The client had been scammed on a previous project. The builder had been scammed on a previous project. Both were using AllSquared because they'd each been burned by the other kind of platform.
>
> When we explained the dispute resolution timeline (24-72 hours per milestone), the client almost left. "That's too slow."
>
> Then we showed them what 'too slow' looked like in their previous platform. 6 weeks. And half the money gone to 'dispute resolution fees.'
>
> They stayed. Here's what happened on the first milestone."

**Voice fit:** Storytelling, narrative threads, building trust through specific examples.

---

## Style Rotation Strategy

**Per brand, per week, pick 1-2 styles:**

- AllSquared (regulated B2B): Contrarian Frame, The Observation, The Process Reveal, The Counterintuitive Question
- TreeAI (technical product): The Builder's Log, The Specific Number, The Process Reveal
- Yapper (consumer health): The Personal Reckoning, The Open Loop, The Specific Number
- Personal founder (eli): The Personal Reckoning, The Builder's Log, The Contrarian Frame

**Why rotate:**
- Predictable = skimmable. The reader should never know which style is coming.
- Different styles exercise different parts of the brain. Mix keeps engagement fresh.
- Each style creates different engagement patterns (replies vs shares vs saves). Rotation = multi-dimensional engagement.

**Rule of thumb:** if you've used the same style 2 weeks in a row, switch.

---

## Style Combinations

Some styles combine well as primary + secondary:

- Builder's Log + Open Loop: "Here's what I built. Here's what went wrong."
- Contrarian Frame + Specific Number: "Everyone says X. The data says otherwise."
- Personal Reckoning + Process Reveal: "I almost quit. Here's the system that brought me back."
- Observation + Counterintuitive Question: "Everyone notices this. Nobody asks the question."

**Max 2 styles per post. More than that = confused structure.**