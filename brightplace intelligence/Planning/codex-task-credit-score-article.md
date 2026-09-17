# Codex Task: First Article with Memory System

**Keyword:** `what credit score do you need to rent an apartment`
**Purpose:** End-to-end test of the new memory system with a real article production run
**Date:** 2026-09-16

---

## Context

This is the first article produced with the new memory system. The memory system was just implemented (see `brightplace intelligence/Planning/memory-system-implementation.md`). This run tests that agents actually read/write memory during production.

---

## What To Do

Follow `brightplace intelligence/Agents/WORKFLOW.md` exactly. The workflow now includes memory reads/writes at every stage. Here's the full sequence:

### SESSION START (new — from memory system)
1. Check `memory/episodic/candidate-rules.md` for PENDING entries with 3+ occurrences → present to user (likely empty on first run)
2. Check `memory/episodic/trend-intelligence.md` for trends needing verification → flag for Pre-Flight

### PRE-FLIGHT (master-writer-agent.md Part 1 — updated)
1. Read `memory/episodic/trend-intelligence.md` — all 6 trends are UNVERIFIED
2. Run 5 web searches for current SEO/AEO/GEO updates
3. Compare findings against the 6 imported trends
4. Update each trend to ACTIVE (verified), EXPIRED, or leave UNVERIFIED with notes
5. Add any NEW trends discovered

### STAGE 0: Content Brief Agent
- Keyword: `what credit score do you need to rent an apartment`
- Hit DataForSEO API for live SERP data
- Read `memory/semantic/keyword-strategy.md` and `memory/semantic/link-registry.md`
- Read `memory/episodic/trend-intelligence.md` — structure brief for current AI patterns
- Output brief to `brightplace intelligence/Content Brief/what-credit-score-to-rent-apartment-brief.md`

### STAGE 2: Brief Check
- Run all 7 sections of brief-check-agent.md
- Run new Section 2f Active Trend Alignment (checks brief against active trends)
- Read `memory/episodic/qa-patterns.md` for recurring gaps
- If new gap found → append to `memory/episodic/candidate-rules.md`

### STAGE 2.5: Reddit Research
- Read `memory/episodic/reddit-patterns.md` FIRST (dedup check)
- Search Reddit for real renter discussions about credit scores and renting
- Append ONLY new themes to `memory/episodic/reddit-patterns.md`
- Output report to `brightplace intelligence/Reddit Research/what-credit-score-to-rent-apartment-reddit-research.md`

### STAGE 3: Writing
- Read ALL `memory/semantic/` files + `memory/episodic/qa-patterns.md` + `memory/episodic/trend-intelligence.md`
- Pre-Write Memory Check: apply active trends, pre-check against QA patterns
- Draft article following all rules
- Key cross-links available (from sitemap):
  - `/resources/how-to-get-an-apartment-with-bad-credit`
  - `/resources/apartments-with-no-credit-check`
  - `/resources/rent-affordability-18-an-hour`
  - `/resources/what-percentage-of-income-should-go-to-rent`
  - `/resources/what-is-a-guarantor-on-a-lease`
  - `/resources/renters-insurance-with-roommates`
  - `/guides/how-to-rent-an-apartment`
  - `/guides/your-true-monthly-cost`
- Output to `brightplace intelligence/Complete Articles/what-credit-score-to-rent-apartment.md`

### STAGE 4: QA
- Run ALL 6 sections + Section 2D Trend Compliance
- Post-QA Memory Write:
  - New failure patterns → append to `memory/episodic/qa-patterns.md`
  - Broken URLs → append to `memory/episodic/link-failures.md`
  - Corrections → append to `memory/episodic/corrections.md`
- Output report to `brightplace intelligence/QA Reports/what-credit-score-to-rent-apartment-qa.md`

### STAGE 5: Image Generation
- Generate 3 image prompt options using blog-image-prompts.md
- Run `generate-image.py` with Prompt A

### STAGE 5.5: HTML Generation
- Convert to production-ready HTML

### STAGE 6: Webflow CMS Push
- Push as DRAFT to Resources collection
- DO NOT publish

### TEACHING (master-writer-agent.md Part 4 — updated)
- Update trend statuses in `memory/episodic/trend-intelligence.md`
- Append to `memory/episodic/content-log.md` with date, keyword, word count, QA result, trends applied
- Write candidate rules to `memory/episodic/candidate-rules.md` if warranted
- Output Teaching Report with "Trends Applied" and "Trend Status Changes" sections

### DO NOT commit to git. User will review first.

---

## SERP Data (from DataForSEO, live as of 2026-09-16)

- AI Overview: PRESENT
- #2: Experian — "What Credit Score Do You Need to Rent an Apartment?"
- #5: Reddit r/movingtoNYC — real renter discussion
- #6: Zillow (competitor — beatable, and we can't link to them)
- #7: Small property management blog
- PAA questions:
  - "What is a minimum credit score for renting an apartment?"
  - "Can I afford $1000 rent making $20 an hour?"
  - "Can I lease with a 500 credit score?"

---

## What Claude Will Review After

1. Were memory files actually updated? (content-log, trend-intelligence, possibly qa-patterns, reddit-patterns)
2. Did Pre-Flight verify the 6 UNVERIFIED trends?
3. Does QA report include Section 2D Trend Compliance?
4. Does Teaching Report include "Trends Applied" section?
5. Article quality: brand compliance, AEO structure, cross-linking, FAQ count
6. Brief quality: DataForSEO data, PAA coverage, competitor analysis
