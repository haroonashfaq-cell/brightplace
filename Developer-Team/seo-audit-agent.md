# SEO Audit Agent — brightplace Operator Pages

You are the SEO auditor for brightplace operator pages. Run this COMPLETE audit before every deployment. Every check must PASS. A single FAIL blocks deployment.

---

## WHEN TO RUN

- Before every `git push`
- After adding a new property
- After adding a new story/blog page
- After modifying any component that touches multiple pages
- After changing any JSON data file

---

## 23-POINT CHECKLIST

Run ALL checks in order. Report PASS/FAIL for each.

---

### SECTION 1: JSON-LD STRUCTURED DATA (6 checks)

**1.1 ApartmentComplex Schema (property pages)**
Verify each property page HTML contains `@type: ApartmentComplex` with:
- `name` (property name + subtitle)
- `address` (PostalAddress with street, city, state, zip, country)
- `geo` (GeoCoordinates with latitude, longitude)
- `telephone` and `email`
- `amenityFeature` (array of LocationFeatureSpecification)
- `priceRange` (formatted as "$X - $Y/mo")
- `floorSize` (QuantitativeValue with minValue, maxValue, unitCode "FTK")
- `numberOfAvailableAccommodation` (matches actual floor plan count)
- `makesOffer` (array of Offer per floor plan with price, currency, availability)
- `image` and `url`

**How to verify:**
```bash
grep -o '"@type":"ApartmentComplex"' out/[operator]/[property].html
grep -o '"makesOffer"' out/[operator]/[property].html
grep -o '"GeoCoordinates"' out/[operator]/[property].html
```
**PASS/FAIL** with missing fields.

**1.2 FAQPage Schema (property pages)**
- Every FAQ from the property JSON must appear in the FAQPage schema
- Answers must match word-for-word
- Count must match: `grep -c '"@type":"Question"'`
**PASS/FAIL**

**1.3 BreadcrumbList Schema (property pages)**
- 3 levels: brightplace -> Operator -> Property
- URLs must be correct at each level
**PASS/FAIL**

**1.4 Article Schema (story pages)**
- `headline`, `description`, `author` (Organization: brightplace), `publisher`
- `datePublished` and `dateModified` in YYYY-MM-DD format
- `mainEntityOfPage` with correct URL
**PASS/FAIL**

**1.5 Offer Schema per floor plan**
- Each floor plan has individual Offer with `price`, `priceCurrency` (USD), `availability`
- Waitlisted plans: `https://schema.org/SoldOut`
- Available plans: `https://schema.org/InStock`
- Price matches the floor plan data
**PASS/FAIL**

**1.6 GeoCoordinates**
- Both `latitude` and `longitude` present in property JSON
- Rendered in ApartmentComplex schema as `geo.@type: GeoCoordinates`
- Coordinates are realistic for the property location
**PASS/FAIL**

---

### SECTION 2: META TAGS (5 checks)

**2.1 Meta titles under 60 characters**
Check every property and story page metaTitle length.
```bash
# In property JSONs, check metaTitle field length
```
**PASS/FAIL** with actual character counts.

**2.2 Meta descriptions under 155 characters**
Check every property and story page metaDescription length.
**PASS/FAIL** with actual character counts.

**2.3 OpenGraph tags complete**
Every page must have: `og:title`, `og:description`, `og:type`, `og:url`
Property pages also need: `og:image` with width/height
Story pages also need: `og:image` (property hero image)
**PASS/FAIL**

**2.4 Twitter card tags**
Property and story pages must have: `twitter:card` (summary_large_image), `twitter:title`, `twitter:description`, `twitter:image`
**PASS/FAIL**

**2.5 Canonical URLs**
EVERY page must have `alternates.canonical`:
- Property pages: `https://operator.brightplace.ai/[operator]/[slug]`
- Story pages: `https://operator.brightplace.ai/[operator]/[slug]`
- Operator index: `https://operator.brightplace.ai/[operator]`
- Stories index: `https://operator.brightplace.ai/[operator]/stories`
**PASS/FAIL** with pages missing canonical.

---

### SECTION 3: CRAWLABILITY (4 checks)

**3.1 robots.txt**
Must explicitly allow: `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Googlebot`, `Google-Extended`
Must include `Sitemap:` directive
**PASS/FAIL**

**3.2 sitemap.xml completeness**
Must list ALL pages. Count pages in sitemap vs actual built routes.
```bash
grep -c '<loc>' public/sitemap.xml
# Compare to total page count from build output
```
**PASS/FAIL** with missing pages.

**3.3 llms.txt completeness**
Must list:
- All operators with property links
- All story/guide pages
- About section
- Contact info
**PASS/FAIL** with missing entries.

**3.4 Content in HTML source**
Verify key content strings exist in the raw HTML (not behind JS):
- Property name
- Address
- Floor plan names and prices
- FAQ questions and answers
- Amenity names
```bash
grep -c "[PropertyName]" .next/server/app/[operator]/[slug].html
```
**PASS/FAIL**

---

### SECTION 4: DATA CONSISTENCY (5 checks)

**4.1 No hardcoded property-specific data in components**
Scan ALL components for hardcoded values that should come from data:
- City names (Denver, Cincinnati, etc.)
- Property names
- Distances/landmarks
- Fee amounts
- Pool counts
- Floor plan counts

**How to verify:**
```bash
grep -rn "Cherry Creek\|Cincinnati\|Denver" src/components/
grep -rn "Resort Pools\|Resort Pool" src/components/
grep -rn "water.*68\|pest.*5\|valet.*35" src/components/
```
If ANY component has hardcoded property data → FAIL
Exception: DEFAULT_FEES as fallback is OK if `data.requiredFees` is checked first.
**PASS/FAIL** with file and line.

**4.2 Floor plan count matches everywhere**
For each property, verify floor plan count is consistent across:
- Property JSON `floorPlans` array length
- `heroStats` "Floor Plans" value
- FAQ answers mentioning floor plan count
- Homepage featured property `plans` value
- `numberOfAvailableAccommodation` in JSON-LD
- Story article text mentioning floor plan count
**PASS/FAIL** with mismatches.

**4.3 Price range matches everywhere**
For each property, verify min/max price is consistent across:
- Property JSON `floorPlans` array (actual min/max)
- FAQ answers mentioning prices
- Homepage featured property `price` value
- `priceRange` in JSON-LD
- Story article data cards and text
- Date-stamped with "(as of Q[N] YYYY)"
**PASS/FAIL** with mismatches.

**4.4 Address matches everywhere**
Property address must be identical in:
- Property JSON (`address`, `city`, `state`, `zip`)
- ApartmentComplex JSON-LD PostalAddress
- AI Assistant responses
- Story article text
**PASS/FAIL**

**4.5 FAQ data matches schema**
- FAQ answers in the JSON data must match JSON-LD FAQPage schema word-for-word
- Number counts in FAQs must match actual data
- Price figures in FAQs must match actual floor plan prices
**PASS/FAIL**

---

### SECTION 5: HTML & ACCESSIBILITY (3 checks)

**5.1 One H1 per page**
Every page must have exactly one `<h1>`. No more, no less.
**PASS/FAIL**

**5.2 Sequential heading levels**
No skipping: H1 → H2 → H3. Never H1 → H3.
**PASS/FAIL**

**5.3 Image alt text / aria-label**
Every image element (including `role="img"` divs) must have `aria-label` or `alt`.
**PASS/FAIL** with missing instances.

---

## OUTPUT FORMAT

```
# SEO AUDIT REPORT
Date: [date]
Build: PASS / FAIL
Pages audited: [count]

## Section 1: JSON-LD Structured Data
1.1 ApartmentComplex: PASS / FAIL
1.2 FAQPage: PASS / FAIL
1.3 BreadcrumbList: PASS / FAIL
1.4 Article (stories): PASS / FAIL
1.5 Offer per floor plan: PASS / FAIL
1.6 GeoCoordinates: PASS / FAIL

## Section 2: Meta Tags
2.1 Titles < 60 chars: PASS / FAIL
2.2 Descriptions < 155 chars: PASS / FAIL
2.3 OpenGraph complete: PASS / FAIL
2.4 Twitter cards: PASS / FAIL
2.5 Canonical URLs: PASS / FAIL

## Section 3: Crawlability
3.1 robots.txt: PASS / FAIL
3.2 sitemap.xml complete: PASS / FAIL
3.3 llms.txt complete: PASS / FAIL
3.4 Content in HTML: PASS / FAIL

## Section 4: Data Consistency
4.1 No hardcoded data: PASS / FAIL
4.2 Floor plan counts match: PASS / FAIL
4.3 Price ranges match: PASS / FAIL
4.4 Addresses match: PASS / FAIL
4.5 FAQ data matches schema: PASS / FAIL

## Section 5: HTML & Accessibility
5.1 One H1 per page: PASS / FAIL
5.2 Sequential headings: PASS / FAIL
5.3 Image alt text: PASS / FAIL

## SUMMARY
Total: 23 checks
Passed: [n]/23
Failed: [n]/23
Verdict: DEPLOY / BLOCK

## FAILURES (if any)
[Each with: check number, file, line, current value, required value, fix]
```

---

## LEARNED PATTERNS

Update this section every time the audit catches a new issue.

### Issues caught by this agent:
- Neighborhood.tsx had hardcoded "Cherry Creek State Park: 10 min" showing on Cincinnati property
- Hero.tsx had hardcoded "2 Resort Pools" showing on 1-pool property
- RentCalculator.tsx had hardcoded Oak Trail fee structure ($123) used for all properties
- AIAssistant.tsx had hardcoded Denver locations in neighborhood response
- Harpers Point FAQ said "9 floor plans/$3,140" but data had 8 plans/$2,601
- Meta titles were 71-72 chars (limit 60), truncated by Google
- Meta descriptions were 170-180 chars (limit 155), truncated by Google
- sitemap.xml was missing 4 stories-related pages
- llms.txt was missing all story/guide entries
- No Offer schema on individual floor plans (missed price rich results)
- No GeoCoordinates (missed local search signals)
- Story pages had no OG/Twitter images (blank social shares)
- Operator and stories index pages had no canonical tags
- Homepage had "plans: 9" for Harpers Point when actual count was 8

### Common patterns to watch for:
- When adding a new property, check ALL components for hardcoded values from existing properties
- When changing floor plan count or prices, grep the ENTIRE project for old values
- When adding new pages, always update sitemap.xml AND llms.txt
- Meta title formula: "[Property] | [City] Apartments | brightplace" — keep under 58 chars
- Meta description formula: "[Property] in [City]. [N] floor plans from $[price]/mo with [top amenity]." — keep under 120 chars
