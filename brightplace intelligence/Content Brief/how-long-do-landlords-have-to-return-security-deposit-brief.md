# Content Brief: How Long Do Landlords Have to Return a Security Deposit?

**Created:** 2026-09-24
**Stage:** 0 (Content Brief Agent)
**Collection:** Resources
**Slug:** `security-deposit-return-deadline`
**Content type:** knowledgebase

---

## 1. Keyword Targeting

**Primary keyword:** `how long do landlords have to return security deposit`
- Search volume: 1,600/mo (US, en)
- Keyword difficulty: 28
- Intent: informational

**Near-duplicate variant (same SERP, treat as one target):**
- `how long does landlord have to return security deposit` — 1,600/mo, KD 18

**Secondary keywords:**
| Keyword | Volume | KD |
|---|---|---|
| `can you get security deposit back` | 880 | 15 |
| `do you get a security deposit back` | 880 | 7 |
| `security deposit return` | — | — |
| `how long to get security deposit back` | — | — |
| `landlord not returning security deposit` | — | — |

Source: OpenSEO `research_keywords`, 2026-09-24, seed `security deposit`, US/en.
Do not sum variant volumes — 1,600 appears against both phrasings and may be shared.

**Entities to cover:** security deposit, itemized statement, normal wear and tear,
forwarding address, small claims court, statutory damages, move-out inspection,
deposit cap, business days vs calendar days.

---

## 2. SERP Evidence and Intent Classification

**Checked:** 2026-09-24, live, via OpenSEO `get_serp_results`, depth 10, US/en.

**Classification: ARTICLE / GUIDE — proceed.**

Top 10 for the primary keyword:

1. AI Overview
2. `selfhelp.courts.ca.gov` — Guide to security deposits in California
3. People Also Ask
4. `ohiobar.org` — Ohio Law Gives Tenants Security Deposit Rights
5. `guides.sll.texas.gov` — Security Deposits
6. `peoples-law.org` — Security Deposits (Maryland)
7. `rentguidelinesboard.cityofnewyork.us` — Security Deposits FAQs
8. `lawhelpnc.org` — Housing: Your Security Deposit
9. `lawhelp.colorado.gov` — Security Deposits
10. `michiganlegalhelp.org` — Your Security Deposit

**Why this passes the SERP intent gate:**
- **Zero ILS platforms.** No Apartments.com, Zillow, Zumper, Rentable, StreetEasy.
  This is not a listing-intent query, so the failure mode recorded in
  `brightplace-serp-intent-rule` does not apply.
- Every organic result is a **single-state** legal-aid or court page.
- **No national publisher ranks at all.** Not one result covers more than one state.

**Content-farm note:** a plain web search for this topic surfaces
`depositdeadline.com`, `claimsmaximizer.com`, `rentlatefee.com`, `gettenantshield.com`
and similar, all claiming 50-state coverage. **None of them appear in the live SERP.**
Google is currently choosing primary-source legal pages over aggregators. The
opportunity is a multi-state answer with primary-source citations, not another
aggregator table.

---

## 3. The Content Gap (this is the whole thesis)

A renter who just moved out of Texas and is moving to California cannot answer
"when do I get my money back" from any single page on page one. They get a Texas page
or a California page, never both, and never the comparison.

**What no competitor on page 1 has:**
1. More than one state on the page.
2. The calendar-days vs business-days distinction (Arizona counts business days;
   nearly everyone else counts calendar days). Getting this wrong costs a renter
   roughly four days of standing.
3. The forwarding-address precondition. In Texas, Ohio and Michigan the clock does
   not start, or the tenant forfeits damages entirely, without a written address.
   This is the single most common reason a renter loses a deposit claim they should win.
4. Florida's split timeline (15 days with no deductions, 30 days to notice a claim)
   and its 15-day tenant objection window.
5. Penalty multipliers side by side — they range from 1× to 3× and change whether
   small claims is worth filing.

---

## 4. Article Specification

**H1:** How Long Does a Landlord Have to Return Your Security Deposit?
**SEO title:** Security Deposit Return Deadlines by State | brightplace
**Meta description:** How long does a landlord have to return a security deposit? Deadlines run 14 to 30 days depending on your state. Verified rules for 10 states, plus what to do if yours is late.
**Word count target:** 1,600–1,900
**Internal links:** 10–12 (per content-standards 4.1 for this length)
**External authority links:** 8–10, all `.gov` primary sources
**FAQ pairs:** 10+, 40–60 words each

### Required structure (all H2s question-format, answer-first in 40–60 words)

1. **How Long Does a Landlord Have to Return Your Security Deposit?**
   Lead: the range and the most common figure. 49–55 word opener under the H1.
2. **What Is the Security Deposit Return Deadline in Your State?**
   The verified 10, grouped by deadline tier using bold-label bullets.
3. **When Does the Clock Actually Start?**
   Move-out vs surrender of possession vs receipt of forwarding address.
4. **What Is a Forwarding Address and Why Does It Decide Your Case?**
   The precondition renters miss. Ohio: no address, no damages, full stop.
5. **What Can a Landlord Legally Deduct?**
   Normal wear and tear vs damage. Itemization and receipt thresholds.
6. **What Happens If a Landlord Misses the Deadline?**
   Penalty multipliers by state, 1× to 3×.
7. **How Do You Get Your Security Deposit Back If the Landlord Will Not Pay?**
   Demand letter, then small claims. Practical sequence.
8. **How Can You Protect Your Deposit Before You Move Out?**
   Documentation, walkthrough, written address.
9. **Frequently Asked Questions** (10+ pairs)

### Comparison requirement (TREND-001)

One structured comparison, **bold-label bullet format**, not a table.
`CAND-2026-09-24-tables` is PENDING and unpromoted, so the bold-label rule stands.
Grouping the states by deadline tier is also better for extraction than 50 rows:
each tier is an independently liftable answer.

---

## 5. Verified Source Data (10 states, primary sources, checked 2026-09-24)

Every figure below was fetched from the cited source on 2026-09-24. **Do not add a
state to the article that is not on this list.** Illinois and Georgia were attempted
and returned 404; they are deliberately excluded rather than guessed.

**14 days**
- **New York** — 14 days, itemized statement required. Deposit capped at one month's
  rent. Willful violation: punitive damages up to 2× the deposit.
  `https://www.nysenate.gov/legislation/laws/GOB/7-108` (NY Gen. Oblig. Law §7-108)

**14 business days**
- **Arizona** — 14 days *excluding Saturdays, Sundays and legal holidays*, after
  termination, delivery of possession **and tenant demand**. Deposit capped at 1.5×
  monthly rent. Penalty: 2× the amount wrongfully withheld.
  `https://www.azleg.gov/ars/33/01321.htm` (A.R.S. §33-1321)

**15 / 30 days (split)**
- **Florida** — 15 days to return if the landlord makes no claim; 30 days to send
  written notice of intent to impose a claim. Tenant then has 15 days to object in
  writing.
  `https://www.flsenate.gov/Laws/Statutes/2023/83.49` (Fla. Stat. §83.49)

**21 days**
- **California** — 21 days to return the deposit or return it with an itemized
  statement. Deductions over $125 require attached invoices or receipts. Bad-faith
  retention: up to 2× the deposit in damages, on top of the deposit.
  `https://selfhelp.courts.ca.gov/guide-security-deposits-california` (Cal. Civ. Code §1950.5)

**30 days**
- **Texas** — 30 days after the tenant surrenders the premises. §92.107: the landlord
  is not obliged to refund or itemize until the tenant gives a **written forwarding
  address**. Bad faith: **3×** the portion wrongfully withheld plus fees.
  `https://guides.sll.texas.gov/landlord-tenant-law/security-deposits` (Tex. Prop. Code §§92.103, 92.107, 92.109)
- **Ohio** — 30 days after termination and delivery of possession. Tenant **must**
  provide a written forwarding address; if they do not, "the tenant shall not be
  entitled to damages or attorneys fees." Damages: the amount wrongfully withheld
  plus reasonable attorney's fees.
  `https://codes.ohio.gov/ohio-revised-code/section-5321.16` (Ohio Rev. Code §5321.16)
- **Washington** — 30 days after termination of the rental agreement and vacation.
  Non-compliance: liable for the full deposit; court may award up to 2× for
  intentional refusal, plus costs and attorney's fees.
  `https://app.leg.wa.gov/RCW/default.aspx?cite=59.18.280` (RCW 59.18.280)
- **Massachusetts** — 30 days after termination of occupancy. Itemized list must be
  sworn under penalty of perjury with written evidence attached. Failure: **3×** the
  deposit plus 5% interest and attorney's fees.
  `https://malegislature.gov/Laws/GeneralLaws/PartII/TitleI/Chapter186/Section15B` (M.G.L. c.186 §15B)
- **North Carolina** — 30 days. If damages cannot be determined in time, an interim
  accounting at 30 days and a **final accounting within 60 days**.
  `https://www.ncleg.gov/EnactedLegislation/Statutes/HTML/BySection/Chapter_42/GS_42-52.html` (N.C.G.S. §42-52)
- **Michigan** — 30 days after receiving the forwarding address. Deposit capped at
  1.5× monthly rent. Tenant must give a written address within **4 days** of moving
  out and has **7 days** to dispute a damage claim. Penalty: 2× the deposit.
  `https://www.michiganlegalhelp.org/resources/housing/your-security-deposit-what-it-and-how-get-it-back`
  (Michigan Legal Help — `.org`, not `.gov`; use as supporting, not primary authority)

**Defensible summary claim:** six of the ten verified states use 30 days. Do **not**
write "22 states use 30 days" — that figure came from an aggregator and is unverified.

---

## 6. Internal Link Targets (verified against live sitemap 2026-09-24)

All confirmed present in `https://www.brightplace.ai/sitemaps/content.xml`.

| Path | Anchor context |
|---|---|
| `/resources/homes-for-rent-no-deposit` | alternatives to a traditional deposit |
| `/resources/pet-deposit-vs-pet-fee` | refundable vs non-refundable money |
| `/guides/your-true-monthly-cost` | what renters actually pay upfront |
| `/guides/how-to-rent-an-apartment` | the overall renting process |
| `/resources/what-happens-when-you-break-a-lease` | early termination and deposits |
| `/resources/questions-to-ask-when-touring-an-apartment` | what to ask before signing |
| `/resources/apartment-checklist-first-apartment` | move-in documentation |
| `/resources/prorated-rent` | partial-month money at move-out |
| `/resources/month-to-month-vs-12-month-lease` | lease term and termination |
| `/resources/short-term-lease-agreement` | shorter tenancies |
| `/resources/what-is-a-guarantor-on-a-lease` | cosigners and liability |
| `/resources/move-in-specials-apartments` | move-in cost offsets |

⚠️ `how-to-rent-an-apartment` and `your-true-monthly-cost` are under **`/guides/`**,
not `/resources/`. Confirmed in the sitemap. Getting this wrong produces a 404.

---

## 7. CTA Plan

Three CTAs, per content-standards. **One domain only** — `app.brightplace.ai` is
merged into the main site and must never appear.

1. After first H2 → `https://www.brightplace.ai/search`
2. Mid-article → `https://www.brightplace.ai`
3. End of article → `https://www.brightplace.ai/search`

Informational framing only. No "sign up", no urgency, no superlatives.

---

## 8. Trends Applied

- **TREND-001** (comparison data): one structured comparison, bold-label bullets. APPLIED.
- **TREND-002** (freshness): every figure date-stamped "(as of Q3 2026)", `last_reviewed`
  set, `date_modified` set. APPLIED.
- **TREND-003** (.gov/.edu outbound): 9 `.gov` primary sources available, well over the
  3–5 minimum. APPLIED.
- **TREND-004** (FAQ rich results retired): FAQPage schema still emitted for AEO
  extraction, not for rich-result display. APPLIED, no change to output.

All four verified 2026-09-16, inside the 30-day eligibility window.

---

## 9. Compliance Notes

- **YMYL-adjacent.** This is legal information. Every figure must trace to a cited
  primary source. No state may appear without one. Include a line telling readers to
  confirm against their own state's current statute.
- Brand rules: lowercase brightplace, no em dashes, no "signal", no banned phrases.
- Fair Housing: not applicable to this topic, but no demographic framing anywhere.
- Banned sources: do **not** cite Zillow or Apartments.com even though both rank for
  the adjacent "how much is a security deposit" query. Reddit informs voice only.

---

## 10. Verdict

**PROCEED.** Article intent confirmed, gap is real and specific, source data verified
from 10 primary sources, internal and external link targets confirmed live.
