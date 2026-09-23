# brightplace.ai — Post-Migration Issues

**For:** Dennis (and his coding agent)
**Audited:** 2026-09-23 against live production
**Site:** `https://www.brightplace.ai` — Next.js on Vercel

This file is self-contained. You do not need access to any other repository — the data you need
is embedded below.

---

## Context

Two migrations completed successfully:

1. Webflow content (guides, resources, news) → Vercel, **paths unchanged**
2. `app.brightplace.ai` → `www.brightplace.ai`, including ~22,774 `/property/*` pages

Both work. All 148 original URLs return 200, redirects preserve paths, GA4 is live, and every
content page carries canonical, meta description, Open Graph, Twitter Card, JSON-LD and exactly
one `<h1>`. Content fidelity is 100% — no truncation.

**Five issues remain.** They are listed in priority order. Issue 1 is time-sensitive; the rest are
hygiene.

---

## Order of work, and who owns what

**Do Issues 1 and 2 as a single piece of work.** They have the same root cause and the same fix:
`sitemap.xml` and `robots.txt` are static copies rather than generated. Replacing the copy with a
generator resolves Issue 1 and all three sub-issues of Issue 2 at once. Treating them as two
tickets means building the generator, then editing a file the generator overwrites.

| # | Issue | Owner | Depends on |
|---|---|---|---|
| 1 + 2 | Generate sitemap and robots instead of copying | **Dev** | — |
| 3 | `dateModified` before `datePublished` | **Dev** — one rule in the page generator | — |
| 4 | `datePublished` is the migration timestamp | **Dev**, using the dates in the Appendix | Confirm where the value is set |
| 5 | Two articles without `og:image` | **Dev** | Content may need to supply an image |

Issue 4 is the only one needing a decision before work starts: if `datePublished` is read from a
content field, the fix is a data backfill and brightplace should do it. If it is stamped at build
time, the fix is in the generator and Dennis should do it. **Check which, then assign.** The dates
themselves are in the Appendix either way.

Issue 5 likewise: if the two articles genuinely have no hero image, someone has to make one — that
is brightplace's job, not a code fix.

---

## 🔴 Issue 1 — 22,774 property pages are missing from the sitemap

**Severity: high. Do this first — together with Issue 2, which shares the same fix.**

### What's wrong

```
https://www.brightplace.ai/sitemap.xml    → 148 URLs, ZERO /property/ entries
https://app.brightplace.ai/sitemap.xml    → 308 redirects to the www sitemap
/sitemap_index.xml /sitemap-0.xml         → 404
/property-sitemap.xml                     → 404
```

The live `sitemap.xml` is a **byte-identical copy of the old Webflow file** (23,704 bytes, 148
URLs). It was copied across rather than generated. When `app.brightplace.ai` started redirecting,
its 22,774-URL sitemap disappeared with it and nothing replaced it.

There is also no crawl path: the homepage has **8 internal links and zero** pointing at
`/property/`.

So 99% of the site's URLs just changed hostname and Google has neither a sitemap nor a link path
to rediscover them.

The property pages themselves are correct — self-referencing canonical on `www`, `index, follow`,
JSON-LD, GA4. They are simply undiscoverable.

### Fix

1. Generate `/sitemap.xml` as a **sitemap index** (not a flat `<urlset>`). A single file caps at
   50,000 URLs and 50MB; with ~22,900 URLs you want several child files anyway for sane
   regeneration — e.g. `/sitemap-content.xml` plus `/sitemap-property-1.xml`, `-2.xml`, …
2. Generate from the content/property source, never by copying a file.
3. Include **all** URL classes (see the checklist in Issue 2 — the current spec under-counts).
4. Submit the index in Google Search Console under the `www.brightplace.ai` property.
5. Add internal links to property pages so discovery does not depend on the sitemap alone.

### Verify

```bash
curl -s https://www.brightplace.ai/sitemap.xml | head -3          # expect <sitemapindex>
curl -s https://www.brightplace.ai/sitemap.xml | grep -c '<loc>'  # child sitemap count
# then, across all children, total <loc> should be ~22,900 not 148
```

---

## 🟠 Issue 2 — sitemap and robots.txt are static copies, so three bugs persist

Both files are byte-identical to the Webflow originals. Generating them fixes all of the below.

**Do this with Issue 1, not after it.** Same root cause, same fix — one generator resolves both. Fixing these by hand first means editing files the generator will overwrite.

### 2a. Four live pages are absent from the sitemap

All four return **HTTP 200** and none appear in `sitemap.xml`:

```
/resources/apartment-with-terrace
/resources/apartments-with-gyms
/resources/apartments-with-pools
/resources/washer-dryer-in-unit-apartments
```

They were missing from Webflow's sitemap too (published 2026-09-14, right before cutover). A
generated sitemap includes them by construction.

### 2b. `robots.txt` emits the `Sitemap:` directive twice

Current:

```
User-agent: *
Allow: /
Disallow: /*?*_page=
Sitemap: https://www.brightplace.ai/sitemap.xml

Sitemap: https://www.brightplace.ai/sitemap.xml
```

Should be:

```
User-agent: *
Allow: /
Sitemap: https://www.brightplace.ai/sitemap.xml
```

`Disallow: /*?*_page=` was a Webflow pagination artifact. The new `/resources` archive renders all
items with no pagination, so drop it once the archives ship with self-referencing canonicals.

### 2c. `lastmod` is frozen and new content will not appear

Values are stuck at Webflow's. Newly published articles will never enter the sitemap until it is
generated from source.

### URL classes the sitemap must cover

A generator that walks only the article folder silently drops most of this:

| Class | Count |
|---|---|
| `/property/<state>/<city>/<name>/<id>` | **~22,774** |
| `/resources/<slug>` | 80 |
| `/guides/<slug>` | 31 |
| `/news/<slug>` | 9 |
| `/category/<slug>` | 7 |
| `/communities/<slug>` | 6 |
| `/stories/<slug>` | 3 |
| `/author/<slug>` | 3 |
| `/operators/<slug>` | 1 |
| Archive indexes — `/guides` `/resources` `/news` `/communities` `/operators` | 5 |
| Static — `/` `/contact-us` `/privacy` `/terms` `/fair-housing` `/financial-disclosure` `/property-managers` `/community-voice-survey` `/llm-info` `/search` | 10 |

**If the total comes out at 148, the old file was reproduced rather than regenerated.**

---

## 🟠 Issue 3 — `dateModified` is earlier than `datePublished` on 71 articles

A page cannot be modified before it was published. Google flags this in Rich Results.

Examples from live pages:

| URL | datePublished | dateModified | Gap |
|---|---|---|---|
| `/resources/2-bedroom-2-bathroom-apartments` | 2026-08-20 | 2026-07-06 | 45 days earlier |
| `/resources/prorated-rent` | 2026-08-26 | 2026-08-24 | 2 days earlier |
| `/resources/2nd-chance-apartments-houston` | 2026-08-26 | 2026-08-24 | 2 days earlier |

### Fix

```
dateModified = max(last_updated, last_published)
```

This changes no displayed date. It only removes the impossible ordering.

---

## 🟡 Issue 4 — `datePublished` is the migration timestamp on 47 articles

### What's wrong

The migration republish overwrote Webflow's `last_published`, and that value is being rendered as
`datePublished`. So 47 articles claim they were published in mid-September 2026 when they are
months older.

Example — `/resources/pet-deposit-vs-pet-fee`:

```
live page says:  datePublished 2026-09-17
actually:        created_on    2026-07-13
```

### Honest severity

**This is hygiene, not a ranking emergency.** Page age is not a direct Google ranking factor and a
newer displayed date is often neutral for CTR. What it does risk:

- Google's structured-data guidelines require accurate dates. Systematic inaccuracy across 47
  articles risks Google distrusting the date markup sitewide.
- It destroys the baseline for measuring content age, decay and refresh impact.
- A future "updated October 2026" freshness strategy needs a truthful starting point.

### Fix

Set `datePublished = created_on`, using the table in the appendix. All 124 published articles have
a real date — there are no gaps and no exceptions to special-case.

Five articles legitimately show a September 2026 date because they genuinely were created then
(`apartment-with-terrace`, `apartments-with-gyms`, `apartments-with-pools`,
`washer-dryer-in-unit-apartments`). Those are correct as-is.

**Note:** `last_updated` was also overwritten on 45 articles, so the true last-edit date is not
recoverable for those. Only `datePublished` can be fully restored.

---

## 🟡 Issue 5 — two articles ship without `og:image`

```
/resources/las-brisas-apartments-california
/resources/randolph-towers-ballston-arlington-va
```

Both have no featured image in the source data, so they render with no Open Graph image and share
as a bare link. Add images, or render a site-wide fallback `og:image` so no page ships without one.

---

## Do not change these — they are correct and were verified

Regressions here would break URL parity with what Google already has indexed.

| Behaviour | Current | Keep |
|---|---|---|
| Trailing slash | `/guides/` → 308 → `/guides` | ✅ |
| Apex → www | `brightplace.ai/x` → 308 → `www.brightplace.ai/x`, path preserved | ✅ |
| `app.` → `www.` | 308, path preserved byte-for-byte | ✅ |
| Unknown paths | real 404, not a soft 200 | ✅ |
| `/knowledgebase/*` | 404 — **do not** redirect to `/resources/` | ✅ |
| `llms.txt` | byte-identical to the original, including the Fair Housing line | ✅ |
| Canonical | absolute, self-referencing, `https://www.brightplace.ai/...` | ✅ |
| `app.brightplace.ai` | keep alive and redirecting for at least 12 months | ✅ |

---

## Acceptance checks

Run against production after the fixes.

```bash
# 1. sitemap is an index and covers property
curl -s https://www.brightplace.ai/sitemap.xml | head -3 | grep -q sitemapindex && echo OK

# 2. the four previously-missing resources are listed
for s in apartment-with-terrace apartments-with-gyms apartments-with-pools washer-dryer-in-unit-apartments; do
  curl -s https://www.brightplace.ai/sitemap.xml | grep -c "/resources/$s<"
done

# 3. robots.txt emits Sitemap once
curl -s https://www.brightplace.ai/robots.txt | grep -c '^Sitemap:'     # expect 1

# 4. no page reports dateModified before datePublished
#    (spot-check, then run across the sitemap)
curl -s https://www.brightplace.ai/resources/prorated-rent \
  | grep -oE '"datePublished":"[^"]*"|"dateModified":"[^"]*"'

# 5. og:image present on every content page
curl -s https://www.brightplace.ai/resources/las-brisas-apartments-california \
  | grep -c 'property="og:image"'                                        # expect >=1

# 6. parity — these must not change
curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' https://www.brightplace.ai/guides/
curl -s -o /dev/null -w '%{http_code}\n' https://www.brightplace.ai/knowledgebase/prorated-rent
```

---

## Appendix — `datePublished` backfill data

Source: the Webflow CMS API, captured 2026-09-17 **before** cutover. These values no longer exist
in Webflow (the republish overwrote `last_published`, and `last_updated` on 45 items).

Join on `slug`. Use `created_on` as `datePublished`.

| collection | slug | created_on (use as datePublished) | last_updated |
|---|---|---|---|
| guides | `atlanta-active-renters` | `2026-04-13T11:16:21Z` | `2026-09-17T11:52:46Z` |
| guides | `austin-north-central-renters` | `2026-09-03T16:21:21Z` | `2026-09-03T17:02:35Z` |
| guides | `austin-young-professionals` | `2026-04-13T11:16:21Z` | `2026-09-16T23:20:18Z` |
| guides | `brooklyn-neighborhood-guide` | `2026-04-29T15:24:27Z` | `2026-09-17T11:52:46Z` |
| guides | `charlotte-affordable-neighborhoods` | `2026-04-21T09:02:18Z` | `2026-09-17T11:51:42Z` |
| guides | `chicago-pet-owners` | `2026-04-13T11:16:21Z` | `2026-09-16T23:48:28Z` |
| guides | `columbia-usc-student` | `2026-04-13T11:16:21Z` | `2026-09-17T11:52:46Z` |
| guides | `dallas-families` | `2026-04-13T11:16:21Z` | `2026-09-03T15:27:44Z` |
| guides | `dc-empty-nesters` | `2026-04-13T11:16:21Z` | `2026-09-17T11:52:46Z` |
| guides | `denver-city-orientation` | `2026-04-21T11:14:04Z` | `2026-09-17T11:52:46Z` |
| guides | `dog-friendly-neighborhoods-san-diego` | `2026-05-06T20:40:42Z` | `2026-09-17T11:52:46Z` |
| guides | `fort-collins-outdoor-renters` | `2026-04-13T11:16:21Z` | `2026-09-17T11:52:46Z` |
| guides | `greensboro-renters-orientation` | `2026-04-13T11:16:21Z` | `2026-09-16T23:48:28Z` |
| guides | `houston-city-orientation` | `2026-04-21T10:41:16Z` | `2026-09-17T11:52:46Z` |
| guides | `how-to-rent-an-apartment` | `2026-04-22T11:13:45Z` | `2026-09-01T18:38:16Z` |
| guides | `huntsville-renters-orientation` | `2026-04-20T08:49:48Z` | `2026-09-17T11:52:46Z` |
| guides | `kansas-city-young-professionals` | `2026-04-22T07:47:45Z` | `2026-09-16T23:20:18Z` |
| guides | `knoxville-young-professionals` | `2026-04-21T07:20:29Z` | `2026-09-17T11:51:42Z` |
| guides | `lexington-student-neighborhoods-uk` | `2026-04-21T09:09:04Z` | `2026-09-17T11:52:46Z` |
| guides | `miami-city-orientation` | `2026-04-21T11:37:10Z` | `2026-04-27T19:26:38Z` |
| guides | `minneapolis-city-orientation` | `2026-04-21T12:06:12Z` | `2026-09-17T11:52:46Z` |
| guides | `nashville-corporate-relocation-neighborhoods` | `2026-04-21T09:39:34Z` | `2026-09-17T11:52:46Z` |
| guides | `philadelphia-city-orientation` | `2026-04-21T10:56:53Z` | `2026-09-17T11:52:46Z` |
| guides | `phoenix-renters-orientation` | `2026-04-13T11:16:21Z` | `2026-09-16T23:48:28Z` |
| guides | `raleigh-durham-young-professionals` | `2026-04-13T11:16:21Z` | `2026-09-17T11:51:42Z` |
| guides | `relocating-to-austin` | `2026-04-29T17:34:02Z` | `2026-09-03T17:36:14Z` |
| guides | `salt-lake-city-renters-orientation` | `2026-04-21T08:02:11Z` | `2026-09-17T11:52:46Z` |
| guides | `tampa-renters-orientation` | `2026-04-21T08:11:28Z` | `2026-09-17T11:52:46Z` |
| guides | `uf-gainesville-student-housing` | `2026-04-22T09:13:04Z` | `2026-09-17T11:52:46Z` |
| guides | `ut-austin-student-housing` | `2026-04-22T08:51:02Z` | `2026-09-17T11:51:42Z` |
| guides | `your-true-monthly-cost` | `2026-04-22T09:27:23Z` | `2026-04-29T19:44:40Z` |
| news | `a-quiet-revolution-in-the-rental-market` | `2026-06-22T19:18:14Z` | `2026-06-25T17:11:45Z` |
| news | `brightplace-commercial-observer-coverage` | `2026-06-17T19:10:58Z` | `2026-06-25T16:52:33Z` |
| news | `brightplace-connect-launch` | `2026-06-17T19:10:58Z` | `2026-06-25T16:53:29Z` |
| news | `brightplace-financial-intelligence-launch` | `2026-06-17T19:10:58Z` | `2026-06-25T16:55:00Z` |
| news | `brightplace-launches-ai-native-apartment-search` | `2026-06-17T19:10:58Z` | `2026-06-25T17:10:32Z` |
| news | `brightplace-multifamily-executive-coverage` | `2026-06-17T19:10:58Z` | `2026-06-25T16:52:59Z` |
| news | `how-brightplace-became-ai-search-favorite` | `2026-06-30T20:08:56Z` | `2026-07-06T15:49:31Z` |
| news | `ten-questions-brightplace-founder` | `2026-06-17T19:10:58Z` | `2026-06-25T16:51:25Z` |
| news | `what-we-learned-about-mcp-building-brightplace-connect` | `2026-06-25T15:23:26Z` | `2026-07-06T12:59:56Z` |
| resources | `113-university-place` | `2026-08-03T21:38:23Z` | `2026-08-25T16:20:54Z` |
| resources | `17-battery-place-new-york` | `2026-08-10T11:24:00Z` | `2026-09-14T10:51:50Z` |
| resources | `2-bedroom-2-bathroom-apartments` | `2026-06-30T17:07:22Z` | `2026-07-06T12:20:47Z` |
| resources | `2-bedroom-apartments-bloomington-in` | `2026-05-21T10:06:21Z` | `2026-09-17T17:43:32Z` |
| resources | `2nd-chance-apartments-houston` | `2026-05-07T22:39:49Z` | `2026-08-24T21:05:03Z` |
| resources | `3-bedroom-apartments-knoxville-tn` | `2026-06-24T12:18:33Z` | `2026-09-17T17:43:32Z` |
| resources | `3-bedroom-townhomes-for-rent-near-me` | `2026-07-06T10:43:42Z` | `2026-09-17T16:51:26Z` |
| resources | `4-bedroom-apartments-orlando` | `2026-05-07T22:35:32Z` | `2026-08-24T21:05:03Z` |
| resources | `affordable-places-to-live-in-florida` | `2026-08-17T09:03:13Z` | `2026-08-18T17:15:01Z` |
| resources | `apartment-checklist-first-apartment` | `2026-07-07T11:47:42Z` | `2026-09-17T17:43:32Z` |
| resources | `apartment-with-terrace` | `2026-09-14T22:52:45Z` | `2026-09-15T18:10:28Z` |
| resources | `apartments-near-university-of-texas-san-antonio` | `2026-07-13T10:23:48Z` | `2026-09-17T17:43:32Z` |
| resources | `apartments-with-attached-garages` | `2026-06-09T17:06:46Z` | `2026-09-17T17:43:32Z` |
| resources | `apartments-with-dog-parks` | `2026-06-12T09:53:33Z` | `2026-08-28T08:52:23Z` |
| resources | `apartments-with-gyms` | `2026-09-14T22:52:44Z` | `2026-09-16T18:15:01Z` |
| resources | `apartments-with-no-credit-check` | `2026-06-29T20:38:52Z` | `2026-08-26T17:13:40Z` |
| resources | `apartments-with-pools` | `2026-09-14T22:52:44Z` | `2026-09-16T18:10:02Z` |
| resources | `average-rent-for-1-bedroom-apartment` | `2026-09-07T20:44:11Z` | `2026-09-08T17:00:01Z` |
| resources | `banyan-flats` | `2026-08-03T21:39:40Z` | `2026-08-25T16:20:54Z` |
| resources | `best-neighborhoods-in-houston` | `2026-08-24T10:55:42Z` | `2026-08-25T17:10:01Z` |
| resources | `best-neighborhoods-in-philadelphia` | `2026-08-24T11:12:05Z` | `2026-08-28T09:18:42Z` |
| resources | `best-neighborhoods-in-tampa` | `2026-08-24T11:09:29Z` | `2026-08-27T17:25:01Z` |
| resources | `bronx-apartments-for-rent-under-1300` | `2026-05-28T16:26:51Z` | `2026-05-28T19:17:23Z` |
| resources | `brooklyn-neighborhoods` | `2026-08-24T10:22:57Z` | `2026-08-24T21:05:03Z` |
| resources | `camden-copper-square-apartments-phoenix-az` | `2026-06-25T21:15:18Z` | `2026-06-25T21:28:31Z` |
| resources | `cascades-at-northlake-apartments` | `2026-05-07T22:36:32Z` | `2026-07-06T12:27:10Z` |
| resources | `cat-friendly-apartments` | `2026-07-13T10:08:57Z` | `2026-08-24T20:48:01Z` |
| resources | `century-university-city-apartments-charlotte` | `2026-07-20T12:34:49Z` | `2026-09-17T17:43:32Z` |
| resources | `cheap-one-bedroom-apartments` | `2026-07-29T00:01:04Z` | `2026-08-26T17:13:40Z` |
| resources | `cheapest-cost-of-living-states` | `2026-09-07T20:44:10Z` | `2026-09-10T17:00:01Z` |
| resources | `cheapest-places-to-live-in-california` | `2026-08-31T09:16:32Z` | `2026-09-03T17:15:01Z` |
| resources | `city-view-apartments` | `2026-07-27T16:20:59Z` | `2026-07-27T17:25:01Z` |
| resources | `cypress-at-trinity-groves` | `2026-07-29T00:00:58Z` | `2026-08-25T16:36:46Z` |
| resources | `discovery-at-space-coast` | `2026-05-07T22:34:37Z` | `2026-07-06T11:18:54Z` |
| resources | `domain-college-park` | `2026-08-31T09:19:00Z` | `2026-09-17T17:43:31Z` |
| resources | `eastgate-apartments` | `2026-08-11T14:11:37Z` | `2026-08-11T14:21:15Z` |
| resources | `fair-housing-act-guidelines` | `2026-08-24T11:09:37Z` | `2026-08-26T14:11:48Z` |
| resources | `foxcroft-apartments` | `2026-08-17T09:02:55Z` | `2026-08-17T17:15:01Z` |
| resources | `homes-for-rent-no-deposit` | `2026-05-21T10:07:52Z` | `2026-08-28T08:50:45Z` |
| resources | `how-to-get-an-apartment-with-bad-credit` | `2026-05-28T14:48:13Z` | `2026-05-28T19:17:27Z` |
| resources | `income-based-homes-charlotte-nc` | `2026-07-28T18:18:44Z` | `2026-08-26T17:13:40Z` |
| resources | `jack-flats-apartments-melrose` | `2026-05-07T22:33:49Z` | `2026-07-06T11:20:24Z` |
| resources | `las-brisas-apartments-california` | `2026-05-18T09:05:53Z` | `2026-07-06T13:14:27Z` |
| resources | `luxury-home-rentals-phoenix` | `2026-05-21T10:09:14Z` | `2026-07-06T12:39:04Z` |
| resources | `month-to-month-vs-12-month-lease` | `2026-08-03T21:36:42Z` | `2026-08-07T14:50:37Z` |
| resources | `move-in-specials-apartments` | `2026-07-02T10:05:09Z` | `2026-09-17T16:51:25Z` |
| resources | `one-bedroom-apartment-nyc` | `2026-07-20T12:45:31Z` | `2026-09-17T16:51:26Z` |
| resources | `one-bedroom-apartments-bloomington-normal-il` | `2026-06-17T10:24:09Z` | `2026-07-06T12:30:26Z` |
| resources | `panama-city-beach-pet-friendly-rentals` | `2026-05-28T17:18:14Z` | `2026-07-06T12:15:34Z` |
| resources | `parkside-at-legacy-plano` | `2026-05-07T22:38:39Z` | `2026-09-14T10:51:51Z` |
| resources | `pet-deposit-vs-pet-fee` | `2026-07-13T11:06:00Z` | `2026-09-17T17:43:32Z` |
| resources | `pet-friendly-apartments-greenville-sc` | `2026-05-18T09:07:31Z` | `2026-08-24T21:05:03Z` |
| resources | `pet-friendly-vacation-rentals-st-augustine-fl` | `2026-05-18T09:07:31Z` | `2026-08-24T21:05:03Z` |
| resources | `prorated-rent` | `2026-07-07T12:00:15Z` | `2026-08-24T21:03:18Z` |
| resources | `questions-to-ask-when-touring-an-apartment` | `2026-07-20T13:02:22Z` | `2026-08-24T21:03:18Z` |
| resources | `randolph-towers-ballston-arlington-va` | `2026-05-07T22:37:33Z` | `2026-07-06T12:30:26Z` |
| resources | `redstone-ranch-denver` | `2026-07-20T13:10:24Z` | `2026-08-24T21:03:18Z` |
| resources | `rent-affordability-18-an-hour` | `2026-07-13T10:49:29Z` | `2026-08-24T20:48:01Z` |
| resources | `renters-insurance-with-roommates` | `2026-06-16T10:13:54Z` | `2026-08-25T14:59:10Z` |
| resources | `renting-mission-beach-san-diego` | `2026-06-22T17:58:10Z` | `2026-07-06T12:35:24Z` |
| resources | `restaurants-for-lease-near-me` | `2026-05-18T09:08:39Z` | `2026-08-25T14:59:10Z` |
| resources | `rooms-for-rent-huntsville-al` | `2026-05-21T10:10:43Z` | `2026-08-25T14:59:10Z` |
| resources | `short-term-lease-agreement` | `2026-06-11T17:40:09Z` | `2026-08-26T17:13:40Z` |
| resources | `studio-vs-1-bedroom` | `2026-08-31T09:15:28Z` | `2026-09-17T17:43:32Z` |
| resources | `sublet-apartments-nyc` | `2026-06-08T19:14:05Z` | `2026-08-24T20:48:01Z` |
| resources | `the-frances-apartments-madison` | `2026-08-13T09:14:45Z` | `2026-09-17T16:51:26Z` |
| resources | `the-quaye-at-palm-beach-gardens-fl` | `2026-07-02T10:26:40Z` | `2026-07-03T17:10:02Z` |
| resources | `town-center-apartments` | `2026-08-17T09:03:15Z` | `2026-08-19T17:15:01Z` |
| resources | `twin-oaks-apartments` | `2026-08-17T09:03:17Z` | `2026-08-20T17:15:01Z` |
| resources | `university-club-apartments` | `2026-08-03T21:38:41Z` | `2026-08-25T16:20:54Z` |
| resources | `university-village-little-italy-chicago` | `2026-07-07T10:30:19Z` | `2026-07-07T11:15:57Z` |
| resources | `venice-lofts-apartments-philadelphia-pa` | `2026-06-15T20:14:00Z` | `2026-08-24T21:05:03Z` |
| resources | `washer-dryer-in-unit-apartments` | `2026-09-14T22:52:43Z` | `2026-09-14T23:08:51Z` |
| resources | `weston-oaks-apartments-holiday-florida` | `2026-06-23T08:49:41Z` | `2026-07-06T11:28:53Z` |
| resources | `what-does-700-rent-get-you-in-chicago` | `2026-09-07T20:44:11Z` | `2026-09-09T17:00:01Z` |
| resources | `what-does-income-restricted-mean` | `2026-08-13T10:02:55Z` | `2026-08-27T09:19:13Z` |
| resources | `what-happens-when-you-break-a-lease` | `2026-08-31T09:12:30Z` | `2026-09-02T15:39:52Z` |
| resources | `what-is-a-guarantor-on-a-lease` | `2026-08-31T09:14:40Z` | `2026-09-03T14:25:10Z` |
| resources | `what-percentage-of-income-should-go-to-rent` | `2026-08-31T09:18:08Z` | `2026-09-01T17:15:01Z` |
| resources | `whispering-hills-apartments-overland-park-ks` | `2026-09-07T20:44:10Z` | `2026-09-11T17:00:01Z` |

Total rows: 120
