# SEO Product Vision

**Project:** End-to-End SEO Content Production Platform
**Status:** Planning
**Created:** August 2026

---

## The Problem

Every SEO team stitches together 4-6 tools with manual work in between. No single product owns the full pipeline from keyword research to published, ranked content.

| What Exists | What's Missing |
|---|---|
| Semrush/Ahrefs = keyword research + site audit | No connection to content production |
| Surfer/Clearscope = content optimization scoring | No AI writing, no brief creation, no research |
| Jasper/Copy.ai = AI writing | No SERP analysis, no competitive research, no QA |
| Frase = SERP analysis + briefs | No Reddit research, no AEO analysis, no QA agent |
| MarketMuse = content strategy | No writing, no publishing, no image generation |

---

## The Product

An agent-based platform that takes a user from "I need content that ranks" to "published article with featured image" in one connected flow.

### Core Pipeline

```
Site Audit → Keyword Gap → Long-tail Discovery → Research Engine → Content Brief → Writing Agent → QA Agent → Image Generation → CMS Publish
```

### 3 Features Nobody Has

1. **AI Mode Analysis** — analyzing what ChatGPT/Claude/Google AI Overview says for your keyword and finding citation gaps
2. **Reddit Research Agent** — automated forum research that feeds real renter/user language into writing
3. **Business Context Memory** — every agent knows your brand, voice, existing content, and rules

---

## User Journey

### Step 0: Onboard Your Business

User signs up. First screen:
- Enter website URL
- System auto-detects niche, crawls existing content
- Extracts brand voice from published pages
- Finds current indexed pages and their keywords
- Detects technical SEO issues (audit baseline)
- Stores as "Business Context" that every agent uses

### Step 1: Site Audit Dashboard

Dashboard showing:
- Site Health Score (0-100)
- Technical issues count
- Pages with thin content
- Schema coverage (FAQ, Article, HowTo)
- AI-specific checks (llms.txt, AI crawler access, Bing indexation)
- Watermark risk assessment on existing content

### Step 2: Competitor Intelligence

System auto-detects or user adds competitor URLs:
- Shows top 5 competitors with DR and page counts
- "Find Gaps" button reveals keywords they rank for that you don't
- Filters by KD, volume, intent
- Each keyword has [Select] and [Find Long-tail] buttons
- Suggested titles auto-generated for each keyword
- Long-tail finder shows related keywords with volume/KD

### Step 3: Research Engine (triggered per keyword)

5 research agents run in parallel:
1. **SERP Analysis** — top 10 results, DA, content format, word count, content gaps
2. **AI Mode Analysis** — what ChatGPT/Claude/AI Overview says, who they cite, citation gaps
3. **Featured Snippet Analysis** — current holder, format, recommended structure
4. **PAA Questions** — all People Also Ask questions extracted
5. **Reddit Research** — real user discussions, pain points, specific numbers, language patterns

Output: Structured research report (MD file)

### Step 4: Content Brief Generator

Brief agent takes research + business context and generates:
- 3 title options with character counts
- H2 structure (question-format matching PAA)
- Entity density targets
- Content gaps to fill (unique angles)
- FAQ questions (10+, from PAA + AI gaps)
- Internal link recommendations
- CTA placements
- DO/DON'T rules
- Word count target
- Schema requirements

User can edit the brief or approve it as-is.

### Step 5: Writing Agent

Takes approved brief + business context + Reddit research:
- Writes full article following all rules
- Applies ranking optimizations (question H2s, entity density, snippet paragraphs)
- Live preview with SEO score sidebar
- User can click any section to regenerate or edit manually (creates human-AI hybrid content)

### Step 6: QA Agent

Runs automatically after writing:
- Brand compliance checks (customizable rules per project)
- SEO structure validation (keyword density, headings, date stamps)
- Link audit (checks all URLs for 404s)
- Math verification
- Watermark risk assessment
- Pass/fail report with auto-fix option for simple issues

### Step 7: Image Generation

Generates 3 featured image options:
- Based on article topic and content
- Correct dimensions (1200x628 default, customizable)
- Auto-generated alt text with primary keyword
- Auto-generated file name
- Download or direct CMS upload

### Step 8: CMS Publish

Push to connected CMS as draft or published:
- WordPress, Webflow, Shopify, Ghost, HubSpot, Wix
- Maps fields automatically (title, body, meta, image, categories)
- Handles image upload separately
- Draft vs Published toggle

---

## Competitive Differentiation

| Feature | Semrush | Surfer | Jasper | Frase | Our Product |
|---|---|---|---|---|---|
| Site audit | Yes | No | No | No | Yes + AI-specific checks |
| Keyword research | Yes | No | No | Yes | Yes + competitor gap |
| SERP analysis | Yes | Yes | No | Yes | Yes |
| AI Mode analysis | No | No | No | No | Yes |
| Reddit research | No | No | No | No | Yes |
| Content brief | No | Partial | No | Yes | Yes (with business context) |
| AI writing | No | No | Yes | Partial | Yes (brief-driven) |
| Custom QA rules | No | No | No | No | Yes |
| Watermark risk check | No | No | No | No | Yes |
| Image generation | No | No | Yes | No | Yes |
| Business context memory | No | No | No | No | Yes |
| CMS publishing | No | No | No | No | Yes (multi-platform) |
