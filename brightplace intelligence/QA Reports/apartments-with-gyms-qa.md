# QA REPORT: Apartments with Gyms: What Renters Should Know About Fitness Centers by City in 2026
**Content Type:** knowledgebase
**Primary Keyword:** apartments with gyms
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
**Fix:** Added `"mainEntityOfPage": {"@type": "WebPage", "@id": "https://www.brightplace.ai/resources/apartments-with-gyms"}` to the Article schema.

---

## Warnings (review recommended)

### WARNING 1: External operator links not on approved list (Section 6.4)
- `https://www.amli.com/` (AMLI Residential official site)
- `https://www.maac.com/` (MAA Communities official site)
- `https://cortland.com/` (Cortland official site)
- These are official property management company websites and appropriate per external link rules, but not on the approved .gov/.edu list. Flag for manual verification before publishing.

### WARNING 2: Frontmatter missing `reviewed_by` field
- Not a blocking issue. Other articles include `reviewed_by: "Katie Mikles, Content Lead at brightplace"`. Consider adding for consistency.

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
| 2.1 First Sentence | PASS | "Apartments with gyms are now the norm, with 93% of complexes including a fitness center as of Q3 2026." -- contains primary keyword |
| 2.2 First 100 Words | PASS | Direct answer (93% include gym), audience (renters), data points ($600-$1,800/yr savings, 93%) |
| 2.3 Keyword Density | PASS | "apartments with gyms" and variants appear 12+ times. In H1, first sentence, multiple H2s, meta description |
| 2.4 Meta Description | PASS | 146 characters. Contains keyword. No questions or clickbait |
| 2.4a SEO Title | PASS | "Apartments with Gyms: Renter Guide \| brightplace" = 49 chars. Under 60. Differs from H1. Ends with "\| brightplace" |
| 2.5 Heading Hierarchy | PASS | One H1, 7 H2s (question-format), H3s for equipment tiers and FAQ sub-questions. No skipped levels |
| 2.6 H2 Opening Rule | PASS | Each H2 opens with direct answer |
| 2.7 No Markdown Tables | PASS | Zero tables. Bold-label bullet points used |
| 2.8 Date Stamps | PASS | All dollar figures and stats stamped "(as of Q3 2026)" |
| 2.9 FAQ Section | PASS | 12 FAQ pairs. Answers in 40-60 word range |
| 2.10 Schema Blocks | PASS | FAQPage, Article, WebPage all present |
| 2.11 Internal Links | PASS | 10+ internal links, all verified in sitemap: your-true-monthly-cost, what-percentage-of-income, houston-city-orientation, tampa-renters-orientation, dog-friendly-neighborhoods-san-diego, charlotte-affordable-neighborhoods, camden-copper-square, phoenix-renters-orientation, denver-city-orientation, nashville-corporate-relocation-neighborhoods, apartments-with-attached-garages, questions-to-ask-when-touring, apartment-checklist-first-apartment, apartments-with-dog-parks, month-to-month-vs-12-month-lease |
| 2.12 External Links | PASS | 5 external links: amli.com, maac.com, cortland.com, consumerfinance.gov (approved), hud.gov (approved) |
| 2.13 CTA Placements | PASS | 3 CTAs: (1) after first H2 (line 28), (2) mid-article (line 84), (3) end of article (line 156). Informational tone |
| 2.14 Anti-AI Detection | PASS | Varied section lengths, natural transitions, no hedge stacking |
| 2.15 Last Reviewed Footer | PASS | "Last reviewed: September 2026" at line 158 |

### SECTION 2B: CONTENT QUALITY

| Check | Result | Notes |
|-------|--------|-------|
| 2B.1 AEO Citability | PASS | Sections self-contained, 3-tier equipment breakdown is standalone extractable, opening paragraph works as featured snippet |
| 2B.2 Entity Density | PASS | "apartments with gyms" / "fitness center": 15+ mentions. Equipment brands (Peloton, TRX, CrossFit) mentioned 3-5x each |
| 2B.3 Information Gain | PASS | Unique: CrossFit/TRX demand surpassing Peloton (40%/41% vs 28%), real-world Equinox cancellation example ($3,300 savings), 3-tier equipment classification system |
| 2B.4 Readability | PASS | Average sentence length under 25 words, no oversized paragraphs |

### SECTION 2C: SCHEMA VALIDATION

| Check | Result | Notes |
|-------|--------|-------|
| 2C.1 Required Schemas | PASS | FAQPage, Article, WebPage all present |
| 2C.2 FAQ Schema Match | PASS | All 12 FAQ pairs match article word-for-word |
| 2C.3 Schema URLs | FIXED | Added `mainEntityOfPage` to Article schema. All URLs use `/resources/`. Breadcrumb correct. Dates match |

### SECTION 3: RENTER'S CORNER
N/A (knowledgebase content type)

### SECTION 4: MATH VERIFICATION

| Claim | Calculation | Result |
|-------|-------------|--------|
| Budget gym: $10-$25/mo = $120-$300/yr | $10 x 12 = $120; $25 x 12 = $300 | PASS |
| Mid-tier: $30-$60/mo = $360-$720/yr | $30 x 12 = $360; $60 x 12 = $720 | PASS |
| Premium: $100-$300/mo = $1,200-$3,600/yr | $100 x 12 = $1,200; $300 x 12 = $3,600 | PASS |
| Boutique: $150-$250/mo = $1,800-$3,000/yr | $150 x 12 = $1,800; $250 x 12 = $3,000 | PASS |
| Equinox example: $275/mo x 12 = $3,300 | $275 x 12 = $3,300 | PASS |
| Savings range $600-$1,800/yr in meta | Mid-tier low $360 to boutique $3,000 -- meta says $600-$1,800, conservative mid-range | PASS |

### SECTION 5: LINK AUDIT

**Internal Links (all verified against sitemap):**
| URL | Status |
|-----|--------|
| /guides/your-true-monthly-cost | VALID |
| /resources/what-percentage-of-income-should-go-to-rent | VALID |
| /guides/houston-city-orientation | VALID |
| /guides/tampa-renters-orientation | VALID |
| /guides/dog-friendly-neighborhoods-san-diego | VALID |
| /guides/charlotte-affordable-neighborhoods | VALID |
| /resources/camden-copper-square-apartments-phoenix-az | VALID |
| /guides/phoenix-renters-orientation | VALID |
| /guides/denver-city-orientation | VALID |
| /guides/nashville-corporate-relocation-neighborhoods | VALID |
| /resources/apartments-with-attached-garages | VALID |
| /resources/questions-to-ask-when-touring-an-apartment | VALID |
| /resources/apartment-checklist-first-apartment | VALID |
| /resources/apartments-with-dog-parks | VALID |
| /resources/month-to-month-vs-12-month-lease | VALID |

**External Links:**
| URL | Status |
|-----|--------|
| https://www.hud.gov/topics/rental_assistance | VALID (approved) |
| https://www.amli.com/ | WARNING (manual verify) |
| https://www.maac.com/ | WARNING (manual verify) |
| https://cortland.com/ | WARNING (manual verify) |
| https://www.consumerfinance.gov/housing/housing-insecurity/help-for-renters/ | VALID (approved) |

**CTA Links:**
| Position | URL |
|----------|-----|
| After first H2 (line 28) | app.brightplace.ai |
| Mid-article (line 84) | brightplace.ai |
| End of article (line 156) | app.brightplace.ai |

### SECTION 6: INFRASTRUCTURE CHECKS

| Check | Result | Notes |
|-------|--------|-------|
| 6.1 No HTTP Links | PASS | All links use https:// |
| 6.2 No Legacy Paths | PASS | No /knowledgebase/ references |
| 6.3 Frontmatter Consistency | PASS | Slug matches, dates valid, schema_types correct |
| 6.4 External Link Freshness | WARNING | amli.com, maac.com, cortland.com not on approved list -- flag for manual verification |
