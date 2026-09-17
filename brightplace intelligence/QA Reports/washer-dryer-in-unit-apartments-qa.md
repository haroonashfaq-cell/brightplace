# QA REPORT: Apartments with In-Unit Washer and Dryer: What It Costs, What to Ask, and Where to Find Them by State
**Content Type:** knowledgebase
**Primary Keyword:** washer dryer in unit apartments
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
**Fix:** Added `"mainEntityOfPage": {"@type": "WebPage", "@id": "https://www.brightplace.ai/resources/washer-dryer-in-unit-apartments"}` to the Article schema.

---

## Warnings (review recommended)

### WARNING 1: External operator links not on approved list (Section 6.4)
- `https://www.amli.com/` (AMLI Residential official site)
- `https://www.maac.com/` (MAA Communities official site)
- These are official property management company websites and appropriate per external link rules, but not on the approved .gov/.edu list. Flag for manual verification before publishing.

### WARNING 2: FAQ answer word counts slightly over 60-word target for some answers (Section 2.9)
- FAQ 1 ("What does in-unit washer and dryer mean?"): ~62 words
- FAQ 9 ("How do I ask my landlord..."): ~53 words
- FAQ 12 ("What apartments include..."): ~48 words
- Most FAQs are within the 40-60 word range. Slight overages are acceptable for completeness.

---

## Full Results

### SECTION 1: BRAND COMPLIANCE

| Check | Result | Notes |
|-------|--------|-------|
| 1.1 brightplace Capitalization | PASS | All instances lowercase |
| 1.2 Em Dashes | PASS | No em dashes in body (only frontmatter `---` separators) |
| 1.3 Banned Word "Signal" | PASS | Zero instances |
| 1.4 Banned Phrases | PASS | Zero matches |
| 1.5 Banned Sources | PASS | No ILS, review aggregators, score sites, or forums referenced |
| 1.6 Title Rules | PASS | No "Top X", "Best", "Ultimate Guide", "#1" in H1 |
| 1.7 Fair Housing | PASS | No demographic descriptions, crime stats, or school ratings |

### SECTION 2: SEO STRUCTURE

| Check | Result | Notes |
|-------|--------|-------|
| 2.1 First Sentence | PASS | "Washer dryer in unit apartments include a washing machine and dryer inside the apartment itself" -- contains primary keyword |
| 2.2 First 100 Words | PASS | Contains direct answer, audience identification (renters), data point (93%, $50-$100/mo) |
| 2.3 Keyword Density | PASS | "washer dryer in unit apartments" and close variants appear 10+ times across body. Keyword in H1, first sentence, multiple H2s, meta description |
| 2.4 Meta Description | PASS | 145 characters. Contains primary keyword. No questions or clickbait |
| 2.4a SEO Title | PASS | "In-Unit Washer Dryer Apartments Guide \| brightplace" = 52 chars. Under 60. Differs from H1. Ends with "\| brightplace" |
| 2.5 Heading Hierarchy | PASS | One H1, 7 H2s (all question-format), H3s for FAQ sub-questions. No skipped levels |
| 2.6 H2 Opening Rule | PASS | Each H2 opens with a direct answer sentence |
| 2.7 No Markdown Tables | PASS | Zero markdown tables. Uses bold-label bullet points |
| 2.8 Date Stamps | PASS | All dollar figures stamped "(as of Q3 2026)" |
| 2.9 FAQ Section | PASS | 12 FAQ pairs (exceeds 10+ preferred). Most answers 40-60 words |
| 2.10 Schema Blocks | PASS | FAQPage, Article, and WebPage schemas all present |
| 2.11 Internal Links | PASS | 10 internal links: what-percentage-of-income, your-true-monthly-cost, houston-city-orientation, austin-young-professionals, cheapest-places-to-live-in-california, charlotte-affordable-neighborhoods, camden-copper-square, phoenix-renters-orientation, denver-city-orientation, nashville-corporate-relocation-neighborhoods, move-in-specials-apartments, questions-to-ask-when-touring, apartment-checklist-first-apartment, renters-insurance-with-roommates. All verified in sitemap |
| 2.12 External Links | PASS | 4 external links: amli.com, maac.com, consumerfinance.gov (approved), hud.gov (approved) |
| 2.13 CTA Placements | PASS | 3 CTAs: (1) after first H2 (line 29), (2) mid-article (line 86), (3) end of article (line 163). All informational tone |
| 2.14 Anti-AI Detection | PASS | Varied section lengths, no hedge stacking, minimal transition word repetition, conclusion does not restate intro |
| 2.15 Last Reviewed Footer | PASS | "Last reviewed: September 2026" present at line 165 |

### SECTION 2B: CONTENT QUALITY

| Check | Result | Notes |
|-------|--------|-------|
| 2B.1 AEO Citability | PASS | Sections self-contained, definitions clean, comparison section present with bold-label bullets, opening paragraph works as standalone citation |
| 2B.2 Entity Density | PASS | "washer dryer" / "in-unit laundry": 20+ mentions. Cities mentioned 3-5x each |
| 2B.3 Information Gain | PASS | Unique: 12-month cost comparison across 4 laundry types, time-cost calculation ($15/hr), Philadelphia 20% premium data |
| 2B.4 Readability | PASS | Average sentence length under 25 words, no paragraphs over 4 sentences |

### SECTION 2C: SCHEMA VALIDATION

| Check | Result | Notes |
|-------|--------|-------|
| 2C.1 Required Schemas | PASS | FAQPage, Article, WebPage all present |
| 2C.2 FAQ Schema Match | PASS | All 12 FAQ pairs in schema match article word-for-word |
| 2C.3 Schema URLs | FIXED | Added missing `mainEntityOfPage` to Article schema. All URLs use `/resources/` path. Breadcrumb uses "Resources" at position 2. Dates match frontmatter |

### SECTION 3: RENTER'S CORNER
N/A (knowledgebase content type)

### SECTION 4: MATH VERIFICATION

| Claim | Calculation | Result |
|-------|-------------|--------|
| Manhattan premium $4,984 - $4,406 = $578/mo | $4,984 - $4,406 = $578 | PASS |
| Shared laundry 12-month: $3-$5/load, $144-$480 | $3 x 48 loads = $144; $5 x 96 loads = $480 | PASS |
| Hookups renting 12-month: $30-$50/mo = $360-$600 | $30 x 12 = $360; $50 x 12 = $600 | PASS |
| Hookups buying: $800-$1,200 one-time | One-time cost, no recurring | PASS |
| Laundromat 12-month: $50-$100/mo = $600-$1,200 | $50 x 12 = $600; $100 x 12 = $1,200 | PASS |
| In-unit premium 12-month: $50-$100/mo = $600-$1,200 | $50 x 12 = $600; $100 x 12 = $1,200 | PASS |
| Time savings 24-48 hours/yr | 2-4 hrs/mo x 12 = 24-48 hrs/yr | PASS |
| Time cost at $15/hr: $30-$60/mo | 2-4 hrs x $15 = $30-$60 | PASS |

### SECTION 5: LINK AUDIT

**Internal Links (all verified against sitemap):**
| URL | Status |
|-----|--------|
| /resources/what-percentage-of-income-should-go-to-rent | VALID |
| /guides/your-true-monthly-cost | VALID |
| /guides/houston-city-orientation | VALID |
| /guides/austin-young-professionals | VALID |
| /resources/cheapest-places-to-live-in-california | VALID |
| /guides/charlotte-affordable-neighborhoods | VALID |
| /resources/camden-copper-square-apartments-phoenix-az | VALID |
| /guides/phoenix-renters-orientation | VALID |
| /guides/denver-city-orientation | VALID |
| /guides/nashville-corporate-relocation-neighborhoods | VALID |
| /resources/move-in-specials-apartments | VALID |
| /resources/questions-to-ask-when-touring-an-apartment | VALID |
| /resources/apartment-checklist-first-apartment | VALID |
| /resources/renters-insurance-with-roommates | VALID |

**External Links:**
| URL | Status |
|-----|--------|
| https://www.amli.com/ | WARNING (manual verify) |
| https://www.maac.com/ | WARNING (manual verify) |
| https://www.consumerfinance.gov/housing/housing-insecurity/help-for-renters/ | VALID (approved) |
| https://www.hud.gov/topics/rental_assistance | VALID (approved) |

**CTA Links:**
| Position | URL |
|----------|-----|
| After first H2 (line 29) | app.brightplace.ai |
| Mid-article (line 86) | brightplace.ai |
| End of article (line 163) | app.brightplace.ai |

### SECTION 6: INFRASTRUCTURE CHECKS

| Check | Result | Notes |
|-------|--------|-------|
| 6.1 No HTTP Links | PASS | All links use https:// |
| 6.2 No Legacy Paths | PASS | No /knowledgebase/ references |
| 6.3 Frontmatter Consistency | PASS | Slug matches, dates valid, schema_types includes Article and FAQPage, canonical URL matches |
| 6.4 External Link Freshness | WARNING | amli.com and maac.com not on approved list -- flag for manual verification |
