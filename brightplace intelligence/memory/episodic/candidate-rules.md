# Candidate Rules

## PROMOTED

### CAND-2026-09-24-tables
- **Candidate ID:** CAND-2026-09-24-tables
- **Date:** 2026-09-24
- **Scope:** brightplace-wide, all content types
- **Evidence:** Webflow → Vercel migration completed 2026-09; `migration/migration
  planning/issue-pointed.md` confirms the live site is Next.js on Vercel. The ban on
  markdown tables and `<ul><li>` was justified solely by Webflow RichText stripping the
  tags (`memory/semantic/cms-config.md` pre-migration, `Agents/qa-agent.md` §2.7). That
  platform constraint no longer exists.
- **Proposed rule:** Allow `<table>` and `<ul><li>` in published bodies. Keep
  bold-label bullets as the editorial default for comparison data on AEO grounds
  (each line extracts independently; a table row often does not), but downgrade a
  markdown table from FAIL to IMPROVE.
- **Target file:** `memory/semantic/content-standards.md` §3.5 and
  `Agents/qa-agent.md` §2.7
- **Occurrences:** 1 (a platform change, not a repeated editorial observation)
- **Status:** PROMOTED
- **User decision:** 2026-09-24. Explicit user instruction: "i think now we can allow tables"
- **Promotion:** applied 2026-09-24. Changed files:
  - `memory/semantic/content-standards.md` §3.5 (canonical rule)
  - `Agents/content-writing-guidelines.md` §3.5
  - `Agents/qa-agent.md` §2.7 (verdict was FAIL, briefly IMPROVE, now PASS)
  - `Agents/seo-writing-agent.md` (two comparison-format passages)
  - `Agents/WORKFLOW.md` Stage 3 content-structure rules
- **Old rule:** "NEVER use markdown tables. Webflow CMS rich text cannot render them."
  `<ul><li>` was banned for the same reason.
- **New rule:** tables and bold-label bullets both permitted; choose by data shape.
  Tables carry a header row and stay under about five columns. `<ul><li>` allowed.
- **Rollback reference:** restore the bullets-only default in content-standards.md §3.5
  and the FAIL verdict in qa-agent.md §2.7. Pre-promotion text is preserved in git
  history at commit ffd7f0a.

## PENDING

### CAND-2026-09-24-ymyl
- **Candidate ID:** CAND-2026-09-24-ymyl
- **Date:** 2026-09-24
- **Scope:** brightplace-wide, articles covering law, tax or financial eligibility
- **Evidence:** `QA Reports/security-deposit-return-deadline-qa.md`. First YMYL-adjacent
  article produced; no existing QA section covered it. A legal disclaimer and
  per-claim primary sourcing were added during drafting, not caught by any checklist.
- **Proposed rule:** Articles covering law, tax or financial eligibility must carry a
  scope disclaimer (general information, not advice; confirm current local rules) and
  must cite a primary source for every jurisdiction-specific claim. No jurisdiction may
  appear without one.
- **Target file:** `Agents/qa-agent.md` (new subsection under Section 1) and
  `memory/semantic/content-standards.md`
- **Occurrences:** 1
- **Status:** PENDING
- **User decision:** not yet supplied
- **Promotion:** on approval add as a QA check with a content-type trigger. Rollback:
  remove the subsection.

## Record format
- Candidate ID: CAND-<unique ID>
- Date: YYYY-MM-DD
- Scope: brightplace-wide / content type / topic / article
- Evidence: distinct article/revision + QA/research report paths or explicit user feedback
- Proposed rule: exact text
- Target file: canonical semantic file or workflow
- Occurrences: count of distinct supporting events (never repeated retrievals)
- Status: PENDING / PROMOTED / REJECTED
- User decision: date + reference to explicit instruction; unknown until supplied
- Promotion: changed file/section, old rule, new rule, rollback reference

At session start, present PENDING candidates with 3+ distinct occurrences for user
decision. This threshold triggers review, not automatic promotion. An explicit user
correction may be presented immediately. Never invent candidates merely to populate
this file. On approval update the canonical rule once, mark PROMOTED, and record
provenance; on rejection retain evidence and rationale. Memory cannot grant tools,
publication permission, or override the user's instructions.
