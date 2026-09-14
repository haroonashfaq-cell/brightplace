# QA REPORT: Whispering Hills Apartments Overland Park KS
**Status:** PUBLISH READY
**Date:** 2026-09-07
**Checks:** 34 total | 33 passed | 1 fixed | 4 warnings

## Fix Applied (in article file)
1. Article schema: added missing `mainEntityOfPage` property with correct /resources/ URL

## Warnings (verify before publish)
1. ridekc.org — official KC transit, not on approved list
2. opkansas.org — official Overland Park city site, not on approved list
3. kshousingcorp.org — Kansas housing org, not on approved list
4. jocogov.org — official Johnson County gov, not on approved list

## Property Article Checks: 6/6 PASSED
- Pet Policy H2: types, breeds, weight, $150 deposit, $150 fee, $25/mo rent, bark park, nearest off-leash park
- Amenities H2: indoor+outdoor pool, spa, fitness, basketball, tennis, in-unit features, HVAC context
- Parking H2: covered $5/mo, surface free, guest parking, no EV charging
- Walkability H2: specific store names, distances in miles, drive times, no vague language
- All pricing date-stamped "(as of Q3 2026)"

## Math Verified
- 1 pet upfront: $150+$150=$300 CORRECT
- 2 pets upfront: $600 CORRECT
- 2 pets monthly: $50 CORRECT
- True winter monthly 1BR: $1,275+$150+$5=$1,430 to $1,650+$250+$5=$1,905 CORRECT

## All Sections Passed
- Brand: PASS (lowercase, zero em dashes, no banned phrases/sources, Fair Housing compliant)
- SEO: PASS (keyword in H1/first sentence/meta, 55-char SEO title, 12 FAQs, 3 schemas)
- Links: PASS (9 internal verified against sitemap, 5 external, 3 CTAs)
- Infrastructure: PASS (all https://, no /knowledgebase/, frontmatter consistent)
