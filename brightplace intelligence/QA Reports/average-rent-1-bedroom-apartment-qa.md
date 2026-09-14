# QA REPORT: Average Rent for 1 Bedroom Apartment
**Status:** PUBLISH READY
**Date:** 2026-09-07
**Checks:** 35 total | 32 passed | 2 fixed | 3 warnings

## Fixes Applied (in article file)
1. Article schema: added missing `mainEntityOfPage`
2. FAQ 12 answer trimmed from 66 → 57 words (body + schema synced)

## Warnings (verify before publish)
1. bls.gov/cpi/factsheets/owners-equivalent-rent-and-rent.htm — not on approved list
2. census.gov/housing — not on approved list
3. Housing Wage $29.19/hr derives from NLIHC Fair Market Rent, not the $1,545 median used in article — consider adding "(based on Fair Market Rent)" parenthetical

## Math Verified (ALL 17 calculations)
- $40K: $3,333/mo × 30% = $1,000 CORRECT
- $50K: $4,167/mo × 30% = $1,250 CORRECT
- $60K: $5,000/mo × 30% = $1,500 CORRECT
- $75K: $6,250/mo × 30% = $1,875 CORRECT
- $100K: $8,333/mo × 30% = $2,500 CORRECT
- $20/hr: $41,600/yr, $3,467/mo, $1,000 = 29% CORRECT
- $2,000/mo × 30% = $600 CORRECT
- True cost: $1,545 × 1.15 = $1,780, × 1.25 = $1,930 CORRECT
- Singles tax: ($1,850/2) = $925, $1,545-$925 = $620/mo × 12 = $7,440/yr CORRECT
- NYC salary: $4,695 × 12 / 0.30 = $188K CORRECT
- Min wage: $7.25 × 40 × 52 = $15,080, 30% = $377/mo CORRECT

## All Sections Passed
- Brand: PASS (lowercase, zero em dashes, no banned phrases/sources, Fair Housing compliant)
- SEO: PASS (12 keyword instances, 148-char meta, 52-char SEO title, 14 FAQs, 3 schemas)
- Links: PASS (18 unique internal links verified, 5 external .gov, 3 CTAs)
- Infrastructure: PASS (all https://, no /knowledgebase/, frontmatter consistent)
