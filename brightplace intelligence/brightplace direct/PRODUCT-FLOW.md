# brightplace direct — Content Engine Flow

## Prerequisites (Done by Developer Team, NOT Us)
- Operator site is live at [operator].brightplace.ai
- Property pages are built with data (floor plans, amenities, pricing)
- Site has proper SEO infrastructure (schemas, sitemap, robots.txt)

## What We Need From Developer Team Before Starting Content
- Operator brand guidelines (_brand.json): voice, tone, preferred language
- Business context (_context.json): company description, mission, markets
- List of all property pages with URLs (so we can internal-link to them)
- Property data access (names, addresses, amenities, prices) for content accuracy

---

## Phase 1: Keyword Research (Keyword Agent)

**Trigger:** Operator site is live, we have their brand context and property data.

**Process:**
1. Keyword Agent analyzes operator's properties, markets, and competitors
2. Generates keyword suggestions in 4 tiers:

| Tier | Type | Example | Why |
|---|---|---|---|
| Quick Wins | Branded, zero competition | "[Property name] reviews" | No editorial content exists |
| Long Tail | Location + modifier | "pet-friendly apartments [city]" | Moderate volume, low KD |
| Informational | How-to, what-is | "what does rent include" | Builds topical authority |
| Gap Keywords | Competitor not ranking | "[Competitor] vs [Property]" | Steal traffic |

3. Each keyword includes: volume, KD, intent, article angle, reasoning

**Output:** Keyword report presented to operator for approval.

---

## Phase 2: Operator Keyword Approval

**Trigger:** Keyword report delivered.

**Process:**
1. Operator reviews keyword suggestions
2. Selects which keywords they want articles written for
3. Approved keywords enter the writing pipeline

**No brief writing needed from the operator.** They just pick keywords.

---

## Phase 3: Auto-Brief Generation (Brief Agent)

**Trigger:** Keyword approved by operator.

**Process:**
1. Brief Agent takes the approved keyword
2. Auto-generates complete brief:
   - H1 title + SEO title (under 60 chars)
   - H2 structure in question format (matching PAA)
   - Content gaps to fill (what competitors miss)
   - Internal linking targets (which property pages to link)
   - Entity density targets
   - 8-12 FAQ suggestions
   - Target word count

**Key difference from brightplace intelligence:** No manual brief writing. Brief is fully automated from keyword data.

---

## Phase 4: Article Writing (Writing Agent)

**Trigger:** Brief generated.

**Inputs the Writing Agent uses:**
- Content brief (from Phase 3)
- Operator brand guidelines (voice, tone, terminology)
- Business context (company description, USPs)
- Property data (accurate prices, amenities, addresses)

**What it writes:**
- 1,500-2,500 word article following SEO/AEO rules
- 49-55 word featured snippet paragraph
- Question-format H2s with BLUF answers
- 10+ FAQ pairs
- 7+ internal links to operator property pages
- 3 CTAs linking to operator pages
- Date-stamped dollar figures
- Entity density per brief targets

**Brand adaptation:**
- Uses operator's voice/tone (not brightplace voice)
- CTAs link to operator's property pages (not brightplace.ai)
- Author credited as operator (not brightplace)

---

## Phase 5: Quality Assurance (QA Agent)

**Trigger:** Article written.

**6-section validation:**
1. Brand Compliance (operator name casing, em-dashes, banned phrases, Fair Housing)
2. SEO Structure (keyword density, meta tags, headings, FAQs, schemas)
3. Content Accuracy (prices, floor plans, addresses match property data)
4. Link Audit (internal links valid, no broken externals, 3 CTAs present)
5. Infrastructure (all HTTPS, frontmatter complete)
6. AI Readiness (self-contained FAQs, entity density, extractable answers)

**All 6 must PASS.** Fix and re-run any failures.

---

## Phase 6: Image Generation (Image Agent)

**Trigger:** QA passes.

**Process:**
- 3 featured image prompt options (1200x628, 16:9, no people, no text)
- Alt text with primary keyword
- Operator or auto-selects option A

---

## Phase 7: Publishing (Publish Agent)

**Trigger:** Image ready.

**Process:**
1. Article formatted for the operator's site (markdown → HTML or data file)
2. JSON-LD schemas generated (Article, FAQPage, BreadcrumbList)
3. Content pushed to the operator's site repo
4. sitemap.xml and llms.txt updated
5. Site auto-rebuilds on Vercel
6. Live URL verified

**Coordination with developer team:** We push content files, their codebase renders them.

---

## Phase 8: Analytics & Reporting

**Ongoing:**
- Track page views, traffic sources, CTA clicks per article
- Monitor Google Search Console for keyword rankings
- Monitor AI citations (ChatGPT, Perplexity, Claude mentions)

**Monthly report to operator:**
```
MONTHLY REPORT: [Operator Name]
Period: [Month Year]

Content Published: [X articles]
Total Traffic: [visits] (+X% from last month)
Top Performing Articles: [list with views]
Top Search Queries: [from Search Console]
CTA Clicks: [tour: X, call: X, email: X]
AI Citations: [X mentions detected]

Next Month Plan:
- [X new keywords identified]
- [X articles scheduled]
- [Content gaps to fill]
```

---

## Plug-and-Play Vision (Future)

The content engine should work with ANY website stack:
- **Current:** Next.js/Vercel (push data files, auto-rebuild)
- **Future:** Webflow (push via CMS API), WordPress (REST API), Contentful/Sanity, custom CMS via webhook

The content engine is platform-agnostic. Keyword research, brief creation, writing, QA, and image generation don't care where the content is published. Only the Publish Agent needs a platform adapter.
