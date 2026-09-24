# QA Patterns

Bootstrapped: 2026-09-16 from all 8 available QA reports. Occurrence counts are
unique report/article IDs, not lines or retries. A fixed historical instance does
not mean the recurring pattern is RESOLVED. No new production run is claimed.
Root causes labeled inferred are hypotheses. Only transition ACTIVE → RESOLVED
with dated evidence of prevention, retaining history. Update an existing pattern
by evidence ID; do not count repeated QA of the same revision as a new occurrence.

Template: Pattern ID; name; first seen; occurrence count; evidence/report IDs;
root cause (observed/inferred); fix; severity; status ACTIVE/RESOLVED; last seen.

## QA-001: Missing Article mainEntityOfPage
- **First seen:** 2026-09-07
- **Last seen:** 2026-09-14
- **Occurrence count:** 8
- **Severity:** failure
- **Root cause:** Schema template omitted canonical linkage (inferred from repeated fixes).
- **Fix:** Add mainEntityOfPage matching canonical URL; retain schema QA.
- **Status:** ACTIVE
- **Evidence:**
  - `QA Reports/apartment-with-terrace-qa.md`
  - `QA Reports/apartments-with-gyms-qa.md`
  - `QA Reports/apartments-with-pools-qa.md`
  - `QA Reports/average-rent-1-bedroom-apartment-qa.md`
  - `QA Reports/cheapest-cost-of-living-states-qa.md`
  - `QA Reports/washer-dryer-in-unit-apartments-qa.md`
  - `QA Reports/what-does-700-rent-get-you-in-chicago-qa.md`
  - `QA Reports/whispering-hills-apartments-qa.md`

## QA-002: External links require verification
- **First seen:** 2026-09-07
- **Last seen:** 2026-09-14
- **Occurrence count:** 8
- **Severity:** warning
- **Root cause:** Historical approved list is not exhaustive.
- **Fix:** Verify official targets and record results; absence from the list alone is not a broken link.
- **Status:** ACTIVE
- **Evidence:**
  - `QA Reports/apartment-with-terrace-qa.md`
  - `QA Reports/apartments-with-gyms-qa.md`
  - `QA Reports/apartments-with-pools-qa.md`
  - `QA Reports/average-rent-1-bedroom-apartment-qa.md`
  - `QA Reports/cheapest-cost-of-living-states-qa.md`
  - `QA Reports/washer-dryer-in-unit-apartments-qa.md`
  - `QA Reports/what-does-700-rent-get-you-in-chicago-qa.md`
  - `QA Reports/whispering-hills-apartments-qa.md`

## QA-003: Opening paragraph over snippet target
- **First seen:** 2026-09-07
- **Last seen:** 2026-09-14
- **Occurrence count:** 3
- **Severity:** failure/warning
- **Root cause:** Opening paragraph not word-counted (inferred).
- **Fix:** Trim to the canonical snippet target without changing sourced facts.
- **Status:** ACTIVE
- **Evidence:**
  - `QA Reports/apartment-with-terrace-qa.md`
  - `QA Reports/apartments-with-pools-qa.md`
  - `QA Reports/what-does-700-rent-get-you-in-chicago-qa.md`

## QA-004: FAQ length outside target
- **First seen:** 2026-09-07
- **Last seen:** 2026-09-14
- **Occurrence count:** 2
- **Severity:** failure/warning
- **Root cause:** Answer length not checked together with schema (inferred).
- **Fix:** Count answers and synchronize body and FAQ schema after trimming.
- **Status:** ACTIVE
- **Evidence:**
  - `QA Reports/average-rent-1-bedroom-apartment-qa.md`
  - `QA Reports/washer-dryer-in-unit-apartments-qa.md`

## QA-005: Banned source named in body
- **First seen:** 2026-09-07
- **Last seen:** 2026-09-07
- **Occurrence count:** 1
- **Severity:** failure
- **Root cause:** Research-source language leaked into published copy (inferred).
- **Fix:** Apply brand-rules.md source policy; independently verify factual claims.
- **Status:** ACTIVE
- **Evidence:**
  - `QA Reports/cheapest-cost-of-living-states-qa.md`

## QA-006: Arithmetic mismatch
- **First seen:** 2026-09-07
- **Last seen:** 2026-09-07
- **Occurrence count:** 1
- **Severity:** failure
- **Root cause:** Cost sum not independently checked (inferred).
- **Fix:** Recalculate all terms; synchronize article and schema.
- **Status:** ACTIVE
- **Evidence:**
  - `QA Reports/what-does-700-rent-get-you-in-chicago-qa.md`

## QA-007: Word-count target set before source research
- **First seen:** 2026-09-24
- **Last seen:** 2026-09-24
- **Occurrence count:** 1
- **Severity:** warning
- **Root cause:** Stage 0 set a generic 1,600-1,900 band before the per-state source
  research existed (observed). The finished body was 2,659 words, 40% over.
- **Fix:** When a brief specifies a per-item research set (states, cities, properties),
  derive the word target from item count times observed item length, not a generic band.
  Ten primary-source state entries averaged ~55 words each with citation.
- **Consequence if missed:** the internal-link requirement in content-standards.md 4.1
  is length-banded, so an under-estimated target silently under-specifies links too.
  This article needed 10-15 links, not the 7 the brief implied.
- **Status:** ACTIVE
- **Evidence:**
  - `QA Reports/security-deposit-return-deadline-qa.md`

## QA-008: External factual claims require primary-source verification
- **First seen:** 2026-09-24
- **Last seen:** 2026-09-24
- **Occurrence count:** 1
- **Severity:** failure (would have been, if unchecked)
- **Root cause:** Aggregator pages and web-search summaries restate statutory figures
  inaccurately (observed). During research a search summary asserted "60 days (Texas)"
  for deposit return. Tex. Prop. Code 92.103, read directly, says 30 days.
- **Fix:** For any statutory, regulatory or numeric claim, fetch the primary source and
  read the figure. Extends QA-002 from link liveness to fact accuracy.
- **Status:** ACTIVE
- **Evidence:**
  - `QA Reports/security-deposit-return-deadline-qa.md`

## QA-009: Output HTML diverges from the live corpus convention
- **First seen:** 2026-09-24
- **Last seen:** 2026-09-24
- **Occurrence count:** 1
- **Severity:** failure
- **Root cause:** FAQ questions were authored as bold markdown, rendering as
  `<p><strong>` (observed). All 86 live Resources bodies contain `<h3>`, and 82 of 86
  use `<h3>` for FAQ questions. The first article on the new output stack had zero.
- **Fix:** Author FAQ questions as `###`. Compare the generated body's tag profile
  against `migration/extract/resources/*.html` before Stage 6 is considered done.
  Corpus norms: h2 7-9, h3 7-11, p 31-51, strong 6-30, em 0-2.
- **Note:** a higher `<a>` count than the corpus (4-11) is expected and not a defect.
  Current ranking-rules require 10-12 internal links plus .gov citations; the older
  articles predate that target.
- **Status:** ACTIVE
- **Evidence:**
  - `QA Reports/security-deposit-return-deadline-qa.md`
