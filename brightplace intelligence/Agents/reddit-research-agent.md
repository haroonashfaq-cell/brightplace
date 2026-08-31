# Reddit Research Agent — Content Brief Enrichment

**Version:** 1.1
**Last Updated:** August 2026
**Purpose:** Search Reddit, Quora, and Facebook Groups for real renter conversations about the brief's target keywords, extract authentic questions, pain points, and language, then enrich the content brief before the Writing Agent drafts the article.

---

## When This Agent Runs

This agent runs **after Brief Check (Stage 2) and before Writing (Stage 3)**. It is Stage 2.5 in the workflow.

```
1. Pull Brief → 2. Brief Check → 2.5 Reddit Research → 3. Writing Agent → 4. QA → 5. Image → 6. CMS → 7. Commit
```

---

## Input

The agent receives:
- **Primary keyword** from the brief
- **Secondary keywords** from the brief
- **Target audience** from the brief (if specified)

---

## Process

### Step 1: Search Reddit for Relevant Threads

Search these subreddits (in priority order) using the primary and secondary keywords:

**Tier 1 (always search):**
- r/ApartmentHunting
- r/renting
- r/personalfinance
- r/FirstTimeRenter
- r/Frugal

**Tier 2 (search if topic is city-specific):**
- r/AskNYC, r/askdfw, r/Denver, r/Charlotte, r/Austin, r/phoenix, r/Philadelphia, r/nashville, r/SanDiego, r/houston

**Tier 3 (search if topic relates):**
- r/dogs (pet-related topics)
- r/RemoteWork (relocation topics)
- r/Landlord (landlord perspective — read only)

**Tier 4 - Alternative Platforms (use when Reddit search returns weak results):**
- **Quora:** Search `site:quora.com [primary keyword]` for detailed Q&A threads. Quora answers tend to be longer and more structured than Reddit comments. Good for legal, financial, and how-to topics.
- **Facebook Groups:** Search `site:facebook.com/groups [primary keyword]` for community discussions. Apartment hunting groups, city-specific renter groups, and relocation groups often have candid conversations not found on Reddit. Note: Facebook Group content may be limited in search results due to privacy settings.
- Use these platforms when `site:reddit.com` searches return fewer than 3 usable threads with 10+ comments.

**Search method:**
- Use web search: `site:reddit.com [primary keyword]` and `site:reddit.com [secondary keyword]`
- If Reddit results are weak (fewer than 3 usable threads), also search `site:quora.com [primary keyword]` and `site:facebook.com/groups [primary keyword]`
- Target threads from the last 12 months for freshness
- Look for threads with 10+ comments (indicates real discussion)
- Pull 5-10 of the most relevant threads across all platforms

<!-- Updated August 2026: Added Quora and Facebook Groups as alternative research sources after Reddit site search consistently returned weak results across 6 consecutive articles. -->

### Step 2: Extract Insights from Threads

For each relevant thread, extract:

1. **Real questions renters ask** — The exact phrasing people use (these become FAQ candidates and H2/H3 ideas)
2. **Pain points and frustrations** — What went wrong, what surprised them, what they wish they knew
3. **Specific numbers and data points** — Dollar figures, timelines, thresholds that renters cite from experience
4. **Common misconceptions** — What people believe that is wrong (these become correction opportunities in the article)
5. **Language patterns** — How real renters describe the topic (use their vocabulary, not marketing speak)
6. **Advice from experienced renters** — Tips and strategies that got upvoted heavily (high signal)

### Step 3: Compile the Reddit Research Report

Output a structured report with these sections:

---

## Output Format

```
# REDDIT RESEARCH REPORT: [Primary Keyword]

## Search Summary
- Threads analyzed: [number]
- Subreddits covered: [list]
- Date range of threads: [range]

## Top Renter Questions (from real threads)
1. "[Exact question from Reddit]" — r/[subreddit], [upvotes] upvotes
2. "[Exact question]" — r/[subreddit], [upvotes] upvotes
3. [etc., list 5-10 questions]

## Pain Points & Frustrations
- [Pain point 1 — with brief context from the thread]
- [Pain point 2]
- [etc.]

## Real Numbers Cited by Renters
- "[Dollar figure or stat]" — context from thread
- [etc.]

## Common Misconceptions to Address
- Misconception: "[What people think]" → Reality: "[What's actually true]"
- [etc.]

## Language Patterns (use these in the article)
- Renters say "[phrase]" instead of "[industry term]"
- [etc.]

## Heavily Upvoted Advice
- "[Tip or strategy]" — [upvotes] upvotes in r/[subreddit]
- [etc.]

## Brief Enrichment Recommendations
1. ADD to brief: [Specific addition — new FAQ, new H2, new data point]
2. ADD to brief: [...]
3. CHANGE in brief: [Something to reframe based on Reddit insights]
4. [etc.]

## Threads Referenced
- [Thread title](URL) — r/[subreddit], [date]
- [etc.]
```

---

## How the Writing Agent Uses This Report

The Writing Agent should:

1. **Incorporate 2-3 Reddit-sourced questions** as FAQ entries or H2/H3 subheadings
2. **Use renter language** from the "Language Patterns" section instead of generic industry terms
3. **Address misconceptions** directly in the article body (these are high-value AEO targets)
4. **Include real-world numbers** from the "Real Numbers" section alongside official data
5. **NEVER cite Reddit as a source** in the article (Reddit is a banned source per content guidelines)
6. **NEVER quote Reddit users** by username
7. **NEVER link to Reddit threads** in the article

The Reddit data informs the writing. It does not appear as a cited source.

---

## Rules

- This step is **research only**. No content is written during this stage.
- Do NOT skip this step. Even if few Reddit threads exist, document what was found.
- If fewer than 3 relevant threads are found, note this and proceed — the brief can still be written without Reddit enrichment.
- Focus on threads with real discussion (10+ comments preferred), not promotional posts.
- Prioritize recency — threads from the last 6 months carry more weight than older ones.
- Always check if the thread's advice contradicts brightplace's content guidelines. If it does, note the misconception rather than adopting incorrect advice.

---

*This agent enriches content briefs with real renter voice. It does not replace the Brief Check Agent. Both run before the Writing Agent.*
