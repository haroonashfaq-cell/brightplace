# Guide Articles Update Progress

**Started:** September 3, 2026
**Goal:** Fix all 30 guides using brightplace agents (5 per day)
**Audit Checklist:** `AUDIT-CHECKLIST.md` in this folder

---

## Completion Status

| # | Article | Priority | Issues | Status | Date |
|---|---|---|---|---|---|
| 1 | dallas-families | P0 | 6 issues, 4 warnings | DONE - PUBLISHED | Sep 3, 2026 |
| 2 | dc-empty-nesters | P0 | 6 issues, 4 warnings | DONE - READY FOR PUBLISH | Sep 14, 2026 |
| 3 | kansas-city-young-professionals | P0 | 6 issues, 4 warnings | PENDING | |
| 4 | minneapolis-city-orientation | P0 | 6 issues, 4 warnings | PENDING | |
| 5 | brooklyn-neighborhood-guide | P0 | 6 issues, 3 warnings | PENDING | |
| 6 | salt-lake-city-renters-orientation | P0 | 6 issues, 3 warnings | PENDING | |
| 7 | chicago-pet-owners | P0 | 5 issues, 5 warnings | PENDING | |
| 8 | austin-young-professionals | P0 | 5 issues, 4 warnings | PENDING | |
| 9 | denver-city-orientation | P0 | 5 issues, 4 warnings | PENDING | |
| 10 | houston-city-orientation | P0 | 5 issues, 4 warnings | PENDING | |
| 11 | miami-city-orientation | P0 | 5 issues, 4 warnings | PENDING | |
| 12 | philadelphia-city-orientation | P0 | 5 issues, 4 warnings | PENDING | |
| 13 | phoenix-renters-orientation | P1 | 5 issues, 4 warnings | PENDING | |
| 14 | dog-friendly-san-diego | P1 | 5 issues, 3 warnings | PENDING | |
| 15 | fort-collins-outdoor-renters | P1 | 5 issues, 3 warnings | PENDING | |
| 16 | greensboro-renters-orientation | P1 | 5 issues, 3 warnings | PENDING | |
| 17 | how-to-rent-an-apartment | P1 | 5 issues, 3 warnings | PENDING | |
| 18 | relocating-to-austin | P1 | 5 issues, 3 warnings | PENDING | |
| 19 | uf-gainesville-student-housing | P1 | 5 issues, 3 warnings | PENDING | |
| 20 | your-true-monthly-cost | P1 | 4 issues, 7 warnings | PENDING | |
| 21 | lexington-student-neighborhoods-uk | P1 | 4 issues, 4 warnings | PENDING | |
| 22 | columbia-usc-student | P2 | 4 issues, 3 warnings | PENDING | |
| 23 | knoxville-young-professionals | P2 | 4 issues, 3 warnings | PENDING | |
| 24 | raleigh-durham-young-professionals | P2 | 4 issues, 3 warnings | PENDING | |
| 25 | ut-austin-student-housing | P2 | 4 issues, 3 warnings | PENDING | |
| 26 | tampa-renters-orientation | P2 | 3 issues, 4 warnings | PENDING | |
| 27 | atlanta-active-renters | P2 | 3 issues, 3 warnings | PENDING | |
| 28 | charlotte-affordable-neighborhoods | P2 | 3 issues, 3 warnings | PENDING | |
| 29 | huntsville-renters-orientation | P2 | 3 issues, 3 warnings | PENDING | |
| 30 | nashville-corporate-relocation | P2 | 3 issues, 3 warnings | PENDING | |

**Completed: 2/30 | Remaining: 28**

---

## Article 1: dallas-families — COMPLETED

### What Was Fixed
- Banned phrases removed ("notably", "landscape")
- 12 FAQ pairs added (was 0)
- 8 internal links (was 6) — added how-to-rent, income-restricted, parkside-at-legacy
- 10 external authority links (was 2) — TX State Law Library, Dallas ISD, Richardson ISD, DART, CFPB, HUD, Dallas County
- 23 date stamps added on all dollar figures (was 0)
- Focus keyword "family friendly apartments dallas" woven in 16x (was 0)
- 3 CTAs to app.brightplace.ai added (was 0)
- All H2s converted to question format (was 0/6 questions)
- Meta description updated with focus keyword (139 chars)
- SEO title updated: "Family Friendly Apartments Dallas TX (2026) | brightplace" (57 chars)
- Last Reviewed updated to September 2026 (was March 2026)
- Rent data verified against Q3 2026 market sources

### New Content Added
- Neighborhood cost comparison section (side-by-side all 4 areas)
- "Real costs beyond rent" section with childcare data ($840/mo infant, $780/mo preschool)
- Worked example: rent + childcare = $2,640-$2,790/mo in Richardson
- DART rail as family budget strategy ($400-600/mo savings)
- Rent vs buy insight (same school access, $1,000+/mo gap)
- Apartment touring checklist for families
- School zoning verification guidance

### Files
- Updated article: `Complete Articles/dallas-families-UPDATED.md`
- Research report: `Complete Articles/dallas-families-RESEARCH.md`
- CMS HTML: `Webflow CMS Data/dallas-families.html`
- CMS JSON: `Webflow CMS Data/dallas-families.json`

### Stats: Before vs After
| Metric | Before | After |
|---|---|---|
| Word count | 1,865 | 3,239 |
| H2 sections | 6 (labels) | 8 (questions) |
| FAQ pairs | 0 | 12 |
| Internal links | 6 | 8 |
| External links | 2 | 10 |
| CTAs | 0 | 3 |
| Date stamps | 0 | 23 |
| Focus keyword | 0x | 16x |

---

## Pipeline Per Article

Each article follows this process:
1. Read current content from CMS pull (`Complete Articles/[slug].md`)
2. Run Community Research Agent (Reddit/Quora/forums)
3. Run SERP analysis (top 5 results, PAA questions, AI Overview)
4. Verify rent data against current market sources
5. Fetch sitemap for internal link targets
6. Rewrite article fixing all audit issues
7. Run QA Agent (all checks must pass)
8. Extract HTML post-body
9. Save to `Webflow CMS Data/[slug].html` + `.json`
10. Push to Webflow CMS (update existing item)
11. Publish

---

## Systemic Issues to Fix in Every Article

These apply to nearly all 30 guides:
1. Add 10+ FAQ section (28/30 articles missing)
2. Add "(as of Q3 2026)" date stamps to all dollar figures (27/30 missing)
3. Add 3 CTAs to app.brightplace.ai (30/30 missing)
4. Weave in focus keyword 7-12x (30/30 at 0 instances)
5. Convert H2s to question format (29/30 using labels)
6. Add/increase internal links to 7+ (12/30 below target)
7. Add external authority links to 3+ (8/30 at zero)
8. Remove banned phrases (11/30 affected)
9. Remove banned sources (10/30 affected)
10. Fix Fair Housing violations (3/30 affected)
11. Fix meta descriptions over 155 chars (6/30 affected)
12. Update "Last Reviewed" to September 2026

---

## Article 2: dc-empty-nesters — COMPLETED

### What Was Fixed
- Banned phrase removed ("navigating" in summary, "unlock" in body)
- 11 FAQ pairs added (was 0)
- 7 internal links (was 0) — added how-to-rent, your-true-monthly-cost, questions-to-ask, what-percentage-of-income, month-to-month-vs-12-month, pet-deposit-vs-pet-fee, fair-housing-act-guidelines
- 5 external authority links (was 0) — Montgomery County gov, Arlington County gov, WMATA, HUD rental assistance, HUD fair housing
- 36 date stamps added on all dollar figures (was 0)
- Focus keyword "empty nester apartments DC suburbs" woven throughout (was 0)
- 3 CTAs to app.brightplace.ai added (was 0)
- All H2s converted to question format (was 0/5 questions)
- Meta description fixed to 125 chars (was 156)
- SEO title confirmed: "Empty Nester Apartments DC Suburbs (2026) | brightplace" (55 chars)
- Last Reviewed updated to September 2026 (was March 2026)
- Featured snippet paragraph added (49-55 words)
- All 3 schemas present with correct /guides/ URLs

### New Content Added
- MD vs VA income tax comparison ($2,600/yr difference at $100K income)
- Rent comparison across all 4 neighborhoods with specific 1BR/2BR ranges
- Rent-vs-own worked example ($34,300 eliminated vs $33,800 new cost)
- Healthcare proximity mapping (NIH, Walter Reed, Inova, VHC Health)
- Purple Line impact section (opening Dec 2027)
- Practical downsizing tips (storage, noise, lease flexibility, rent increases, pets)
- Property recommendations with addresses and pricing

### Files
- Updated article: `Complete Articles/dc-empty-nesters-UPDATED.md`
- SERP analysis: `Content Brief/empty-nester-apartments-dc-suburbs-serp-analysis.md`
- Reddit research: `Reddit Research/empty-nesters-downsizing-dc-metro-reddit-research.md`
- CMS HTML: `Webflow CMS Data/dc-empty-nesters.html`
- CMS JSON: `Webflow CMS Data/dc-empty-nesters.json`

### Stats: Before vs After
| Metric | Before | After |
|---|---|---|
| Word count | ~1,800 | 3,095 |
| H2 sections | 5 (labels) | 10 (questions) |
| FAQ pairs | 0 | 11 |
| Internal links | 0 | 7 |
| External links | 0 | 5 |
| CTAs | 0 | 3 |
| Date stamps | 0 | 36 |
| Focus keyword | 0x | 32x |

### Note
- Article lives in Guides collection (/guides/dc-empty-nesters), NOT Resources
- Guides Collection is RESTRICTED — user must manually update in Webflow Designer
- CMS HTML and JSON files are ready for manual upload

---

*Next session: Continue with articles 3-6 (kansas-city, minneapolis, brooklyn, salt-lake-city)*
