# BRIEF CHECK REPORT: how long do landlords have to return security deposit

**Date:** 2026-09-24
**Brief:** `Content Brief/how-long-do-landlords-have-to-return-security-deposit-brief.md`
**Brief Status:** APPROVED

Memory read: `semantic/brand-rules.md`, `semantic/link-registry.md`,
`episodic/qa-patterns.md`, `episodic/trend-intelligence.md`.

---

## 1. Keyword Coverage — PASS

**1a. Primary keyword validation — PASS.**
`how long do landlords have to return security deposit` (1,600/mo, KD 28) matches the
dominant SERP intent. The near-identical `how long does landlord have to return
security deposit` (1,600/mo, KD 18) returns the same SERP and is correctly treated as
one target rather than a second article. The brief explicitly warns against summing
the two volumes, which is right — Google Ads groups close variants.

Not too broad (no ILS competition), not too narrow (1,600/mo with a long tail).

**1b. Secondary keyword gaps — IMPROVE.**
The brief captures the main variants. Three worth adding to the body naturally:
- `security deposit return letter` — high commercial adjacency, and the demand-letter
  section is already planned. Cover the concept; do not build a template (template
  SERPs are a known trap per `keyword-strategy.md`).
- `landlord kept my security deposit` — the emotional phrasing renters actually type.
- `how long after moving out to get deposit back` — natural-language variant that an
  AI Overview is likely to match.

**1c. Entity coverage — PASS.** All nine listed entities are the right ones. Add
**"useful life"** — it is the standard courts apply to carpet and paint deductions and
it is missing from every page-one competitor.

---

## 2. AEO/GEO Validation — PASS

**2a. AI citation readiness — PASS.** An AI Overview occupies rank 1. The structure is
built for extraction: question H2s, answer-first leads, one self-contained answer per
state tier, 10+ standalone FAQ pairs.

**2b. Extractable definitions — PASS.** Security deposit, normal wear and tear,
forwarding address, itemized statement and useful life all get definition treatment.

**2c. Proof specificity — STRONG PASS.** This is the brief's best feature. Ten states
with statute citations, exact day counts, exact penalty multipliers, exact dollar
thresholds (California's $125 receipt rule), exact sub-deadlines (Michigan's 4-day
address and 7-day dispute windows). Nothing here is vague.

---

## 3. SERP Intent Match — PASS

Format matches: every ranking page is explanatory prose with statutory detail. No
listings, no tools, no templates.

**The gate that matters:** zero ILS platforms in the top 10. The failure recorded in
`brightplace-serp-intent-rule` — five Resources pages losing all top-100 keywords
because they targeted listing intent — does not apply to this keyword. Checked live
2026-09-24, not inferred.

**PAA coverage — PASS.** A People Also Ask block sits at rank 3. The planned H2s and
FAQ set cover the predictable questions (clock start, allowable deductions, what to do
when it is late, whether the landlord can keep it all).

---

## 4. Brand & Compliance — PASS with one correction

- **Title framing — PASS.** "How Long Does a Landlord Have to Return Your Security
  Deposit?" carries no ranking language, no "Ultimate", no "Top". SEO title differs
  from H1 and ends ` | brightplace`. Both correct.
- **CTA targets — PASS.** All three use `https://www.brightplace.ai` or
  `/search`. No `app.brightplace.ai` anywhere. This is the first brief written under
  the merged-domain rule and it applies it correctly.
- **Internal link targets — PASS.** Twelve targets, all verified live in
  `/sitemaps/content.xml` on 2026-09-24. The brief flags the `/guides/` vs
  `/resources/` split for `how-to-rent-an-apartment` and `your-true-monthly-cost`,
  which is the exact mistake `link-registry.md` warns about.
- **Banned sources — PASS.** Brief explicitly excludes Zillow and Apartments.com even
  though both rank for the adjacent "how much is a security deposit" query.

**CORRECTION REQUIRED:** the brief lists Michigan Legal Help (`michiganlegalhelp.org`)
inside the verified-source block. It is a `.org` legal-aid site, not a `.gov` primary
source. The brief already notes this, but the writing agent must not count it toward
the TREND-003 `.gov` requirement. Nine genuine `.gov` sources remain, which clears the
3–5 minimum comfortably.

---

## 5. Competitive Depth — PASS

Ten competitor pages analysed from the live SERP. The differentiation is not a claim,
it is structural: **no page-one result covers more than one state.** A renter moving
between states cannot be served by any of them.

Five specific gaps identified, each verifiable:
1. Multi-state coverage at all
2. Calendar days vs business days (Arizona)
3. The forwarding-address precondition (TX, OH, MI)
4. Florida's split 15/30 timeline and 15-day objection window
5. Penalty multipliers side by side (1× to 3×)

Items 2 and 3 are the strongest. Both decide real cases and neither is explained
anywhere on page one.

---

## 6. Independent Research — PASS, with a warning

**Warning worth recording.** During research, a web-search summary asserted
"60 days (Texas)" and "14 days (Alabama)" for deposit return. The Texas figure is
**wrong** — Tex. Prop. Code §92.103, read directly, says 30 days. Aggregator and
search-summary data for this topic is unreliable. The brief's rule — no state appears
without a fetched primary source — is not bureaucratic caution here, it is load-bearing.

This is new evidence for `QA-002` (external links require verification), extended:
external *facts* require verification too, not just URLs.

**Topical authority fit — STRONG.** brightplace already ranks 5–8 across a wide
no-deposit long-tail (`homes-for-rent-no-deposit`) and has `pet-deposit-vs-pet-fee`
live, but owns nothing on security deposits themselves. This is a pillar gap inside a
cluster where Google already trusts the domain.

---

## Improvements to make during drafting

1. Add `useful life` as a defined entity in the deductions section.
2. Work in `landlord kept my security deposit` and `how long after moving out to get
   deposit back` as natural body phrasings.
3. Do not count `michiganlegalhelp.org` toward the `.gov` link requirement.
4. State the six-of-ten figure for 30 days. Never the unverified "22 states".
5. Add an explicit line telling readers to confirm against their own state's current
   statute — YMYL requirement, and no competitor's single-state page needs it.

---

## Verdict

**APPROVED — proceed to Stage 2.5.**

Strongest brief in the set on proof specificity. The SERP gate passes on live evidence,
the gap is structural rather than asserted, and every number traces to a statute. The
one correction (Michigan's `.org` status) is minor and already half-flagged.
