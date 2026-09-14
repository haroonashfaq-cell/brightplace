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

### Step 1b: Property-Specific Research (for property articles ONLY)

When the brief targets a specific apartment community or property (e.g., "The Avalon apartments Orlando" or "Foxchase apartments Alexandria"), run these additional searches. This step is REQUIRED for all property articles.

**Property-specific search queries (run ALL of these):**
- `site:reddit.com "[Property Name]" review`
- `site:reddit.com "[Property Name]" pets` OR `"[Property Name]" dog` OR `"[Property Name]" cat`
- `site:reddit.com "[Property Name]" parking`
- `site:reddit.com "[Property Name]" amenities`
- `site:reddit.com "living at [Property Name]"` OR `"moved to [Property Name]"`
- `site:reddit.com "[Property Name]" [City Name]`
- `site:google.com/maps "[Property Name]" reviews` (Google Maps reviews surface real resident feedback)

**If property-specific results are thin (fewer than 3 threads), broaden the search:**
- `site:reddit.com "[Management Company Name]" reviews`
- `site:reddit.com apartments [Neighborhood Name] [City] pets`
- `site:reddit.com apartments [Neighborhood Name] [City] parking`
- `site:reddit.com "[City]" apartment amenities worth it`
- `site:reddit.com "[City]" apartment "walking distance"`
- `site:quora.com "[Property Name]"` OR `site:quora.com apartments [City] [Neighborhood]`

**What to look for in property-specific threads:**

1. **Pet policy reality vs. marketing** — Do residents confirm the property is actually pet-friendly? Are there breed or weight restrictions the website doesn't mention? What's the real pet rent and deposit? Are there enough dog waste stations? Is there a dog park on-site or nearby?

2. **Amenity quality and availability** — Which amenities do residents actually use vs. which are just marketing photos? Is the gym well-maintained or outdated? Is the pool overcrowded in summer? Are package lockers reliable? Do in-unit washers/dryers actually work? Is the "business center" just a printer in a closet?

3. **Parking frustrations** — Is there enough parking? What does covered/garage parking actually cost? Do visitors have parking options? Is the lot safe at night? Are EV charging stations available and functional? How far is the walk from the parking area to units?

4. **Walkability and nearby essentials** — What grocery stores, restaurants, pharmacies, coffee shops, and gyms are actually within walking distance? What do residents say about the commute to downtown or major employers? Is there a bus stop or transit station nearby? What do residents wish was closer?

5. **Noise, maintenance, and management** — These are bonus data points that make property articles feel authentic. What do residents say about noise levels, maintenance response times, and management communication?

<!-- Updated August 2026: Added Quora and Facebook Groups as alternative research sources after Reddit site search consistently returned weak results across 6 consecutive articles. -->

### Step 2: Extract Insights from Threads

For each relevant thread, extract ALL 8 categories (plus property-specific categories if applicable):

1. **Real questions renters ask** — The exact phrasing people use (these become FAQ candidates and H2/H3 ideas)
2. **Pain points and frustrations** — What went wrong, what surprised them, what they wish they knew
3. **Specific numbers and data points** — Dollar figures, timelines, thresholds that renters cite from experience
4. **Common misconceptions** — What people believe that is wrong (these become correction opportunities in the article)
5. **Language patterns** — How real renters describe the topic (use their vocabulary, not marketing speak)
6. **Advice from experienced renters** — Tips and strategies that got upvoted heavily (high value)
7. **Emotional triggers** — What makes renters frustrated, excited, anxious, or relieved about this topic? (These reveal the stakes the article must address to feel real)
8. **Unmet needs (unanswered questions)** — Questions that went unanswered or got only weak answers in the threads. These are the highest-value content gaps because no one has answered them well yet.

**Property-specific extraction categories (for property articles ONLY — extract these IN ADDITION to the 8 above):**

9. **Pet policy details** — Confirmed pet types allowed, breed restrictions, weight limits, pet rent amount, pet deposit amount, on-site dog park or pet stations, nearby off-leash parks, resident complaints about pet policies
10. **Amenity reality check** — Which amenities residents praise vs. complain about, amenities that are broken/closed/overcrowded, amenities residents wish existed, seasonal availability (pool months, outdoor grills)
11. **Parking specifics** — Parking types available (surface, covered, garage), monthly costs, availability issues, guest parking, EV charging, distance from parking to units, safety concerns
12. **Walkability and nearby essentials** — Specific stores/restaurants/services residents mention walking to, estimated walk times residents cite, things residents say require a car, transit stops and routes residents use, commute times to major employers or downtown

### Step 3: Identify Content Angles

After extraction, synthesize the raw insights into actionable content angles. This is where research becomes strategy.

1. **Angles no competitor covers** — What real concerns from the threads do top-ranking articles ignore entirely? List 2-3 specific angles with evidence.
2. **Counter-narrative opportunities** — What popular beliefs from the threads are actually wrong? Myth-busting content earns disproportionate AI citations because it provides information gain.
3. **Specificity opportunities** — Where do search results give generic advice but thread users want specifics? (e.g., search results say "budget 30% of income" but renters want exact dollar breakdowns for their city)
4. **Experience-based content opportunities** — What stories, examples, or first-hand accounts from threads could strengthen E-E-A-T if translated into the article's voice?

### Step 4: Compile the Research Report

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

## Emotional Triggers
- **Frustration:** [What makes renters angry or stressed about this topic]
- **Anxiety:** [What they worry about before/during the process]
- **Relief:** [What resolved their concern — this becomes the article's payoff]

## Unmet Needs (Unanswered Questions)
- "[Question that got no good answer]" — [platform]
- "[Question with only weak/generic answers]" — [platform]
[These are the highest-value content gaps. Prioritize covering these in the article.]

## Property-Specific Findings (include ONLY for property articles)

### Pet Policy Intel
- **Allowed:** [Pet types, breed restrictions, weight limits from resident reports]
- **Costs:** [Pet rent $/mo, pet deposit $, pet fee $ — from resident reports]
- **On-site:** [Dog park, pet stations, pet wash — confirmed or denied by residents]
- **Nearby:** [Off-leash parks, vet clinics, pet stores residents mention]
- **Complaints:** [Common pet-related frustrations from residents]

### Amenity Reality Check
- **Praised:** [Amenities residents consistently like — with quotes/context]
- **Complained about:** [Amenities that are broken, outdated, overcrowded, or misleading]
- **Missing:** [Amenities residents wish the property had]
- **Seasonal notes:** [Pool hours, outdoor amenity availability, etc.]

### Parking Intel
- **Types available:** [Surface/covered/garage — confirmed by residents]
- **Costs:** [Monthly parking fees from resident reports]
- **Issues:** [Availability problems, safety concerns, guest parking limitations]
- **EV charging:** [Available/not available, functional/broken — from resident reports]

### Walkability and Nearby Essentials
- **Grocery:** [Store names + estimated walk times from residents]
- **Restaurants/Coffee:** [Names residents mention, walking distance]
- **Pharmacy/Medical:** [Nearby options residents cite]
- **Transit:** [Bus stops, train stations, routes — from resident reports]
- **Commute:** [Drive/transit times to downtown or major employers residents report]
- **Requires a car:** [Things residents say you need a car for]

## Content Angles Identified
1. **Competitor blind spot:** [Angle no top-ranking result covers + evidence from threads]
2. **Counter-narrative:** [Popular belief that is wrong + what's actually true]
3. **Specificity gap:** [Where search results are generic but users want exact numbers/details]
4. **Experience opportunity:** [First-hand account that could strengthen E-E-A-T]

## Brief Enrichment Recommendations
Use these exact action tags:

1. ADD: [New FAQ pair, new H2 section, or new data point to include]
2. ADD: [...]
3. REFRAME: [Adjust an existing section's angle based on what the audience actually cares about]
4. ADDRESS: [Specific misconception to correct in the article body]
5. USE LANGUAGE: [Specific renter phrases to use instead of industry jargon]
6. [etc.]

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
