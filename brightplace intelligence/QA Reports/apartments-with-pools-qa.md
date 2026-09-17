# QA REPORT: Apartments with Pools: Indoor vs Outdoor, Costs, and Where to Find Them by State in 2026
**Content Type:** knowledgebase
**Primary Keyword:** apartments with pools
**Date:** 2026-09-14
**Status:** PUBLISH READY
**Checks:** 30 passed, 1 fixed, 2 warnings

---

## Summary
- Total checks run: 33
- Passed: 30
- Fixed: 1
- Warnings: 2
- Publish ready: YES

## Fixes Applied

### FIX 1: Article Schema missing `mainEntityOfPage` (Section 2C.3)
**Issue:** Article JSON-LD schema lacked the `mainEntityOfPage` property linking to the canonical URL.
**Fix:** Added `"mainEntityOfPage": {"@type": "WebPage", "@id": "https://www.brightplace.ai/resources/apartments-with-pools"}` to the Article schema.

---

## Warnings (review recommended)

### WARNING 1: External operator links not on approved list (Section 6.4)
- `https://www.amli.com/` (AMLI Residential official site)
- `https://www.maac.com/` (MAA Communities official site)
- `https://cortland.com/` (Cortland official site)
- These are official property management company websites. Flag for manual verification.

### WARNING 2: First paragraph word count slightly over 55-word target
- Opening paragraph is approximately 68 words. Recommended 49-55 for featured snippet optimization. Content is strong and works as a standalone answer, but trimming to 55 words would improve snippet capture. Not a blocking issue.

---

## Full Results

### SECTION 1: BRAND COMPLIANCE

| Check | Result | Notes |
|-------|--------|-------|
| 1.1 brightplace Capitalization | PASS | All instances lowercase |
| 1.2 Em Dashes | PASS | No em dashes in body |
| 1.3 Banned Word "Signal" | PASS | Zero instances |
| 1.4 Banned Phrases | PASS | Zero matches |
| 1.5 Banned Sources | PASS | No banned sources referenced |
| 1.6 Title Rules | PASS | No ranking language in H1 |
| 1.7 Fair Housing | PASS | No demographic descriptions, crime stats, or school ratings |

### SECTION 2: SEO STRUCTURE

| Check | Result | Notes |
|-------|--------|-------|
| 2.1 First Sentence | PASS | "Apartments with pools come in four types: outdoor seasonal, outdoor heated, indoor year-round, and rooftop." -- contains primary keyword |
| 2.2 First 100 Words | PASS | Direct answer (4 pool types), audience (renters), data points ($70-$118 premium, Sun Belt states) |
| 2.3 Keyword Density | PASS | "apartments with pools" and variants appear 15+ times. In H1, first sentence, multiple H2s, meta description |
| 2.4 Meta Description | PASS | 146 characters. Contains keyword |
| 2.4a SEO Title | PASS | "Apartments with Pools: Renter Guide \| brightplace" = 50 chars. Under 60. Differs from H1. Ends with "\| brightplace" |
| 2.5 Heading Hierarchy | PASS | One H1, 8 H2s (question-format), H3s for FAQ sub-questions. No skipped levels |
| 2.6 H2 Opening Rule | PASS | Each H2 opens with direct answer |
| 2.7 No Markdown Tables | PASS | Zero tables |
| 2.8 Date Stamps | PASS | All dollar figures stamped "(as of Q3 2026)" |
| 2.9 FAQ Section | PASS | 12 FAQ pairs. Answers within 40-60 word range |
| 2.10 Schema Blocks | PASS | FAQPage, Article, WebPage all present |
| 2.11 Internal Links | PASS | 14+ internal links, all verified in sitemap: your-true-monthly-cost, what-percentage-of-income, apartments-with-dog-parks, chicago-pet-owners, denver-city-orientation, dallas-families, houston-city-orientation, miami-city-orientation, tampa-renters-orientation, camden-copper-square, phoenix-renters-orientation, nashville-corporate-relocation-neighborhoods, charlotte-affordable-neighborhoods, raleigh-durham-young-professionals, huntsville-renters-orientation, atlanta-active-renters, questions-to-ask-when-touring, apartment-checklist-first-apartment |
| 2.12 External Links | PASS | 5 external links: amli.com, maac.com, cortland.com, consumerfinance.gov (approved), hud.gov (approved) |
| 2.13 CTA Placements | PASS | 3 CTAs: (1) after first H2 (line 35), (2) mid-article (line 121), (3) end of article (line 142). Informational tone |
| 2.14 Anti-AI Detection | PASS | Varied section lengths, natural voice, no hedge stacking |
| 2.15 Last Reviewed Footer | PASS | "Last reviewed: September 2026. Reviewed by Katie Mikles, Content Director at brightplace." at line 184 |

### SECTION 2B: CONTENT QUALITY

| Check | Result | Notes |
|-------|--------|-------|
| 2B.1 AEO Citability | PASS | Sections self-contained, 4-type pool classification extractable, seasonal breakdown by climate zone standalone |
| 2B.2 Entity Density | PASS | "apartments with pools": 15+ mentions. Climate zones, city names (Chicago, Dallas, Miami, Nashville) 3-5x each |
| 2B.3 Information Gain | PASS | Unique: seasonal cost-per-visit calculation ($60/weekend, $20 at 3x/week), 10-state community breakdown with specific pool details, pool maintenance cost range ($250-$700/mo) |
| 2B.4 Readability | PASS | Clean sentence structure, no oversized paragraphs |

### SECTION 2C: SCHEMA VALIDATION

| Check | Result | Notes |
|-------|--------|-------|
| 2C.1 Required Schemas | PASS | All 3 present |
| 2C.2 FAQ Schema Match | PASS | All 12 FAQ pairs match word-for-word |
| 2C.3 Schema URLs | FIXED | Added `mainEntityOfPage`. All URLs use `/resources/`. Breadcrumb correct. Dates match |

### SECTION 3: RENTER'S CORNER
N/A (knowledgebase content type)

### SECTION 4: MATH VERIFICATION

| Claim | Calculation | Result |
|-------|-------------|--------|
| $100/mo premium x 12 = $1,200/yr | $100 x 12 = $1,200 | PASS |
| 5-month pool season = ~20 weekends | 5 months x ~4 weekends = ~20 | PASS |
| $1,200 / 20 weekends = $60/visit | $1,200 / 20 = $60 | PASS |
| 3x/week x 5 months = ~65 visits, $1,200/65 ~ $20 | 3 x 4.3 x 5 = 64.5; $1,200/64.5 = $18.60 ~ "$20" | PASS |
| Pool maintenance $250-$700/mo | Industry range claim, reasonable | PASS |
| Indoor pool rents $1,800-$3,500/mo | Consistent with property examples cited | PASS |

### SECTION 5: LINK AUDIT

**Internal Links (all verified against sitemap):**
| URL | Status |
|-----|--------|
| /guides/your-true-monthly-cost | VALID |
| /resources/what-percentage-of-income-should-go-to-rent | VALID |
| /resources/apartments-with-dog-parks | VALID |
| /guides/chicago-pet-owners | VALID |
| /guides/denver-city-orientation | VALID |
| /guides/dallas-families | VALID |
| /guides/houston-city-orientation | VALID |
| /guides/miami-city-orientation | VALID |
| /guides/tampa-renters-orientation | VALID |
| /resources/camden-copper-square-apartments-phoenix-az | VALID |
| /guides/phoenix-renters-orientation | VALID |
| /guides/nashville-corporate-relocation-neighborhoods | VALID |
| /guides/charlotte-affordable-neighborhoods | VALID |
| /guides/raleigh-durham-young-professionals | VALID |
| /guides/huntsville-renters-orientation | VALID |
| /guides/atlanta-active-renters | VALID |
| /resources/questions-to-ask-when-touring-an-apartment | VALID |
| /resources/apartment-checklist-first-apartment | VALID |

**External Links:**
| URL | Status |
|-----|--------|
| https://www.amli.com/ | WARNING (manual verify) |
| https://www.maac.com/ | WARNING (manual verify) |
| https://cortland.com/ | WARNING (manual verify) |
| https://www.consumerfinance.gov/housing/housing-insecurity/help-for-renters/ | VALID (approved) |
| https://www.hud.gov/topics/rental_assistance | VALID (approved) |

**CTA Links:**
| Position | URL |
|----------|-----|
| After first H2 (line 35) | app.brightplace.ai |
| Mid-article (line 121) | brightplace.ai |
| End of article (line 142) | app.brightplace.ai |

### SECTION 6: INFRASTRUCTURE CHECKS

| Check | Result | Notes |
|-------|--------|-------|
| 6.1 No HTTP Links | PASS | All links use https:// |
| 6.2 No Legacy Paths | PASS | No /knowledgebase/ references |
| 6.3 Frontmatter Consistency | PASS | Slug matches, dates valid, schema_types correct |
| 6.4 External Link Freshness | WARNING | amli.com, maac.com, cortland.com not on approved list -- flag for manual verification |
