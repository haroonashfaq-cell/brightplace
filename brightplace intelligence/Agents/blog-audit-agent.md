# Blog Audit Agent

**Purpose:** Systematically audit all published brightplace articles for staleness, broken links, outdated data, and SEO gaps. Run this agent periodically (recommended: monthly) to catch ranking-threatening issues before they cause position loss.

---

## How to Run

Tell Claude Code:

> Run the blog audit agent on all articles in `Complete Articles/`

Or for a single article:

> Run the blog audit agent on `Complete Articles/[filename].md`

---

## Audit Checklist (8 Sections)

The agent MUST run ALL 8 sections for every article audited. Never skip a section.

---

### Section 1: Freshness & Date Check

For each article, check:

1. **`last_reviewed` date in frontmatter** -- Is it older than 3 months? Flag as STALE.
2. **`date_modified` in frontmatter and schemas** -- Does it match `last_reviewed`? Flag mismatches.
3. **All date-stamped claims** -- Search for patterns like "(as of Q[N] YYYY)". List each one and check:
   - Is the date more than 2 quarters old? Flag as NEEDS UPDATE.
   - Dollar figures, rent ranges, toll costs, vacancy rates, and market observations go stale fastest.
4. **Property-specific articles** -- Web search the property name to check for:
   - Name changes / rebrands
   - Ownership or management changes
   - Closures or conversions
   - Major renovations
   - Rent price changes (compare article prices to current listings)

**Output format:**
```
FRESHNESS AUDIT: [article-slug]
Last reviewed: [date] -- [OK / STALE (X months old)]
Date-stamped claims found: [count]
  - "[claim text]" -- [OK / STALE by X quarters]
Property status: [UNCHANGED / NAME CHANGE / CLOSED / VERIFY]
```

---

### Section 2: Link Audit

For each article, extract ALL links (internal and external) and check each one:

1. **Internal links** -- Fetch each URL and verify:
   - Returns 200 (not 404, 301, or 500)
   - Uses correct path (`/resources/` not `/knowledgebase/`)
   - Does not appear on the known broken URL list in MEMORY.md
   - Uses `https://` (not `http://`)
   - Uses correct domain (`brightplace.ai` or `www.brightplace.ai`)
   - CTA links: `app.brightplace.ai` for search actions, `brightplace.ai` for brand

2. **External links** -- Fetch each URL and verify:
   - Site is still live and returning content
   - Content is still relevant (e.g., .gov links still point to correct agency)
   - Uses `https://` (not `http://`)

3. **Missing links** -- Does the article have 7+ internal links? If not, flag for link building.

**Output format:**
```
LINK AUDIT: [article-slug]
Internal links: [count] ([OK count] working, [broken count] broken)
  BROKEN: [url] -- [status code / error]
  LEGACY PATH: [url] -- uses /knowledgebase/ instead of /resources/
External links: [count] ([OK count] working, [broken count] broken)
  BROKEN: [url] -- [status code / error]
Internal link count: [count] -- [OK (7+) / NEEDS MORE]
```

---

### Section 3: SEO Structure Check

For each article, verify compliance with ranking optimization rules:

1. **SEO title vs H1** -- Must be different. Flag if identical.
2. **H2 headings** -- Are they in question format matching PAA queries? Flag declarative H2s.
3. **FAQ count** -- Minimum 10 FAQs. Flag if fewer.
4. **FAQ answer length** -- Each answer should be 40-60 words. Flag outliers.
5. **Featured snippet paragraph** -- First content paragraph under H1 should be 49-55 words as a standalone answer. Flag if missing or wrong length.
6. **Entity density** -- Key entities (property name, city, landmarks) should appear 3-8x. Flag if under 3.
7. **Word count** -- Does it meet the target in frontmatter? Flag significant shortfalls.
8. **Schema types** -- Are Article and FAQPage schemas present? Do FAQ schema entries match the article FAQs?
9. **`dateModified` in schemas** -- Does it match the frontmatter `date_modified`?

**Output format:**
```
SEO AUDIT: [article-slug]
SEO title vs H1: [DIFFERENT (OK) / IDENTICAL (FIX)]
H2 format: [X/Y question format] -- [OK / NEEDS CONVERSION]
FAQ count: [count] -- [OK (10+) / LOW (need X more)]
Featured snippet paragraph: [word count] words -- [OK / FIX]
Entity density: [entity: count] -- [OK / LOW]
Schema match: [OK / MISMATCH]
```

---

### Section 4: Brand Compliance

For each article, check for violations of brand rules:

1. **brightplace casing** -- Must always be lowercase. Search for "Brightplace", "BrightPlace", "BRIGHTPLACE".
2. **Em dashes** -- Search for `—` (unicode) and `--` (double hyphen used as em dash). None allowed.
3. **Banned word "signal"** -- Search for any form. Alternatives: "indicator," "suggests," "points to."
4. **Banned phrases** -- Search for: "deep dive," "dive into," "navigate," "landscape," "unlock," "leverage," "whether you're X or Y," "from X to Y," "it's worth noting," "interestingly," "notably," "hidden gem," "best-kept secret," "vibrant," "bustling," "thriving."
5. **Title superlatives** -- No "Top X," "Best," "Ultimate Guide," "#1" in titles.
6. **ILS citations** -- No links to or mentions of Apartments.com, Zillow, Trulia, Rent.com, Zumper, Apartment List, HotPads, RentCafe, Realtor.com.
7. **Review platform citations** -- No links to ApartmentRatings, Yelp, Google Reviews, Niche, AreaVibes.
8. **Score sites** -- No Walk Score, Bike Score, Transit Score mentions.
9. **Markdown tables** -- None allowed in article content (use bold-label bullet points).
10. **Fair Housing** -- No descriptions of neighborhoods by demographics, crime stats, or safety language.

**Output format:**
```
BRAND AUDIT: [article-slug]
brightplace casing: [OK / VIOLATION at line X]
Em dashes: [OK / FOUND at line X]
Banned phrases: [OK / FOUND "phrase" at line X]
ILS/review citations: [OK / FOUND at line X]
Markdown tables: [OK / FOUND at line X]
Fair Housing: [OK / CONCERN at line X]
```

---

### Section 5: Webflow HTML Check

For each article that has a corresponding file in `Webflow CMS Data/`:

1. **`<ul><li>` tags** -- Webflow RichText strips these. Content will disappear. Flag all instances. Convert to `<p><strong>Label:</strong> text</p>` format.
2. **`<ol><li>` tags** -- OK for numbered lists only. Verify they are truly numbered content.
3. **`<h1>` in post-body** -- Not allowed (Webflow uses the `name` field). Flag any `<h1>` tags.
4. **`<script>` tags** -- Webflow strips these from RichText. Flag any embedded scripts.
5. **`http://` links** -- All links must use `https://`. Flag any `http://`.
6. **`/knowledgebase/` paths** -- Must be `/resources/`. Flag legacy paths.
7. **HTML/JSON consistency** -- Does the HTML content match the markdown article? Flag if the markdown has been updated but Webflow files have not.

**Output format:**
```
WEBFLOW AUDIT: [article-slug]
<ul><li> tags: [OK / FOUND X instances -- content may be invisible]
<h1> tags: [OK / FOUND]
<script> tags: [OK / FOUND]
http:// links: [OK / FOUND at X locations]
Legacy paths: [OK / FOUND X instances]
HTML matches markdown: [YES / NO -- markdown updated on [date], HTML last updated [date]]
```

---

### Section 6: Keyword & SERP Landscape Monitoring

For EVERY article, web search the primary keyword and top 2-3 secondary keywords to check:

1. **Search intent shift** -- Has Google changed what it shows for this keyword?
   - Was the SERP showing articles/guides before but now shows listings, maps, or tools? If so, the keyword may no longer be viable for our content type. Flag as INTENT SHIFT.
   - Has a Local Pack, AI Overview, or featured snippet appeared that wasn't there before? Note what content it pulls from.

2. **Ranking position change** -- Search `site:brightplace.ai [keyword]` to confirm we still appear. Then search the keyword without site restriction:
   - Are we still on page 1? If not, flag as DROPPED.
   - Have new competitors entered the top 10 that weren't there when the article was published? List them with URLs and note what they cover that we don't.
   - Has a high-DA site (Wikipedia, government site, major publication) entered the SERP and pushed us down?

3. **Keyword volume shift** -- Has the keyword itself become obsolete?
   - Property renamed? (e.g., "parkside at legacy" -> "legacy north") Flag as KEYWORD DYING.
   - New keyword emerging that we should target instead? (e.g., new property name, new phrasing)
   - Is search volume seasonal? Are we in a low season for this keyword?

4. **People Also Ask changes** -- Search the primary keyword and list ALL current PAA questions:
   - Which PAA questions are covered by our FAQ section? Mark as COVERED.
   - Which PAA questions are NOT in our FAQ section? Mark as MISSING -- these are new FAQ opportunities.
   - Are any of our existing FAQs targeting questions that no longer appear in PAA? Mark as STALE FAQ.

5. **AI Overview / AEO check** -- What does the AI Overview show for this keyword?
   - Is brightplace cited as a source? YES / NO / PARTIAL.
   - What sources ARE being cited? List them.
   - What information does the AI Overview include that our article doesn't? Flag as AI CONTENT GAP.
   - Does the AI Overview contradict any data in our article? Flag as AI CONFLICT.

6. **Competitor content freshness** -- For each competitor in the top 5:
   - When was their content last updated? (check for date stamps, "updated" notices)
   - If competitors have fresher content, flag as COMPETITORS FRESHER.
   - What specific content do they have that we lack? (tables, calculators, maps, images, videos, more FAQs, deeper data)

**Output format:**
```
KEYWORD AUDIT: [article-slug]
Primary keyword: [keyword]
Search intent: [UNCHANGED / SHIFTED to (listings/maps/tools/other)]
Ranking position: [PAGE 1 / PAGE 2+ / NOT FOUND]
Keyword viability: [ACTIVE / DECLINING / OBSOLETE (new keyword: X)]
PAA coverage: [X/Y covered] -- MISSING: [list uncovered questions]
AI Overview: [CITING US / NOT CITING US / NO AI OVERVIEW]
  AI sources: [list]
  AI content gaps: [list what AI shows that we don't cover]
Competitor freshness: [WE ARE FRESHEST / COMPETITORS FRESHER (list)]
New competitors since publish: [count] -- [list URLs + what they cover]
```

---

### Section 7: Data Accuracy Verification

For EVERY article, extract ALL factual claims and verify each one against current sources. This is the most critical section for preventing ranking loss due to inaccurate information.

**7a. Price & Cost Data Verification**

For every dollar figure, rent range, fee, or cost mentioned in the article:

1. **Rent prices** -- Web search the property name + "rent prices" or check listing sites to find current actual pricing. Compare article figures to current reality:
   - Has the range shifted up or down by more than 10%? Flag as PRICE INACCURATE.
   - Are we quoting a range that no longer exists (e.g., property no longer offers studios)? Flag as UNIT TYPE CHANGED.
   - Is the concession information still current? (e.g., "one month free" may now be "four weeks free" or nothing)

2. **Toll costs, commute costs, fee estimates** -- Verify against current rate schedules:
   - Have toll rates changed? Check NTTA, state DOT, or transit authority sites.
   - Have transit fares changed? Check local transit authority.
   - Are any cost estimates more than 15% off from current reality? Flag as COST INACCURATE.

3. **Market statistics** -- Verify vacancy rates, rent growth percentages, absorption numbers:
   - Web search "[city] apartment vacancy rate [current year]" to find latest data.
   - Is our market data more than 2 quarters old? Flag as MARKET DATA STALE.
   - Does current data contradict our narrative? (e.g., we say "softening market" but it's now tightening) Flag as NARRATIVE OUTDATED.

**7b. Entity & Fact Verification**

For every named entity (business, employer, school, transit line, development):

1. **Employers** -- Are all listed employers still operating at the stated locations?
   - Web search each employer name + city to check for closures, relocations, or layoffs.
   - Are there major NEW employers that should be added? (e.g., AT&T HQ moving to Legacy corridor)
   - Has employee count changed significantly? Flag if a listed employer has had major layoffs or expansions.

2. **Schools & districts** -- Are ratings/rankings still accurate?
   - Web search "[school district] rating [current year]" to verify.
   - Has the TEA rating, Niche grade, or test score data changed? Flag if outdated.

3. **Transit & infrastructure** -- Has anything changed?
   - New transit lines opened? (e.g., DART Silver Line)
   - Stations closed or renamed?
   - Route changes affecting commute times we quoted?
   - New roads, highways, or toll roads opened?

4. **Nearby developments** -- Any new construction, openings, or closures?
   - New apartment communities that should be mentioned as competitors?
   - Retail/restaurant closures we reference? (e.g., "walking distance to Whole Foods" -- is it still there?)
   - Major construction projects affecting the area?

5. **Property-specific facts** -- For property articles:
   - Has the property been renamed, sold, or changed management? (CRITICAL -- this was the #1 issue with Parkside at Legacy)
   - Have amenities been added or removed?
   - Has the unit mix changed? (e.g., added studios, removed 3BR)
   - Has the address changed?
   - Has the year built information changed? (renovations may reset this)
   - Is the pet policy still accurate?

6. **Competitor properties** -- For any properties named in comparison sections:
   - Do they still exist under those names? Web search each one.
   - Are their price ranges still comparable to what we state?
   - Have any been demolished, converted, or rebranded?

**7c. Legal & Regulatory Verification**

1. **Government links** -- Do all .gov links still point to the correct agency/page?
2. **Regulatory bodies** -- Are licensing bodies (TREC, state agencies) still operating under the same name and URL?
3. **Legal requirements** -- Have any rental laws, fair housing rules, or disclosure requirements changed in the article's jurisdiction?

**Output format:**
```
DATA ACCURACY AUDIT: [article-slug]

PRICES & COSTS:
  Rent ranges: [ACCURATE / INACCURATE -- current: $X-$Y, article says: $A-$B]
  Concessions: [ACCURATE / OUTDATED -- current: X, article says: Y]
  Toll/commute costs: [ACCURATE / CHANGED -- current: $X, article says: $Y]
  Market stats: [ACCURATE / STALE -- current: X%, article says: Y%]

ENTITIES & FACTS:
  Employers: [ALL VERIFIED / CHANGES FOUND]
    - [employer]: [STILL THERE / RELOCATED / CLOSED / LAYOFFS / NEW]
  Schools: [ACCURATE / RATING CHANGED]
  Transit: [ACCURATE / NEW SERVICE / ROUTE CHANGE]
  Property status: [UNCHANGED / RENAMED / SOLD / RENOVATED]
  Competitor properties: [ALL VERIFIED / X UNVERIFIABLE / X RENAMED]

CLAIMS NEEDING UPDATE: [count]
  1. "[claim text]" -- CURRENT REALITY: [what's actually true now]
  2. ...

CLAIMS VERIFIED AS STILL ACCURATE: [count]
```

---

### Section 8: Content Gap Analysis

For every article (property AND topic), run a web search to identify:

1. **Competitor content** -- Are new articles ranking for the same keyword? What do they cover that we don't?
2. **People Also Ask** -- What PAA questions appear? Are they covered in our FAQ section?
3. **AI Overview** -- What does the AI Overview show? Is our content being cited?
4. **New information** -- Any new developments, nearby construction, employer changes, transit updates, school rating changes?
5. **Review landscape** (property articles only) -- Have significant new reviews appeared that change the narrative?

**Output format:**
```
CONTENT GAP AUDIT: [article-slug]
New competitors: [count] -- [list URLs]
Uncovered PAA questions: [list]
AI Overview citing brightplace: [YES / NO / PARTIAL]
New information to add: [list]
Review changes: [SIGNIFICANT / MINOR / NONE]
```

---

## Priority Scoring

After running all 8 sections, assign a priority score:

- **P0 (Critical -- fix within 24 hours):** Broken internal links, property name changes, closed properties, content disappearing due to Webflow HTML issues, keyword becoming obsolete (property renamed), rent prices off by 20%+, employer/business we reference has closed
- **P1 (High -- fix within 1 week):** Pricing data more than 2 quarters stale, fewer than 6 FAQs, SEO title identical to H1, brand violations, search intent shifted (SERP now shows different content type), AI Overview contradicts our data, competitors have substantially fresher content
- **P2 (Medium -- fix within 1 month):** Pricing data 1-2 quarters stale, fewer than 10 FAQs, declarative H2 headings, missing internal links, new competitor content, 3+ uncovered PAA questions, market narrative outdated, new transit/infrastructure not mentioned
- **P3 (Low -- fix in next content cycle):** Minor freshness updates, entity density optimization, schema mismatches, 1-2 uncovered PAA questions, minor price drift (<10%), new development to mention

---

## Batch Audit Output Format

When auditing multiple articles, output a summary table at the end:

```
============================================
BATCH AUDIT SUMMARY -- [DATE]
============================================

ARTICLE                              | PRIORITY | TOP ISSUES
-------------------------------------|----------|------------------------------------------
parkside-at-legacy-plano             | P0       | Property renamed, 2 broken links, stale pricing
camden-copper-square-apartments      | P1       | Pricing stale by 3 quarters, only 5 FAQs
discovery-at-space-coast             | P2       | 8 FAQs (need 10+), 2 declarative H2s
studio-apartments                    | P3       | Schema date mismatch
...

TOTAL ARTICLES AUDITED: [count]
P0 (Critical): [count]
P1 (High): [count]
P2 (Medium): [count]
P3 (Low): [count]
ALL CLEAR: [count]
```

---

## Running the Full Portfolio Audit

To audit ALL articles at once, use this prompt with Claude Code:

```
Read the blog audit agent at Agents/blog-audit-agent.md, then run a full
portfolio audit across every article in Complete Articles/. For each article:

1. Read the markdown file
2. Check for a matching Webflow CMS Data file
3. Run all 8 audit sections (Freshness, Links, SEO, Brand, Webflow, Keywords/SERP, Data Accuracy, Content Gaps)
4. Assign a priority score
5. Output the batch summary table

Start with property-specific articles (apartment community names) as they
are most likely to have stale data. Then audit topic articles.

For any P0 issues found, stop and report immediately before continuing
the audit.
```

---

## Scheduling Recommendation

- **Weekly:** Run Section 2 (Link Audit) only across all articles
- **Bi-weekly:** Run Section 6 (Keyword & SERP Landscape) on top 10 performing articles
- **Monthly:** Run full 8-section audit on all articles
- **After any property article is 3+ months old:** Run Sections 1, 6, and 7 (Freshness, Keywords, Data Accuracy)
- **After Google algorithm update:** Run Section 3 (SEO Structure) across all articles
- **After a ranking drop is noticed:** Run Sections 6 + 7 + 8 (Keywords, Data Accuracy, Content Gaps) on the affected article immediately
