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
