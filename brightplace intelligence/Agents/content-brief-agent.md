# Content Brief Agent — brightplace

**Role:** Senior content strategist and SERP analyst. Takes a keyword, runs live SERP research via DataForSEO API, analyzes AI engine responses, competitor content, and PAA questions, then outputs a publish-ready content brief for the Writing Agent.

**Version:** 1.0
**Last Updated:** September 2026

**Output file:** `brightplace intelligence/Content Brief/[keyword-slug]-brief.md`

---

## When This Agent Runs

This agent runs at **Stage 0** — before the existing workflow begins. It replaces the manual brief creation process.

```
0. Content Brief Agent (THIS) → 1. Pull Brief → 2. Brief Check → 2.5 Reddit Research → 3. Writing → 4. QA → 5. Image → 6. CMS → 7. Commit
```

**Trigger:** User provides a keyword (e.g., "foxchase apartments alexandria va" or "pet friendly apartments greenville sc")

---

## API Configuration

### DataForSEO API
- **Endpoint:** `https://api.dataforseo.com/v3/serp/google/organic/live/advanced`
- **Auth Header:** `Authorization: Basic YmVuQGJhc2VvcGVyYXRpb25zLmNvbTo5YjFmZTRiNzU0MjA2NDBj`
- **Method:** POST
- **Response includes:** Organic results, PAA questions, featured snippets, AI Overview, related searches, SERP features

### Additional DataForSEO Endpoints (use as needed)
- **People Also Ask:** `https://api.dataforseo.com/v3/serp/google/organic/live/advanced` (included in organic response)
- **Related Keywords:** `https://api.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live`
- **Keyword Suggestions:** `https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live`
- **SERP Competitors:** `https://api.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live`

---

## Process

### Step 1: SERP Data Collection (DataForSEO API)

Run this curl command to pull live SERP data for the keyword:

```bash
curl -X POST "https://api.dataforseo.com/v3/serp/google/organic/live/advanced" \
  -H "Authorization: Basic YmVuQGJhc2VvcGVyYXRpb25zLmNvbTo5YjFmZTRiNzU0MjA2NDBj" \
  -H "Content-Type: application/json" \
  -d '[{
    "location_name": "United States",
    "language_code": "en",
    "keyword": "[PRIMARY KEYWORD]",
    "device": "desktop",
    "depth": 100,
    "parse": true
  }]'
```

**Extract from the response:**

1. **Organic results (top 10):**
   - URL, title, description, position
   - Estimated word count (from snippet length)
   - SERP features each result has (sitelinks, FAQ rich results, etc.)

2. **People Also Ask (PAA):**
   - Every PAA question shown in the SERP
   - These become H2 headings and FAQ entries in the brief

3. **Featured snippet:**
   - Current snippet holder (URL)
   - Snippet format (paragraph, list, table)
   - Snippet content (this is what we need to beat)

4. **AI Overview (if present):**
   - What Google's AI Overview says for this keyword
   - Which sources it cites
   - What data points it includes
   - What it does NOT cover (these are our content gaps)

5. **Related searches:**
   - All related search suggestions shown at bottom of SERP
   - These become secondary keywords

6. **SERP features present:**
   - Local pack, knowledge panel, images, videos, shopping
   - This tells us what content type Google wants

**If the API call fails:** Fall back to web search for the same data. Search the keyword manually and extract the same information from the SERP.

### Step 1b: Run Additional Keyword Variants (DataForSEO)

For property-specific keywords, also run SERP pulls for these variants:
- `[Property Name] reviews`
- `[Property Name] pet policy`
- `[Property Name] amenities`
- `[Property Name] parking`
- `[Property Name] apartments [City]`
- `is [Property Name] pet friendly`

For general keywords, run variants:
- `[keyword] reddit`
- `[keyword] cost`
- `[keyword] vs`
- `how to [keyword]`
- `what is [keyword]`

Extract PAA questions from ALL variant searches. Deduplicate. These build a comprehensive question bank for the brief.

### Step 2: AI Engine Analysis

Search what AI engines are currently answering for this keyword. This tells us what content already gets cited and what gaps exist.

**Run these web searches:**

1. `site:perplexity.ai "[primary keyword]"` — See if Perplexity has indexed answers for this topic
2. Search the primary keyword directly in web search and look for AI Overview results
3. Search `"[primary keyword]" site:reddit.com` — What are real people asking? (for voice/angle, NOT for sourcing)

**For each AI engine response, extract:**
- What sources are being cited
- What data points are included
- What format the response uses (list, paragraph, comparison)
- What the response does NOT cover (content gaps = our opportunity)
- What claims are made without citation (we can become the citation source)

### Step 3: Competitor Content Analysis

For the top 5 organic results from Step 1:

1. **Fetch each URL** and analyze:
   - Total word count
   - H2/H3 heading structure (exact headings used)
   - Key data points included (rent prices, distances, amenity lists)
   - Internal and external linking patterns
   - Schema markup used
   - Content freshness (when was it last updated?)
   - What's missing (thin sections, outdated data, vague claims)

2. **Identify content gaps across all competitors:**
   - Topics NO competitor covers
   - Data points competitors don't include
   - Questions competitors don't answer
   - Comparison data that doesn't exist yet
   - Specificity gaps (competitors say "nearby shopping" but don't name stores)

3. **Determine beatable positions:**
   - Which top 10 results have thin content (under 800 words)?
   - Which have outdated data (over 12 months old)?
   - Which lack structured data/schema?
   - Which have weak internal linking?

### Step 4: Fetch brightplace Sitemap (for internal linking)

```bash
curl -s "https://www.brightplace.ai/sitemap.xml"
```

Identify 7+ internal link targets relevant to this keyword. Map each to a specific section of the brief.

### Step 5: Find External Authority Links

Web search for .gov and .edu sources relevant to the keyword topic:
- City/county housing authority
- State tenant rights pages
- Local transit authority
- Parks and recreation department
- HUD resources
- CFPB renter resources

Verify each URL is live (not on the known broken URL list from WORKFLOW.md). Identify 3-5 confirmed external links.

### Step 6: Build the Content Brief

Compile all data from Steps 1-5 into the output format below.

---

## Output Format

```
# CONTENT BRIEF: [Primary Keyword]
**Generated:** [YYYY-MM-DD]
**Agent:** brightplace Content Brief Agent v1.0
**Status:** Ready for Brief Check (Stage 2)

---

## Brief Metadata
- **Primary keyword:** [exact keyword]
- **Secondary keywords:** [5-10 keywords from SERP variants and related searches]
- **Search intent:** [informational / commercial / transactional]
- **Search volume:** [from DataForSEO if available]
- **Keyword difficulty:** [from DataForSEO if available]
- **Target word count:** [calibrated against top 3 competitors]
- **Content type:** [guide / property article / comparison / how-to]
- **Target URL:** /resources/[slug]

---

## SERP Snapshot (Live Data from DataForSEO)

### Top 5 Organic Results
1. **[Title]** — [URL]
   - Position: [X] | Est. word count: [X] | Last updated: [date if visible]
   - Strengths: [what they cover well]
   - Weaknesses: [what's missing, outdated, or thin]
2. [...]
3. [...]
4. [...]
5. [...]

### Featured Snippet
- **Current holder:** [URL]
- **Format:** [paragraph / list / table]
- **Content:** [what the snippet says]
- **How to beat it:** [specific instruction]

### People Also Ask (PAA Questions)
1. [PAA question 1]
2. [PAA question 2]
3. [PAA question 3]
4. [PAA question 4]
5. [PAA question 5]
6. [... list ALL PAA questions found across all variant searches]

### AI Overview
- **Present:** [Yes / No]
- **Sources cited:** [list URLs Google AI Overview cites]
- **Key claims:** [what the AI Overview says]
- **Gaps in AI Overview:** [what it doesn't cover — these are our targets]

### Related Searches
- [related search 1]
- [related search 2]
- [... list all]

### SERP Features Present
- [ ] Local pack
- [ ] Knowledge panel
- [ ] Featured snippet
- [ ] PAA
- [ ] AI Overview
- [ ] Images
- [ ] Videos
- [ ] Shopping
- [ ] Sitelinks

---

## AI Engine Analysis

### What AI Engines Currently Answer
- **Google AI Overview:** [summary of what it says, sources cited]
- **Key claims without citation:** [claims where we can become the source]
- **Content gaps across AI responses:** [what NO AI engine covers well]

### Citation Opportunity
[1-2 sentences: What specific content would we need to create to get cited by AI engines for this keyword? What data format do AI engines prefer for this topic?]

---

## Title & Meta

- **H1 title:** "[Title containing primary keyword — question format preferred]"
- **SEO title:** "[Shorter variant | brightplace]" (under 60 chars, MUST differ from H1)
- **Meta description:** "[Under 155 chars, contains primary keyword]"
- **Slug:** [keyword-slug]

---

## Article Outline

### H1: [Title]

**Opening paragraph (49-55 words):**
[Instruction: Write a standalone answer to the primary keyword query. Must contain the keyword, one specific data point, and who this article helps. This targets the featured snippet.]

### H2: [Question-format heading from PAA]
**Target:** 120-180 words
**Must cover:** [specific data points, comparison if applicable]
**Key data needed:** [rent prices, distances, costs — with date stamps]

### H2: [Question-format heading from PAA]
**Target:** 120-180 words
**Must cover:** [...]

[... continue for all planned H2 sections ...]

### H2: [Property-specific: Is [Property] Pet Friendly?] (property articles only)
**Target:** 150-200 words
**Must cover:** Pet types, breed restrictions, weight limits, pet deposit, pet fee, monthly pet rent, on-site pet amenities, nearest off-leash park
**Data needed:** All dollar figures with date stamps

### H2: [Property-specific: What Amenities Does [Property] Offer?] (property articles only)
**Target:** 150-200 words
**Must cover:** Community amenities, in-unit amenities, standout features, seasonal notes
**Data needed:** Specific amenity names and details, not bare lists

### H2: [Property-specific: What Is Parking Like at [Property]?] (property articles only)
**Target:** 120-160 words
**Must cover:** Parking types, costs per type, guest parking, EV charging, distance to units
**Data needed:** Dollar figures with date stamps

### H2: [Property-specific: What Is Within Walking Distance of [Property]?] (property articles only)
**Target:** 200-250 words
**Must cover:** Grocery (name + distance), restaurants/coffee (3-5 names), pharmacy, transit stops, commute to downtown/employers
**Data needed:** All distances in miles and walk times in minutes

### H2: Frequently Asked Questions About [Topic]

#### Q1: [PAA question or high-value community question]
[Instruction: 40-60 word standalone answer, direct answer first sentence]

#### Q2: [Question]
[Instruction: 40-60 words]

[... 10+ FAQ pairs, sourced from PAA questions, AI Overview gaps, and common renter questions ...]

---

## Keyword Placement Map
- **H1:** [primary keyword]
- **First sentence:** [primary keyword]
- **Meta description:** [primary keyword]
- **H2 headings with keyword:** [list which H2s contain the keyword or its variants]
- **Target density:** 7-12 instances for [word count target] words
- **Entity repetition:** [property name / city name / neighborhood] x 5-8 times each

---

## Differentiation Strategy
- **Information gain:** [What we cover that NO competitor does — be specific]
- **Unique data:** [Specific numbers, comparisons, or insights competitors lack]
- **Content gaps filled:** [List 3-5 specific gaps with evidence from competitor analysis]
- **Format advantage:** [How our structure is better than what's ranking]
- **Freshness advantage:** [What competitors have that's outdated]

---

## Internal Link Targets (7+ required)
1. **[Anchor text]** -> [https://www.brightplace.ai/resources/slug] (place in: [section name])
2. **[Anchor text]** -> [https://www.brightplace.ai/guides/slug] (place in: [section name])
[... 7+ internal links, ALL verified against sitemap ...]

## External Link Targets (3-5 required)
1. **[Source name]** -> [URL] (type: .gov / .edu / authority) — verified live
2. **[Source name]** -> [URL]
[... 3-5 external links, all verified not on broken URL list ...]

## CTA Strategy
1. **After first H2:** [CTA copy] -> app.brightplace.ai
2. **Mid-article:** [CTA copy] -> brightplace.ai or app.brightplace.ai
3. **End of article:** [CTA copy] -> app.brightplace.ai

---

## Schema Requirements
- Article schema: headline, description, author (brightplace), dates
- FAQPage schema: all FAQ pairs (answers match article word-for-word)
- WebPage schema: breadcrumb (Home > Resources > [Title]), speakable, canonical URL using /resources/ path

---

## Competitor Comparison

**[Competitor 1 URL]:**
- Word count: [X]
- Strengths: [what they do well]
- Weaknesses: [what's missing or outdated]
- Our edge: [specific advantage]

**[Competitor 2 URL]:**
- Word count: [X]
- Strengths: [...]
- Weaknesses: [...]
- Our edge: [...]

[... for top 5 competitors ...]

---

## Property Data Checklist (property articles only)

- [ ] Pet policy data sourced (types, breeds, weight, costs)
- [ ] Amenity list sourced (community + in-unit)
- [ ] Parking data sourced (types, costs, EV)
- [ ] Walkability data sourced (stores, restaurants, transit — with distances)
- [ ] All dollar figures have date stamps
- [ ] Official property website reviewed
- [ ] Google Maps distances verified

---

## Notes for Writing Agent
[Any special instructions, tricky aspects of this keyword, or warnings about competitor content that the writer should know]
```

---

## Rules

1. **Always call DataForSEO API first.** Live SERP data is the foundation. Never build a brief from assumptions.
2. **If the API fails, fall back to web search.** Do not skip SERP analysis. Search the keyword manually and extract the same data.
3. **Every H2 must come from real data.** PAA questions, AI Overview gaps, or competitor analysis. Never invent sections based on what you think renters want.
4. **All internal link URLs must be verified against the live sitemap.** Do not guess URLs. Fetch the sitemap and match.
5. **All external link URLs must be checked against the known broken URL list** in WORKFLOW.md. Do not include any known-broken URLs.
6. **Word count targets must be calibrated against competitors.** Match or exceed the average of the top 3 results.
7. **Property articles MUST include pet, amenity, parking, and walkability sections.** If the keyword targets a specific apartment community, the brief must plan for all 4 mandatory sections from the property template.
8. **Date-stamp requirement.** Flag every data point in the brief that will need a date stamp in the article.
9. **The brief is a contract.** The Writing Agent executes every section. Do not include optional sections. Every section in the outline will be written.
10. **Never recommend targeting keywords where Google shows listings, tools, or maps instead of articles.** If the SERP is dominated by ILS platforms (Apartments.com, Zillow), flag it and suggest an alternative angle.

---

## brightplace-Specific Additions (on top of SUPER SEO Agent base)

These rules apply to ALL brightplace briefs. They come from the content-writing-guidelines.md and WORKFLOW.md:

- **Title rules:** No superlatives, no ranking language, no "Top X," "Best," "Ultimate Guide"
- **URL path:** Always `/resources/[slug]` — NEVER `/knowledgebase/`
- **CTA targets:** `app.brightplace.ai` for search actions, `brightplace.ai` for brand
- **Banned sources:** Never plan links to Apartments.com, Zillow, Trulia, Yelp, Reddit, Walk Score, or any source in the banned list
- **Fair Housing:** Never plan sections that describe neighborhoods by demographics. Infrastructure only.
- **10+ FAQ pairs preferred** (minimum 6-8)
- **brightplace always lowercase** in all title suggestions
- **Schema breadcrumbs:** Home > Resources > [Title] (never "Knowledgebase")
- **Known non-existent URLs:** Never include `/resources/studio-apartments`, `/resources/pet-friendly-houses-for-rent`, `/resources/1-bedroom-apartments-near-me`

---

*This agent generates content briefs using live SERP data. It replaces manual brief creation and feeds directly into the Brief Check Agent (Stage 2) of the brightplace workflow.*
