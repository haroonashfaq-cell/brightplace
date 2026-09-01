# SUPER SEO Agents - Universal Production Workflow

**Version:** 1.1
**Created:** September 2026
**Updated:** September 2026
**Purpose:** Universal SEO agent team that works for ANY business. Covers the full SEO lifecycle from research to publishing to optimization.

---

## MANDATORY: Folder Structure for Every Article

Every article produced by this pipeline MUST follow this folder structure. No exceptions. This keeps all research traceable, debuggable, and organized.

### Folder Convention
```
[client-name]-intelligence/[keyword-slug]/
  01-keyword-research.md
  02-community-research.md
  03-content-brief.md
  04-brief-check.md
  05-[keyword-slug]-draft.md
  06-qa-report.md
  07-schema.md                          (if schemas saved separately)
  08-image-prompts.md
  09-[keyword-slug]-final-enriched.md
  [keyword-slug]-featured.webp
  [keyword-slug]-featured.json
```

### Naming Rules
- **`[client-name]-intelligence/`** = top-level folder per client or community (e.g., `foxchase-intelligence/`, `citilakes-intelligence/`)
- **`[keyword-slug]/`** = subfolder per article, named after the target keyword slug (e.g., `fox-chase-apartments/`, `apartments-near-seaworld-orlando/`)
- **File numbering** = sequential by pipeline stage (01-09). Every stage saves its output here.
- **Draft file** = `05-[keyword-slug]-draft.md` (first complete draft)
- **Final file** = `09-[keyword-slug]-final-enriched.md` (QA fixes applied, ready to publish)
- **Image** = `[keyword-slug]-featured.webp` + `.json` metadata
- **Schemas** = included in the final article file. Separate `07-schema.md` only if schemas need standalone delivery.

### Before Starting ANY Article
1. Create the `[client-name]-intelligence/` folder if it doesn't exist
2. Create the `[keyword-slug]/` subfolder
3. Every agent saves output to the correct numbered file in this folder
4. Never save pipeline files outside this structure

### Example
```
AIR operator/Foxchase/foxchase-intelligence/fox-chase-apartments/
  01-keyword-research.md                    <- Stage 2 output
  02-community-research.md                  <- Stage 4 output
  03-content-brief.md                       <- Stage 5 output
  04-brief-check.md                         <- Stage 6 output
  05-fox-chase-apartments-draft.md          <- Stage 7 output
  06-qa-report.md                           <- Stage 8 output
  08-image-prompts.md                       <- Stage 10 output
  09-fox-chase-apartments-final-enriched.md <- Final product
  foxchase-apartments-alexandria-featured.webp  <- Generated image
  foxchase-apartments-alexandria-featured.json  <- Image metadata
```

---

## Overview

This is a 12-stage workflow. Stages can be run individually or as a full pipeline. Every stage produces a deliverable the next stage consumes.

```
RESEARCH PHASE
  1. Business Context Setup
  2. Keyword Research
  3. Competitor Analysis
  4. Community Research (Reddit/Quora/Forums)

PLANNING PHASE
  5. Content Brief Generation
  6. Brief Check & Validation

PRODUCTION PHASE
  7. SEO Writing
  8. QA & Compliance
  9. Schema Markup
  10. Image Prompt

OPTIMIZATION PHASE (run on existing content or sites)
  11. Technical SEO Audit
  12. On-Page SEO Audit
  13. Backlink Analysis
  14. Local SEO Audit
  15. Content Portfolio Audit
```

---

## Stage 1: Business Context Setup

**Trigger:** User provides a business name, URL, or description.

**Agent:** None (inline setup)

**Process:**
1. Ask for or infer: business name, URL, industry, target audience, geographic focus, primary products/services, top 3 competitors
2. Web search the business and its competitors to understand the market
3. Store context in a `project-context.md` file in the working directory

**Output:** `project-context.md` with business profile

**Decision rule:** Context established -> proceed to any stage

---

## Stage 2: Keyword Research

**Agent file:** `SUPER SEO Agents/keyword-research-agent.md`

**Input:** Business context + seed topics from user

**Process:**
1. Use Semrush MCP tools (if available) for keyword metrics, gaps, and opportunities
2. Web search for PAA questions, SERP features, and intent signals
3. Cluster keywords by intent and topic
4. Score and prioritize opportunities

**Output:** Save to `[client]-intelligence/[keyword-slug]/01-keyword-research.md`

---

## Stage 3: Competitor Analysis

**Agent file:** `SUPER SEO Agents/competitor-analysis-agent.md`

**Input:** Business context + competitor URLs

**Process:**
1. Analyze competitor organic footprint (Semrush if available, web search otherwise)
2. Identify content gaps, ranking keywords, backlink profiles
3. Map competitor content architecture
4. Find differentiation opportunities

**Output:** Save to `[client]-intelligence/[keyword-slug]/01-keyword-research.md` (append competitor section) or standalone competitor report in the client folder

---

## Stage 4: Community Research

**Agent file:** `SUPER SEO Agents/community-research-agent.md`

**Input:** Primary keyword + target audience from brief or research

**Process:**
1. Search Reddit, Quora, and niche forums for real conversations
2. Extract questions, pain points, language patterns, misconceptions
3. Identify content angles competitors miss

**Output:** Save to `[client]-intelligence/[keyword-slug]/02-community-research.md`

---

## Stage 5: Content Brief Generation

**Agent file:** `SUPER SEO Agents/content-brief-agent.md`

**Input:** Keyword research + competitor analysis + community research

**Process:**
1. Select target keyword and define intent
2. Build article outline with H2/H3 structure
3. Map internal/external link targets
4. Define schema requirements
5. Set word count, CTA strategy, and differentiation angle

**Output:** Save to `[client]-intelligence/[keyword-slug]/03-content-brief.md`

---

## Stage 6: Brief Check & Validation

**Agent file:** `SUPER SEO Agents/brief-check-agent.md`

**Input:** Content brief

**Process:**
1. Validate keyword targeting and intent alignment
2. Check AEO/GEO readiness
3. Verify competitive differentiation
4. Validate structural completeness

**Output:** Save to `[client]-intelligence/[keyword-slug]/04-brief-check.md`

**Decision rule:**
- APPROVED -> proceed to Stage 7
- NEEDS REVISION -> fix issues, re-check

---

## Stage 7: SEO Writing

**Agent file:** `SUPER SEO Agents/seo-writing-agent.md`

**Input:** Approved brief + community research + business context

**Process:**
1. Draft complete article following brief structure
2. Apply AEO optimization (BLUF, self-contained sections, entity density)
3. Build FAQ section (10+ pairs)
4. Insert internal/external links
5. Apply anti-AI-detection patterns

**Output:** Save to `[client]-intelligence/[keyword-slug]/05-[keyword-slug]-draft.md`

---

## Stage 8: QA & Compliance

**Agent file:** `SUPER SEO Agents/qa-agent.md`

**Input:** Completed article draft + business brand rules (if provided)

**Process:**
1. SEO structure validation
2. Content quality checks
3. Link audit
4. Math verification
5. Schema validation
6. Brand compliance (using client's rules if provided)

**Output:** Save to `[client]-intelligence/[keyword-slug]/06-qa-report.md`

**Decision rule:**
- All pass -> proceed
- Any fail -> fix and re-check

---

## Stage 9: Schema Markup

**Agent file:** `SUPER SEO Agents/schema-agent.md`

**Input:** Completed article

**Process:**
1. Generate appropriate JSON-LD schemas (Article, FAQPage, WebPage, HowTo, Product, LocalBusiness, etc.)
2. Validate schema structure
3. Add breadcrumb and speakable specifications

**Output:** Schemas included in final article. If standalone needed, save to `[client]-intelligence/[keyword-slug]/07-schema.md`

---

## Stage 10: Image Prompt

**Agent file:** `SUPER SEO Agents/image-prompt-agent.md`

**Input:** Article title, keyword, and theme

**Process:**
1. Generate 3 image prompt options matching the article topic
2. Include alt text and file naming convention
3. Follow SEO image best practices

**Output:** Save to `[client]-intelligence/[keyword-slug]/08-image-prompts.md`. Then generate the image using `generate-image.py` and save to `[client]-intelligence/[keyword-slug]/[keyword-slug]-featured.webp`

---

## Stage 11: Final Assembly

**Trigger:** QA passed + image generated

**Process:**
1. Copy the draft to `09-[keyword-slug]-final-enriched.md`
2. Apply any QA fixes
3. Verify all files are present in the keyword folder (01 through 09 + image)
4. Confirm folder checklist:

```
✅ 01-keyword-research.md
✅ 02-community-research.md
✅ 03-content-brief.md
✅ 04-brief-check.md
✅ 05-[keyword-slug]-draft.md
✅ 06-qa-report.md
✅ 08-image-prompts.md
✅ 09-[keyword-slug]-final-enriched.md
✅ [keyword-slug]-featured.webp
✅ [keyword-slug]-featured.json
```

**Output:** Publish-ready article with complete research trail

---

## OPTIMIZATION STAGES (Run independently on any site)

### Stage 11: Technical SEO Audit

**Agent file:** `SUPER SEO Agents/technical-seo-agent.md`

Run on any URL. Covers: crawlability, indexability, Core Web Vitals, mobile rendering, security headers, robots.txt, XML sitemaps, canonicals, redirects.

### Stage 12: On-Page SEO Audit

**Agent file:** `SUPER SEO Agents/on-page-seo-agent.md`

Run on any page. Covers: title tags, meta descriptions, heading hierarchy, keyword placement, content quality, E-E-A-T signals, internal linking, image optimization.

### Stage 13: Backlink Analysis

**Agent file:** `SUPER SEO Agents/backlink-agent.md`

Run on any domain. Covers: backlink profile overview, referring domains, anchor text distribution, toxic link detection, competitor backlink gaps, link building opportunities.

### Stage 14: Local SEO Audit

**Agent file:** `SUPER SEO Agents/local-seo-agent.md`

Run on any local business. Covers: Google Business Profile, NAP consistency, local citations, review analysis, local pack ranking, geo-grid visibility.

### Stage 15: Content Portfolio Audit

**Agent file:** `SUPER SEO Agents/content-audit-agent.md`

Run on a set of articles. Covers: freshness, link health, keyword cannibalization, content gaps, SERP position changes, AI Overview citation status.

---

## How to Use

### Full content pipeline (research to published article):
```
Run the SUPER SEO workflow stages 1-10 for [business/topic]
```

### Keyword research only:
```
Run keyword research agent for [seed keywords] in [industry]
```

### Site audit:
```
Run technical SEO audit on [URL]
```

### Content audit:
```
Run content portfolio audit on [list of URLs or articles]
```

### Single article from keyword:
```
Run stages 2, 4, 5, 6, 7, 8, 9, 10 for keyword "[keyword]" in [industry]
```

---

## Tools Available

These agents leverage whatever tools are available in the environment:

- **Semrush MCP** (if connected) - keyword metrics, competitor data, backlink analysis
- **Base Operations MCP** (if connected) - threat/safety intelligence for location content
- **Web Search** - SERP analysis, PAA extraction, competitor research
- **Web Fetch** - page analysis, content extraction
- **Webflow MCP** (if connected) - CMS publishing
- **Google Drive/Gmail** (if connected) - collaboration

If a premium tool is unavailable, agents fall back to web search and manual analysis.

---

*This workflow is the source of truth for the SUPER SEO agent team. All agent files are in the `SUPER SEO Agents/` folder.*
