# brightplace Content Production Workflow

**Version:** 1.0
**Last Updated:** July 2026
**Purpose:** This document defines the exact steps Claude Code follows when producing content for brightplace. Follow every step in order. Do not skip steps. Do not improvise the process.

---

## Overview

The workflow has 8 stages. Every article passes through all 8 before it is considered complete.

```
1. Pull Brief → 2. Brief Check → 2.5 Reddit Research → 3. Writing Agent → 4. QA Agent → 5. Image Prompt → 6. Webflow CMS Push → 7. GitHub Commit
```

---

## Stage 1: Pull the Content Brief

**Trigger:** User says "I pushed a new brief" or "pull the briefs"

**Action:**
```bash
git pull origin main
```

**Check:** Confirm new files appeared in `brightplace intelligence/Content Brief/`

**Output:** Read the brief file completely before proceeding.

---

## Stage 2: Brief Check Agent

**Purpose:** Validate the brief's strategic quality before writing. Catch keyword gaps, missing entities, weak AEO structure, and link issues BEFORE they become article problems.

**Agent file:** `brightplace intelligence/Agents/brief-check-agent.md`

**What to check (6 sections):**

1. **Keyword Coverage** — Is the primary keyword right? Are secondary keywords missing? Are entities complete?
2. **AEO/GEO Validation** — Will this article get cited by AI engines? Are sections self-contained? Are definitions extractable? Are proof points specific enough?
3. **SERP Intent Match** — Does the format match what's ranking? Are PAA questions covered? Are content gaps genuine?
4. **Brand & Compliance** — Title framing correct? CTAs use `app.brightplace.ai` for search actions? Internal link targets identified?
5. **Competitive Depth** — Enough competitor analysis? Clear differentiation strategy?
6. **Independent Research** — Additional keywords to add? Topical authority fit?

**Output format:**
```
# BRIEF CHECK REPORT: [Keyword]
Brief Status: APPROVED / NEEDS REVISION
[Summary of checks, improvements, additional keywords, missing links]
Verdict: [Proceed or revise]
```

**Decision rule:**
- If APPROVED → proceed to Stage 2.5
- If NEEDS REVISION → make improvements yourself during drafting (don't send back to user unless critical issues exist)
- If REJECTED → tell the user the brief needs rework and explain why

---

## Stage 2.5: Reddit Research Agent

**Purpose:** Search Reddit for real renter conversations about the brief's target keywords. Extract authentic questions, pain points, specific numbers, and language patterns. Enrich the brief so the Writing Agent produces content that matches how renters actually talk and think.

**Agent file:** `brightplace intelligence/Agents/reddit-research-agent.md`

**Process:**
1. Take the primary and secondary keywords from the brief
2. Search Reddit (r/ApartmentHunting, r/renting, r/personalfinance, r/FirstTimeRenter, r/Frugal + city-specific subs if relevant)
3. Analyze 5-10 threads with real discussion (10+ comments preferred)
4. Extract: real questions, pain points, specific numbers, misconceptions, language patterns, heavily upvoted advice
5. Compile a Reddit Research Report with enrichment recommendations

**Output:** A structured report with:
- Top renter questions (exact phrasing from threads)
- Pain points and frustrations
- Real numbers cited by renters
- Common misconceptions to address
- Language patterns to use
- Brief enrichment recommendations (new FAQs, new H2s, reframes)

**Rules:**
- Research only — no content is written during this stage
- NEVER cite Reddit as a source in the article (banned source per guidelines)
- NEVER quote Reddit users by username
- NEVER link to Reddit threads in the article
- The Reddit data informs the writing voice and content depth, not sourcing

**Decision rule:**
- Report compiled → proceed to Stage 3 (Writing Agent uses the enriched brief + Reddit report)

---

## Stage 3: Writing Agent

**Purpose:** Draft the complete article following the brief and all content guidelines.

**Reference files:**
- `brightplace intelligence/Agents/content-writing-guidelines.md` — master brand + SEO rules
- `brightplace intelligence/Agents/seo-writing-agent.md` — writing agent prompt with AEO section
- `brightplace intelligence/Agents/renters-corner-guidelines.md` — ONLY for Renter's Corner (interview-based) pieces

**Critical rules during drafting:**

### Content Structure
- H1 title from the brief
- **All H2 headings must be question-format** matching PAA queries (e.g., "What Are the Rent Prices at [Property]?" not "Rent Prices and Unit Types")
- Every H2 opens with its answer in the first sentence (40-60 words)
- **First paragraph after H1 must be 49-55 words**, structured as a standalone featured snippet answer
- Self-contained sections (each works if extracted independently)
- Bold-label bullet points for comparisons (NO markdown tables, NO `<ul><li>` — Webflow strips them)
- **10+ FAQ pairs preferred** (minimum 6-8), each 40-60 words, standalone answers
- **Entity density:** repeat primary entity 8+ times, key landmarks/locations 3-5x each throughout the article

### Ranking Optimization (apply to every article)
- **7+ internal links** per article (aggressive cross-linking builds topical authority)
- **Target correct search intent** — only target keywords where Google shows article/guide content, NOT listings or templates
- **Fill genuine content gaps** — include data, comparisons, and tradeoffs NO competitor covers
- **Question-format H2s** get 3x higher featured snippet capture than label-format

### Links
- `brightplace.ai` for brand mentions
- `app.brightplace.ai` for search-action CTAs (NEVER both in the same line)
- 3 CTAs: after first H2, mid-article, end of article
- Internal links use `https://www.brightplace.ai/resources/[slug]` or `https://www.brightplace.ai/guides/[slug]`
- NEVER use `/knowledgebase/` path (legacy, causes 404s)
- NEVER link to known non-existent URLs:
  - `/resources/studio-apartments`
  - `/resources/pet-friendly-houses-for-rent`
  - `/resources/1-bedroom-apartments-near-me`
  - `/guides/studio-apartments`

### Brand Rules (zero tolerance)
- brightplace ALWAYS lowercase
- NO em dashes (use commas, periods, semicolons, colons, parentheses)
- NO word "signal" (use "indicator", "suggests", "points to", "reflects")
- NO banned phrases (deep dive, navigate, landscape, unlock, leverage, vibrant, bustling, thriving, hidden gem, etc.)
- NO banned sources in body (Zillow, Apartments.com, Reddit, Yelp, Walk Score, etc.)
- Fair Housing: describe neighborhoods by infrastructure only

### Schema
- All schema URLs use `/resources/` path, NOT `/knowledgebase/`
- Breadcrumb position 2 = "Resources" NOT "Knowledgebase"
- Three schemas required: FAQPage, Article, WebPage
- SEO title MUST differ from H1

### Dates
- All figures dated "(as of Q[N] YYYY)"
- Include "Last reviewed: [Month Year]" in article
- Use current quarter, not the brief's quarter if it's outdated

**Output:** Save to `brightplace intelligence/Complete Articles/[slug].md`

---

## Stage 4: QA Agent (FULL — ALL SECTIONS)

**Purpose:** Catch every issue before the article goes to Webflow. This is the gate. Nothing passes without a full QA.

**Agent file:** `brightplace intelligence/Agents/qa-agent.md`

**YOU MUST RUN ALL 6 SECTIONS. DO NOT SKIP ANY.**

### Section 1: Brand Compliance
- brightplace lowercase
- Em dashes (body only, ignore HTML comments)
- Banned word "signal" (literal "cell signal" is OK)
- Banned phrases
- Banned sources
- Title rules
- Fair Housing

### Section 2: SEO Structure (knowledgebase only)
- First sentence contains keyword
- Keyword density 7-12 instances
- Meta description under 155 chars
- SEO title under 60 chars and DIFFERENT from H1
- Heading hierarchy (one H1, H2s, H3s)
- H2 opening rule (answer first)
- No markdown tables
- Date stamps on all figures
- FAQ section (6-8 pairs, 40-60 words each)
- All 3 schemas present with correct URLs

### Section 3: Renter's Corner Structure (Renter's Corner only)
- Source material used
- Cohort in title
- Katie voice throughout
- Section word counts within targets
- Quoted source phrases

### Section 4: Math Verification
- Verify EVERY calculation independently
- Show the math

### Section 5: Link Audit (CRITICAL — DO NOT SKIP)
- **Internal links:** List every brightplace.ai link. Verify against sitemap. REJECT any `/knowledgebase/` path. REJECT known non-existent URLs.
- **External links:** List every non-brightplace link. REJECT banned sources. REJECT known broken URLs from the QA agent's broken URL list. Flag any .gov/.edu link not on the approved list for manual verification.
- **CTA links:** Count and verify app.brightplace.ai usage.

### Section 6: Infrastructure Checks (CRITICAL — DO NOT SKIP)
- No `http://` links (all must be `https://`)
- No legacy `/knowledgebase/` paths anywhere (body, schema, frontmatter)
- Frontmatter consistency (slug, dates, schema_types)
- External link freshness (check against approved list)

**Output format:**
```
# QA REPORT: [Article Title]
Content Type: knowledgebase / renters-corner
All checks: [X passed, Y failed]
[Full results table]
[Any fixes made]
```

**Decision rule:**
- All pass → proceed to Stage 5
- Any FAIL → fix immediately, re-run the failed check, confirm PASS, then proceed

---

## Stage 5: Image Prompt

**Purpose:** Generate a featured image prompt for the article.

**Reference file:** `brightplace intelligence/Agents/blog-image-prompts.md`

**Rules:**
- 1200 x 628 pixels, 16:9 aspect ratio
- WebP format, under 200KB
- No people visible (Fair Housing)
- No text, logos, or watermarks
- Warm editorial photography style
- 3 prompt options (A recommended, B and C alternatives)
- Include alt text and file name

**Output:** Provide 3 prompt options with alt text and filename.

---

## Stage 6: Webflow CMS Push

**Purpose:** Create or update the article as a draft in Webflow CMS.

**Collection:** Resources (`69fcfcef26d35b66ba874f9d`)

**Process:**
1. Convert markdown to HTML using Python markdown module
2. Save HTML to `Webflow CMS Data/[slug].html`
3. Save CMS JSON to `Webflow CMS Data/[slug].json`
4. Push to Webflow CMS via MCP as draft (isDraft: true)
5. If post-body doesn't go through on create, update the item with full HTML in a second call

**CMS Field Mapping:**
| Field | Source |
|---|---|
| name | Article title (H1) |
| slug | URL slug from frontmatter |
| seo-title | SEO title (must differ from H1, under 60 chars, ends with "\| brightplace") |
| meta-description | Under 155 chars, contains primary keyword |
| focus-keyword | Primary keyword from brief |
| post-summary | First paragraph, plain text, under 300 chars |
| post-body | Full HTML body (exclude frontmatter and schema blocks) |

**If Webflow MCP is unavailable:**
- Save the HTML and JSON files locally
- Tell the user the CMS files are ready for manual upload
- Do NOT block the workflow

---

## Stage 7: GitHub Commit

**Purpose:** Version control all content files.

**Only commit when the user explicitly asks.**

**What to commit:**
- `Complete Articles/[slug].md`
- `Webflow CMS Data/[slug].html`
- `Webflow CMS Data/[slug].json`

**Commit message format:**
```
Add [article title] knowledgebase article

- [word count] words, QA passed all checks
- [number] content gaps filled: [list them]
- [number] FAQ pairs, [number] CTAs, all schemas use /resources/ path
- Drafted to Webflow CMS as draft

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

**If GitHub token is expired:** Tell the user to update it. Do not attempt to push with a bad token.

---

## Content Types

| Type | Guide | Author Voice | Lives At |
|---|---|---|---|
| Knowledgebase (Resources) | content-writing-guidelines.md + seo-writing-agent.md | 3rd person, brightplace | /resources/[slug] |
| Renter's Corner | renters-corner-guidelines.md | 1st person, Katie | /resources/[slug] |
| Property Guide | Same as knowledgebase | 3rd person, brightplace | /resources/[slug] |
| Guest Posts | Manual guidelines | 3rd person, editorial | External sites |
| News | LinkedIn announcements as source | 3rd person, brightplace | News CMS collection |

---

## Known Non-Existent URLs (DO NOT LINK TO THESE)

These URLs return 404. Never use them in any article:
- `/resources/studio-apartments`
- `/resources/pet-friendly-houses-for-rent`
- `/resources/1-bedroom-apartments-near-me`
- `/guides/studio-apartments`

---

## Known Broken External URLs (DO NOT LINK TO THESE)

These external URLs return 403 or 404. Use the replacement URL instead:

| Broken URL | Replacement |
|---|---|
| `consumerfinance.gov/consumer-tools/renting/` | `consumerfinance.gov/housing/housing-insecurity/help-for-renters/` |
| `consumer.ftc.gov/articles/renting-home` | `consumerfinance.gov/housing/housing-insecurity/help-for-renters/` |
| `hud.gov/program_offices/comm_planning/affordablehousing/` | `hud.gov/topics/rental_assistance` |
| `sandiego.gov/park-and-recreation/parks/regional/mission-bay` | `sandiego.gov/parks-and-recreation` |
| `ridetransit.org` | `charlottenc.gov/cats/home/` |
| Any `nyc.gov/site/hpd/...` deep link | `nyc.gov/hpd` (deep links return 403 to bots) |
| `hcr.ny.gov/tenant-protection` | `hcr.ny.gov/` |
| `hcr.ny.gov/system/files/documents/2020/11/fact-sheet-07-09-2020.pdf` | `hcr.ny.gov/` |
| `nyc.gov/site/dca/about/about-dca.page` | `nyc.gov/site/dca/` |
| `greenvillerec.com/swamp-rabbit-trail/` | `greenvillerec.com/` |
| `sjcfl.us/Parks/TreatyPark` | `sjcfl.us/Beaches` |
| `redstone.army.mil` | Remove link, keep text (domain dead) |
| `tdhca.texas.gov` | `texas.gov` (domain dead) |
| `texasattorneygeneral.gov/.../renters-rights` | `texas.gov` (domain dead) |
| `trec.texas.gov` | `texas.gov` (domain dead) |
| `scps.k12.fl.us` | `scps.us` (domain moved) |

---

## Approved External URLs (confirmed working July 2026)

- `hud.gov/topics/rental_assistance`
- `hud.gov/program_offices/fair_housing_equal_opp`
- `consumerfinance.gov/housing/housing-insecurity/help-for-renters/`
- `floodsmart.gov`
- `annualcreditreport.com`
- `rentguidelinesboard.cityofnewyork.us/`

Any .gov or .edu link NOT on this list should be flagged as a WARNING for manual verification.

---

## Quick Reference: The 7-Stage Flow

When the user gives you a content brief, run this exact sequence:

1. **Pull** → `git pull origin main`
2. **Brief Check** → Run brief-check-agent.md (keyword gaps, AEO, links)
2.5. **Reddit Research** → Run reddit-research-agent.md (search Reddit for real renter questions, pain points, language)
3. **Write** → Draft article using brief + Reddit research report
4. **QA** → Run FULL qa-agent.md (ALL 6 sections including link audit)
5. **Image** → Generate 3 image prompts with alt text
6. **Webflow** → Convert to HTML, push to CMS as draft
7. **Commit** → Only when user says "push to GitHub"

If any stage fails, fix and re-run that stage before proceeding. Never skip a stage.

---

*This workflow document is the source of truth for how brightplace content is produced. All agents, guidelines, and processes referenced here are stored in the `brightplace intelligence/Agents/` folder.*
