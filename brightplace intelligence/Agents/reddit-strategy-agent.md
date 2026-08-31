# Reddit Strategy Agent — brightplace Community Engagement

**Version:** 1.0
**Last Updated:** July 2026
**Purpose:** Monitor relevant Reddit conversations, draft helpful expert answers, and build brightplace's authority in renter communities without violating Reddit's rules.

---

## How This System Works

```
1. Monitor: n8n polls target subreddits every 15-30 minutes
2. Filter: Keywords match against renter-relevant posts
3. Draft: Claude drafts a helpful answer using brightplace expertise
4. Notify: Slack/email sends you the post link + drafted answer
5. Review: You read the draft, adjust if needed
6. Post: You manually paste the answer on Reddit
```

**You always post manually.** The system drafts. You decide. This keeps brightplace compliant with Reddit's rules and ensures every answer feels human.

---

## Target Subreddits

### Tier 1: High Priority (monitor daily)

| Subreddit | Members | Why |
|---|---|---|
| r/ApartmentHunting | ~50K | Direct renter questions about finding apartments. Highest relevance. |
| r/renting | ~30K | General renting advice. Lease questions, landlord issues, cost questions. |
| r/MovingToCity (various) | Varies | City-specific moving questions. r/AskNYC, r/askdfw, r/AskChicago, etc. |
| r/personalfinance | ~18M | Rent affordability, budgeting, renters insurance questions. Huge reach. |
| r/Frugal | ~3M | Cheap apartments, saving on rent, deposit alternatives. |

### Tier 2: City-Specific (monitor 2-3x per week)

| Subreddit | Relevance |
|---|---|
| r/AskNYC | NYC rent, broker fees, rent stabilization — maps to brightplace NYC content |
| r/askdfw | DFW apartments, Legacy corridor, pet-friendly — maps to Dallas guides |
| r/Denver | Denver apartments, neighborhoods — maps to Denver guides |
| r/Charlotte | University City, South End, NoDa — maps to Charlotte guides |
| r/Austin | Austin apartments, relocating — maps to Austin guides |
| r/phoenix | Phoenix apartments, summer heat, pet-friendly — maps to Phoenix guides |
| r/Philadelphia | Manayunk, Center City, University City — maps to Philly guides |
| r/nashville | Nashville apartments, relocation — maps to Nashville guides |
| r/SanDiego | Mission Beach, Pacific Beach — maps to San Diego content |
| r/houston | Houston apartments, 2nd chance, pet-friendly — maps to Houston content |

### Tier 3: Topical (monitor weekly)

| Subreddit | Relevance |
|---|---|
| r/FirstTimeRenter | First apartment questions. High intent, low competition. |
| r/Landlord | Understand landlord perspective. Do NOT promote here. Listen only. |
| r/RealEstate | Rent vs buy discussions. Contribute renter perspective when relevant. |
| r/dogs | Pet-friendly apartment questions come up regularly. |
| r/RemoteWork | "Where should I move" questions from remote workers. |

---

## Keyword Triggers

### Primary Keywords (high relevance, always draft a response)

```
apartment hunting tips
how to find an apartment
apartment tour questions
what to ask leasing agent
rent affordability
how much rent can I afford
renters insurance roommate
pet friendly apartment
pet deposit vs pet rent
short term lease
subletting rules
no credit check apartment
first apartment checklist
moving to [city name]
apartments near [university]
apartment with dog park
attached garage apartment
rent too high
lease break penalty
security deposit return
```

### Secondary Keywords (draft if context matches brightplace content)

```
rent to income ratio
30% rule rent
40x rule NYC
broker fee NYC
rent stabilized apartment
month to month lease
furnished apartment
apartment application fee
apartment scam
how to negotiate rent
utility costs apartment
master metered utilities
apartment tour checklist
what to look for apartment
cost of living [city]
relocating for work
```

### Negative Keywords (DO NOT respond to these)

```
landlord complaint
eviction
legal advice
lawsuit
discrimination report
mold lawsuit
bed bugs
cockroach infestation
harassment
retaliation
```

These are legal, health, or dispute situations where an apartment search platform should not insert itself. Skip these posts entirely.

---

## Response Rules

### The Golden Rule

**Every Reddit answer must be genuinely useful even if the reader never clicks a link.** The answer itself is the value. The brightplace reference is optional context, not the point.

### When to Include a brightplace Link

| Situation | Include Link? | How |
|---|---|---|
| Your answer directly references data from a brightplace article | Yes | "brightplace has a breakdown of [topic] that covers this: [link]" |
| The question is exactly what a brightplace article answers | Yes, at the end | "I wrote about this in more detail here: [link]" or "There's a good walkthrough of this at [link]" |
| Your answer is complete without any link | No | Just answer. Build karma. Links come later. |
| The post has fewer than 5 upvotes | No | Low visibility posts don't warrant link risk. Just help. |
| You've already posted a brightplace link in this subreddit today | No | One link per subreddit per day maximum. |

### When NOT to Respond

- The post is a rant or vent (not asking for advice)
- The post involves active legal disputes
- The post is about a specific property you have no data on
- The post already has 50+ comments (your answer will be buried)
- The post is from a landlord asking how to handle tenants
- The post involves discrimination or harassment claims

### Link Format Rules

- NEVER use shortened URLs
- NEVER use tracking parameters
- Use the full URL: `https://www.brightplace.ai/resources/[slug]`
- For app links: `https://app.brightplace.ai`
- Never link more than once per answer
- Place the link at the END of your answer, after the helpful content

---

## Account Guidelines

### Account Setup

- Use a real account with a real username (not "brightplace_official" or "apartment_expert_bot")
- Complete the profile with a brief bio mentioning renter education (not brightplace by name)
- Build karma before posting any links: spend the first 2 weeks answering questions with zero links
- Subscribe to all target subreddits
- Upvote and engage with other helpful answers (be a real community member)

### Reputation Building Phase (Weeks 1-2)

- Answer 3-5 questions per day with genuinely helpful, link-free answers
- Build comment karma to at least 100 before posting any links
- Engage naturally (reply to comments on your answers, ask follow-up questions)
- Establish a voice: practical, specific, honest about tradeoffs

### Active Phase (Week 3+)

- Answer 2-3 questions per day
- Include a brightplace link in no more than 1 of every 5 answers (20% link rate maximum)
- Vary which articles you link to (don't link to the same article repeatedly)
- Mix brightplace links with other helpful resources (.gov sites, nonprofit housing resources)

### Red Lines (will get the account banned)

- Never post the same answer twice
- Never post links without substantial original content in the answer
- Never argue with users who push back on your advice
- Never mention brightplace by name more than once per answer
- Never use marketing language ("check out", "you should try", "I recommend this platform")
- Never create multiple accounts to upvote your own content

---

## Answer Drafting — Tone and Structure

### Voice

Write like a knowledgeable friend who has helped a lot of people rent apartments. Not like a brand. Not like a customer service rep. Not like a content marketer.

**Good voice patterns:**
- "I've helped a bunch of people through this. Here's what usually works..."
- "The thing most renters miss is..."
- "Honestly, [direct answer]. Here's why..."
- "This depends on [specific variable]. If you're in [situation A], then [advice]. If [situation B], then [different advice]."

**Bad voice patterns (never use):**
- "At brightplace, we believe..."
- "You should check out brightplace for..."
- "Our platform offers..."
- "As a renter education platform..."
- Any sentence that sounds like it came from a marketing department

### Answer Structure

```
1. Direct answer to the question (1-2 sentences)
2. Specific details that make the answer useful (2-4 sentences)
3. Honest tradeoff or caveat (1 sentence)
4. [Optional] Link to relevant resource if genuinely helpful
```

Keep total length to 100-200 words. Reddit rewards concise, specific answers. Walls of text get skipped.

### Specific Numbers Win

Reddit users love specific numbers. Use them whenever possible:

- "Pet deposits typically run $200-$500, and monthly pet rent is $25-$75/pet on top of that"
- "The 40x rule in NYC means a $3,000/month apartment requires $120K/year income"
- "Broker fees in NYC run 12-15% of annual rent. On a $3K/month place, that's $4,320-$5,400 upfront"
- "Start searching 60-90 days before your target move-in date in competitive markets"

---

## Response Templates

### Template 1: "How much rent can I afford?"

```
The standard guideline is spending no more than 30% of your gross monthly income on rent. So if you make $60K/year ($5,000/month gross), your ceiling is about $1,500/month.

But that's just the starting point. Factor in utilities ($80-$150/month in most markets), renters insurance ($15-$30/month), and any parking or pet fees. Your actual housing cost is usually 15-30% higher than the listed rent.

Most landlords use a stricter rule: your annual income needs to be 40x the monthly rent (NYC) or 2.5-3x the monthly rent (most other markets). If you're under the threshold, a co-signer or guarantor can help.
```

### Template 2: "What questions should I ask on an apartment tour?"

```
The five categories most renters forget:

1. **Total cost:** What's included in rent vs. paid separately? (Utilities, parking, pet fees, trash, internet)
2. **Lease terms:** What's the early termination fee? (Usually 1-2 months rent.) What notice do I need to give at renewal?
3. **Maintenance:** How are requests submitted? What's the average response time for non-emergencies?
4. **What to observe yourself:** Check under sinks for moisture, test water pressure, flush toilets, open windows, check cell signal in every room.
5. **Nearby construction:** "Are there any planned construction projects on this block in the next 12 months?" This is the question nobody asks and the one that matters most.
```

### Template 3: "Pet-friendly apartment tips"

```
Three things most pet owners learn too late:

1. "Pet-friendly" means different things at every property. Ask specifically: How many pets? Weight limit? Breed restrictions? The listing and the actual policy are often different.

2. Budget for three separate pet charges: pet deposit ($200-$500, sometimes refundable), one-time pet fee ($150-$400, never refundable), and monthly pet rent ($25-$75/pet). On a 12-month lease with two pets, that's $600-$1,800 in pet costs alone.

3. Private landlords are more flexible on pet count and breed restrictions than property management companies. PMs follow insurance-driven policies they can't waive. Individual owners make their own rules.
```

### Template 4: "Moving to [City], what should I know?"

```
[Adapt to the specific city. Use brightplace's published guides as the source for specific data.]

A few things that aren't obvious until you're here:

- [City-specific rent range for the neighborhood they're asking about]
- [The transit situation: what's realistic, what's car-dependent]
- [The timing: when to search for the best selection]
- [One honest tradeoff about the area]

If you want a neighborhood-by-neighborhood breakdown, [link to brightplace city guide if one exists — only if genuinely relevant].
```

### Template 5: "Renters insurance — do I need it?"

```
Short answer: yes, and it's cheaper than you think.

A standard renters insurance policy costs $15-$30/month and covers your belongings if they're stolen, damaged by fire, or destroyed. It also covers liability if someone gets injured in your apartment.

Your landlord's insurance covers the building, not your stuff. If your laptop, clothes, and furniture got destroyed in a fire tomorrow, you'd be replacing everything out of pocket without a policy.

If you have a roommate: your policy does NOT cover their belongings. Each person needs their own policy. Sharing a policy sounds cheaper but creates problems (shared claims history, shared coverage limits, payout disputes if the relationship sours).
```

### Template 6: "Is it worth paying for a broker in NYC?"

```
A broker fee on a $3,000/month NYC apartment runs $4,320-$5,400 (12-15% of annual rent). Combined with first month, last month, and security deposit, your move-in cost can exceed $15,000.

No-fee apartments exist. The landlord pays the commission instead of you. They're harder to find because the inventory is smaller, but they save you thousands upfront.

The tradeoff: no-fee apartments sometimes have slightly higher monthly rent (the landlord builds the commission cost into the rent). But even then, you usually come out ahead vs. paying a lump-sum broker fee. Always compare total 12-month cost, not just monthly rent.
```

---

## n8n Workflow Specification

### Node 1: Reddit RSS Trigger

```
Type: RSS Feed Trigger
Poll interval: 15 minutes
Feeds (one per subreddit):
  - https://www.reddit.com/r/ApartmentHunting/new.rss
  - https://www.reddit.com/r/renting/new.rss
  - https://www.reddit.com/r/personalfinance/new.rss
  - https://www.reddit.com/r/AskNYC/new.rss
  - https://www.reddit.com/r/askdfw/new.rss
  - https://www.reddit.com/r/Denver/new.rss
  - https://www.reddit.com/r/Charlotte/new.rss
  - https://www.reddit.com/r/Austin/new.rss
  - [Add city subs as needed]
```

### Node 2: Keyword Filter

```
Type: IF node
Condition: Post title or body contains ANY primary keyword
Pass: Continue to Node 3
Fail: Stop (not relevant)

Secondary filter: Post title or body does NOT contain any negative keyword
Pass: Continue to Node 3
Fail: Stop (legal/dispute topic, skip)
```

### Node 3: Relevance Check + Answer Draft (Claude)

```
Type: AI Agent node (Claude)
Prompt:

You are a renter education expert helping people find apartments. A Reddit user posted the following question in r/{{ $json.subreddit }}:

Title: {{ $json.title }}
Body: {{ $json.body }}

Your task:
1. Determine if this question is relevant to apartment search, renting, or housing costs.
2. If relevant, draft a helpful answer (100-200 words) following these rules:
   - Answer the question directly in the first sentence
   - Include at least one specific number or data point
   - Be honest about tradeoffs
   - Write like a knowledgeable friend, not a brand
   - Do NOT mention brightplace by name in the answer body
3. If a brightplace article directly addresses this topic, include the URL at the end with natural framing ("There's a more detailed breakdown here: [URL]"). Only include a link if genuinely relevant.
4. Rate the post's link opportunity: HIGH (perfect match to brightplace content), MEDIUM (related), LOW (answer only, no link needed), SKIP (not relevant enough to answer)

Available brightplace articles for linking:
- How to rent an apartment: https://www.brightplace.ai/guides/how-to-rent-an-apartment
- True monthly cost: https://www.brightplace.ai/guides/your-true-monthly-cost
- Pet-friendly houses: https://www.brightplace.ai/resources/pet-friendly-apartments-greenville-sc
- Renters insurance roommates: https://www.brightplace.ai/resources/renters-insurance-with-roommates
- Short-term lease: https://www.brightplace.ai/resources/short-term-lease-agreement
- Sublet NYC: https://www.brightplace.ai/resources/sublet-apartments-nyc
- Apartment tour questions: https://www.brightplace.ai/resources/questions-to-ask-when-touring-an-apartment
- Apartments with dog parks: https://www.brightplace.ai/resources/apartments-with-dog-parks
- Apartments with garages: https://www.brightplace.ai/resources/apartments-with-attached-garages
- [Add new articles as they publish]

Output format:
RELEVANCE: [HIGH/MEDIUM/LOW/SKIP]
LINK_OPPORTUNITY: [HIGH/MEDIUM/LOW/NONE]
SUGGESTED_LINK: [URL or NONE]
DRAFTED_ANSWER:
[The answer text, ready to copy-paste into Reddit]
```

### Node 4: Notification

```
Type: Slack message (or Email)
Channel: #reddit-opportunities
Message format:

🔔 Reddit Opportunity — {{ $json.relevance }}

**Subreddit:** r/{{ $json.subreddit }}
**Post:** {{ $json.title }}
**Link:** {{ $json.post_url }}
**Link Opportunity:** {{ $json.link_opportunity }}

**Drafted Answer:**
{{ $json.drafted_answer }}

**Suggested brightplace Link:** {{ $json.suggested_link }}

*Review and post manually if the answer is good.*
```

---

## Tracking and Measurement

### Weekly Metrics to Track

| Metric | How to Track |
|---|---|
| Answers posted | Manual count (spreadsheet or Notion) |
| Answers with brightplace links | Count of answers that included a link |
| Upvotes received | Check weekly on posted answers |
| Link clicks | UTM parameters on brightplace links (optional) |
| Referral traffic from Reddit | Google Analytics: reddit.com as referral source |
| Account karma growth | Check weekly |
| Subreddit bans or removed posts | Track any removals to adjust strategy |

### Monthly Review Questions

1. Which subreddits generated the most engagement?
2. Which answer templates got the most upvotes?
3. Which brightplace articles were linked most often?
4. Were any answers removed by moderators? Why?
5. Is the account karma growing steadily?
6. Are any new renter question patterns emerging that need new brightplace content?

---

## Compliance Checklist (Review Before Every Post)

- [ ] The answer is genuinely helpful without any link
- [ ] The answer sounds like a person, not a brand
- [ ] brightplace is mentioned no more than once (if at all)
- [ ] The link is at the end, not the beginning
- [ ] No more than 1 link per answer
- [ ] No more than 1 brightplace link in this subreddit today
- [ ] The post is not about a legal dispute, discrimination, or health hazard
- [ ] The answer includes at least one specific number
- [ ] The answer is under 200 words
- [ ] I have not posted the same answer anywhere else

---

*This strategy document governs all brightplace Reddit activity. The system automates monitoring and drafting. A human reviews and posts every answer. No exceptions.*
