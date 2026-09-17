# brightplace Intelligence — Agent Memory System Plan

> **Scope:** `brightplace intelligence/` only. No AIR operator, no SUPER SEO Agents.
> **Memory location:** `brightplace intelligence/memory/`
> **Roles:** Claude plans + reviews. Codex implements.
> **Date:** 2026-09-16

---

## Context

The 14 agent files in `brightplace intelligence/Agents/` have four problems:

1. **Massive duplication.** Brand rules are copy-pasted across 4 files: `content-writing-guidelines.md` (Section 1, lines 9-63), `seo-writing-agent.md` (lines 98-146), `qa-agent.md` (lines 24-80), and `.claude/.../MEMORY.md` (lines 23-32). Broken URL lists exist in 3 files: `WORKFLOW.md` (lines 462-506), `master-writer-agent.md` (lines 98-128), and `MEMORY.md` (lines 34-44).

2. **Zero learning.** QA failures repeat because no pattern database exists. Each session starts from scratch. The QA agent finds the same em dash / `<ul><li>` / broken link failures over and over.

3. **No production memory.** Agents can't reference what worked/failed in previous articles. Reddit research is redone from scratch even when the same themes were found before.

4. **Trend intelligence dies with the session.** `master-writer-agent.md` Part 1 Pre-Flight does 3 web searches for current SEO/AEO/GEO trends. Findings are noted for the Teaching Report then lost. The writing agent (Stage 3) reads only STATIC files (`seo-writing-agent.md`, `content-writing-guidelines.md`) with hardcoded rules from specific dates. No mechanism exists for "this is an active trend" vs "this is a permanent rule."

   Current hardcoded trend data in agent files (will go stale):
   - `seo-writing-agent.md` line 67: "comparison tables earn 25.7% more AI citations" (undated)
   - `seo-writing-agent.md` line 81: "83% of AI citations come from pages updated within 12 months" (undated)
   - `seo-writing-agent.md` line 86-89: "Google May 2026 core update rewards pages that cite primary sources" (dated)
   - `seo-writing-agent.md` line 92: "Google retired FAQ rich results on May 7, 2026" (dated)
   - `seo-writing-agent.md` line 285-286: "Information Gain ranking factor re-weighted in March 2026 core update" (dated)
   - `seo-writing-agent.md` line 288-289: "May 2026 AI Overviews Expert Advice block" (dated)
   - `content-writing-guidelines.md` line 207-209: same Information Gain / March 2026 (duplicate)
   - `content-writing-guidelines.md` line 205-206: same Expert Advice / May 2026 (duplicate)

---

## Solution

Add `brightplace intelligence/memory/` with three layers:
- **Semantic** — permanent facts (brand rules, CMS config, links, strategies)
- **Episodic** — production history (QA patterns, content log, corrections, link failures, Reddit patterns, **trend intelligence**)
- **Procedural** — workflow pointer (not a duplicate)

Then slim agent files to reference memory. Then wire agents to read/write memory during production, including trend awareness.

---

## Phase 1: Create Memory Directory + Canonical Files

**Goal:** Single source of truth for all facts. Zero behavior change for agents yet.

### Directory structure

```
brightplace intelligence/
  memory/
    semantic/
      brand-rules.md
      cms-config.md
      link-registry.md
      keyword-strategy.md
      ranking-rules.md
      content-standards.md
    episodic/
      qa-patterns.md
      content-log.md
      corrections.md
      link-failures.md
      reddit-patterns.md
      candidate-rules.md
      trend-intelligence.md        ← NEW (trend memory)
    procedural/
      workflow-reference.md
```

### Files to create (14 new files):

**1. `memory/semantic/brand-rules.md`**
- Extract from: `content-writing-guidelines.md` Section 1 (lines 9-63), `seo-writing-agent.md` (lines 98-146), `qa-agent.md` (lines 24-80), `MEMORY.md` (lines 23-32)
- Contains: ALL zero-tolerance rules — lowercase, em dashes, banned word "signal", banned phrases (full list), banned sources (full list with ILS/review/score/forum categories), title rules, Fair Housing, brightplace identity ("AI-powered rental search tool" not "listing site")
- Format: Each rule has date added and source file
- This becomes the ONLY file where brand rules live

**2. `memory/semantic/cms-config.md`**
- Extract from: `MEMORY.md` (lines 8-16), `WORKFLOW.md` (lines 357-402)
- Contains: Site ID `69d6907887b739e09622100f`, all collection IDs (Resources, Guides, News), Katie Mikles author ID, all category IDs (Top Apartments, Renter Advice, Neighborhood Guides, Renters Corner, Lifestyle, Property, News), field mapping, HTML rules (no `<ul><li>`, no `<script>`, no `<h1>` in post-body, `<ol><li>` OK), DRAFT-only push rule

**3. `memory/semantic/link-registry.md`**
- Extract from: `WORKFLOW.md` (lines 462-506), `master-writer-agent.md` (lines 98-128), `MEMORY.md` (lines 34-44)
- Contains: Sitemap rule, path rules (guides vs resources), known non-existent URLs (4), known broken external URLs with replacements (14 entries from WORKFLOW.md lines 474-493), approved external URLs (6 entries from WORKFLOW.md lines 498-505), known working internal URLs (17 entries from master-writer-agent.md lines 99-117), pages that live under `/guides/` (19 entries)

**4. `memory/semantic/keyword-strategy.md`**
- Extract from: `MEMORY.md` (lines 97-99)
- Contains: DO/DON'T target patterns, intent classification rules, known non-viable keywords

**5. `memory/semantic/ranking-rules.md`**
- Extract from: `MEMORY.md` (lines 64-73), `WORKFLOW.md` (lines 154-158)
- Contains: 7 ranking optimization rules (question-format H2s, entity density, 10+ FAQs, 49-55 word snippet, 7+ internal links, correct intent, content gaps)

**6. `memory/semantic/content-standards.md`**
- Extract from: `content-writing-guidelines.md` (lines 67-300+), `seo-writing-agent.md` AEO section (lines 50-95)
- Contains: Voice/tone, AEO rules (BLUF, self-contained sections 120-180 words, 18-word avg sentences, comparison data format), paragraph rules, sentence rules, date-stamping, anti-AI-detection patterns, E-E-A-T requirements, CTA rules

**7. `memory/episodic/qa-patterns.md`**
- Bootstrap from: Read all QA reports in `brightplace intelligence/QA Reports/` (4 files)
- Format: Pattern ID, pattern name, first seen date, occurrence count, root cause, fix, status (ACTIVE/RESOLVED)

**8. `memory/episodic/content-log.md`**
- Bootstrap from: Git log for brightplace intelligence Complete Articles
- Format: Date, keyword/slug, word count, QA result, key decisions, fixes applied

**9. `memory/episodic/corrections.md`**
- Seed from: Known corrections in MEMORY.md and agent file HTML comments (e.g. `qa-agent.md` line 358, `reddit-research-agent.md` line 94)
- Format: Correction ID, date, context, correction text, scope, files affected

**10. `memory/episodic/link-failures.md`**
- Extract from: `WORKFLOW.md` broken URL tables (lines 462-493)
- Format: URL, date found, source article, replacement URL, status (PERMANENT/FIXED)

**11. `memory/episodic/reddit-patterns.md`**
- Bootstrap from: Read all Reddit research files in `brightplace intelligence/Reddit Research/` (4 files)
- Format: Theme, first seen, articles found in, renter language patterns, pain points

**12. `memory/episodic/candidate-rules.md`**
- Create empty with header template
- Format: Candidate ID, date, evidence, proposed rule, target file, occurrences, status (PENDING/PROMOTED/REJECTED)

**13. `memory/episodic/trend-intelligence.md`** ← NEW

This is the living document for SEO/AEO/GEO trends. It solves the problem of Pre-Flight discoveries dying with the session.

Bootstrap from the hardcoded trend data currently scattered across `seo-writing-agent.md` and `content-writing-guidelines.md`:

```markdown
# Trend Intelligence — SEO/AEO/GEO

Trends are time-sensitive patterns that affect how we write and structure content.
Unlike permanent rules (in semantic/), trends may change as search engines evolve.

## How This File Works
- Pre-Flight (master-writer-agent.md Part 1) READS this file before web searches
- Pre-Flight WRITES new discoveries here after web searches
- Writing Agent (Stage 3) READS active trends before drafting
- QA Agent (Stage 4) CHECKS article against active trend requirements
- Teaching (Part 4) updates trend STATUS based on production results

## Active Trends

### TREND-001: Comparison data citation boost
- **Discovery date:** Pre-September 2026
- **Source:** AEO research
- **Finding:** Pages with 3+ structured comparison sections earn 25.7% more AI citations
- **Impact on writing:** Include at least 1 cost comparison per article using bold-label bullet format
- **Status:** ACTIVE
- **Last verified:** [date of last Pre-Flight check]

### TREND-002: Freshness citation correlation
- **Discovery date:** Pre-September 2026
- **Source:** AEO research
- **Finding:** 83% of AI citations come from pages updated within 12 months
- **Impact on writing:** Date-stamp all figures, include "Last reviewed" footer, set date_modified
- **Status:** ACTIVE
- **Last verified:** [date]

### TREND-003: Google May 2026 core update — outbound authority links
- **Discovery date:** May 2026
- **Source:** Google algorithm update
- **Finding:** Pages citing .gov/.edu primary sources rank higher post-update
- **Impact on writing:** 3-5 outbound .gov/.edu links per article (mandatory)
- **Status:** ACTIVE
- **Last verified:** [date]

### TREND-004: FAQ rich results retired
- **Discovery date:** May 7, 2026
- **Source:** Google Search Console
- **Finding:** Google deprecated FAQ rich results. FAQPage schema still validates but no SERP rich results.
- **Impact on writing:** KEEP writing FAQs and schema (still valuable for AI citation). Remove expectation of rich result lift.
- **Status:** ACTIVE (permanent — schema still helps AEO)
- **Last verified:** [date]

### TREND-005: Information Gain ranking factor
- **Discovery date:** March 2026
- **Source:** Google March 2026 core update
- **Finding:** Re-weighted ranking factor rewards content with genuinely new data not on competing pages
- **Impact on writing:** Every article must include at least 1 unique data point competitors lack
- **Status:** ACTIVE
- **Last verified:** [date]

### TREND-006: AI Overviews Expert Advice block
- **Discovery date:** May 2026
- **Source:** Google AI Overviews update
- **Finding:** New "Expert Advice" block pulls first-hand perspectives with named attribution
- **Impact on writing:** Include "Reviewed by [Name], [Role] at brightplace" in footer
- **Status:** ACTIVE
- **Last verified:** [date]

## Expired Trends
(trends that were active but no longer apply — keep for history)

## Pre-Flight Search Queries
Standard queries to run at the start of each production session:
1. `Google algorithm update [current month] [current year]`
2. `AEO AI overview optimization best practices [current year]`
3. `featured snippet ranking factors [current year]`
4. `Google AI Mode citation patterns [current year]`
5. `GEO generative engine optimization [current year]`
```

**14. `memory/procedural/workflow-reference.md`**
- Short pointer file (NOT a duplicate) pointing to `Agents/WORKFLOW.md`
- Quick reference of the 10 stages

### Phase 1 Validation:
- [ ] All 14 files exist in `brightplace intelligence/memory/`
- [ ] `grep "em dash" memory/semantic/brand-rules.md` returns the rule
- [ ] `grep "em dash" Agents/*.md` STILL returns hits (not yet removed)
- [ ] `trend-intelligence.md` contains all 6 bootstrapped trends
- [ ] No existing agent files modified

---

## Phase 2: Slim Down Agent Files

**Goal:** Agent files reference memory instead of duplicating rules. Measurable line reduction.

### Files to MODIFY (7 files):

**1. `Agents/seo-writing-agent.md` (~554 lines → ~470 lines)**
- **Remove:** Inline brand rules section (lines 98-146, ~50 lines)
- **Remove:** Hardcoded trend data (lines 67-94 AEO stats, lines 285-289 update references) — these are now in `trend-intelligence.md`
- **Add at top:** Memory References section pointing to `memory/semantic/brand-rules.md`, `memory/semantic/content-standards.md`, `memory/semantic/link-registry.md`, `memory/semantic/ranking-rules.md`, `memory/episodic/trend-intelligence.md`
- **Keep:** Writing instructions, AEO structure rules (BLUF, self-contained sections — these are PERMANENT techniques not trends), property template, self-review checklist, schema output format, voice/tone

**2. `Agents/qa-agent.md` (~458 lines → ~380 lines)**
- **Remove:** Inline brand compliance rules (lines 24-80, ~60 lines), inline broken URL lists in Section 5.2 (lines 366-378, ~15 lines)
- **Add at top:** Memory References pointing to `memory/semantic/brand-rules.md`, `memory/semantic/link-registry.md`, `memory/episodic/qa-patterns.md`, `memory/episodic/trend-intelligence.md`
- **Keep:** All 6 QA section structures, Section 2B content quality checks, Section 2C schema validation, property checks, report format

**3. `Agents/content-writing-guidelines.md` (~466 lines → ~400 lines)**
- **Remove:** Entire Section 1 "Brand Rules" (lines 9-63, ~55 lines)
- **Remove:** Duplicated trend references in Section 5 (Information Gain, Expert Advice — lines 205-209)
- **Replace with:** "Brand rules: see `memory/semantic/brand-rules.md`" and "Active trends: see `memory/episodic/trend-intelligence.md`"
- **Keep:** Voice/tone, SEO structure, linking rules, E-E-A-T framework (permanent), writing mechanics, FAQ rules, schema, anti-AI, output format, QA checklist

**4. `Agents/master-writer-agent.md` (~313 lines → ~270 lines)**
- **Remove:** Inline known working links list (lines 98-128, ~30 lines)
- **Modify Part 1 Pre-Flight:** Change from "note in Teaching Report" to "read `memory/episodic/trend-intelligence.md`, run web searches, compare findings, update file with new trends / mark expired trends"
- **Modify Part 4 Teaching:** Rewire from "update agent files directly" to "write candidate rules to `memory/episodic/candidate-rules.md`" AND "update `memory/episodic/trend-intelligence.md` with trend status changes"
- **Add:** Reference to `memory/semantic/link-registry.md`

**5. `Agents/WORKFLOW.md` (~541 lines → ~490 lines)**
- **Remove:** Inline broken URL tables (lines 462-506, ~50 lines), inline approved URLs
- **Replace with:** "See `memory/semantic/link-registry.md` for all URL data"
- **Keep:** All workflow stages, stage descriptions, content types, property workflow

**6. `Agents/brief-check-agent.md` (~286 lines → ~280 lines)**
- **Add:** Memory References for `memory/semantic/brand-rules.md`, `memory/semantic/link-registry.md`, `memory/episodic/trend-intelligence.md`
- **Modify Section 2 (AEO/GEO Validation):** Add "Check brief against active trends in `trend-intelligence.md` — does the brief structure the article for current AI extraction patterns?"
- **Keep:** All 7 review sections

**7. `.claude/projects/.../memory/MEMORY.md` (~100 lines → ~55 lines)**
- **Remove:** Duplicated brand rules, broken URLs, sitemap rules, ranking rules detail
- **Replace with:** Pointers to `brightplace intelligence/memory/semantic/` files
- **Add:** Pointer to `memory/episodic/trend-intelligence.md`
- **Keep:** Workflow overview (shortened), CMS quick reference, QA section count reminder

### Phase 2 Validation:
- [ ] `grep -r "em dash" Agents/*.md` returns ZERO hits (rules now in memory only)
- [ ] `grep -r "memory/semantic" Agents/*.md` returns references in all 6 modified agent files
- [ ] `grep -r "trend-intelligence" Agents/*.md` returns references in seo-writing-agent, qa-agent, master-writer-agent, brief-check-agent, content-writing-guidelines
- [ ] Hardcoded stats ("25.7%", "83%") removed from agent files, present only in `trend-intelligence.md`
- [ ] Total line count across modified files reduced by ~200+ lines

---

## Phase 3: Active Memory (Agents Read/Write During Production)

**Goal:** Agents learn from production, avoid repeating mistakes, and stay current on trends.

### How Trend Intelligence Flows Through Existing Stages

No new stages. The existing workflow stays at 10 stages. The change is making existing stages trend-aware:

```
PRE-FLIGHT (master-writer-agent.md Part 1):
  READS  → memory/episodic/trend-intelligence.md (what we know)
  ACTION → Web searches for latest SEO/AEO/GEO updates
  WRITES → memory/episodic/trend-intelligence.md (new trends, expired trends, updated "Last verified" dates)

STAGE 0 — Content Brief Agent:
  READS  → memory/episodic/trend-intelligence.md
  IMPACT → Structures brief outline for current AI extraction patterns
           (e.g., if TREND-001 is active, brief includes comparison section)

STAGE 2 — Brief Check Agent:
  READS  → memory/episodic/trend-intelligence.md
  IMPACT → Section 2 AEO/GEO validation checks brief against active trends
           (e.g., "does brief include Expert Advice attribution per TREND-006?")

STAGE 3 — SEO Writing Agent:
  READS  → memory/episodic/trend-intelligence.md
  IMPACT → Applies active trends to article structure during drafting
           (e.g., if TREND-005 is active, ensures unique data point is present)

STAGE 4 — QA Agent:
  READS  → memory/episodic/trend-intelligence.md
  IMPACT → Checks article against active trend requirements
           (e.g., "does article have 3+ comparison sections per TREND-001?")

TEACHING (master-writer-agent.md Part 4):
  READS  → memory/episodic/trend-intelligence.md
  WRITES → Updates trend statuses based on production results
           (e.g., "TREND-001 applied, article scored 9/10 on AEO citability — trend confirmed")
```

### Full Workflow Integration Table

| Stage | Agent | Reads from memory/ | Writes to memory/ |
|---|---|---|---|
| Pre-Flight | Master Writer | `episodic/trend-intelligence.md` | `episodic/trend-intelligence.md` (new/expired trends) |
| 0. Brief | Content Brief Agent | `semantic/keyword-strategy.md`, `semantic/link-registry.md`, `episodic/trend-intelligence.md` | — |
| 2. Brief Check | Brief Check Agent | `semantic/brand-rules.md`, `semantic/link-registry.md`, `episodic/qa-patterns.md`, `episodic/trend-intelligence.md` | `episodic/candidate-rules.md` (if new gap found) |
| 2.5. Reddit | Reddit Research Agent | `episodic/reddit-patterns.md` (skip known themes) | `episodic/reddit-patterns.md` (append new only) |
| 3. Writing | SEO Writing Agent | ALL semantic + `episodic/qa-patterns.md` + `episodic/trend-intelligence.md` | — |
| 4. QA | QA Agent | `semantic/brand-rules.md`, `semantic/link-registry.md`, `episodic/qa-patterns.md`, `episodic/trend-intelligence.md` | `episodic/qa-patterns.md`, `episodic/link-failures.md` |
| Teaching | Master Writer | `episodic/trend-intelligence.md` | `episodic/trend-intelligence.md` (status updates), `episodic/content-log.md`, `episodic/candidate-rules.md` |

### Agent File Modifications for Phase 3

**1. `master-writer-agent.md` Part 1 Pre-Flight — Rewrite:**
```
## PART 1: PRE-FLIGHT — Trend Intelligence Scan

Before writing ANY article:

1. Read `memory/episodic/trend-intelligence.md` to know current active trends
2. Run standard Pre-Flight web searches:
   - `Google algorithm update [current month] [current year]`
   - `AEO AI overview optimization best practices [current year]`
   - `featured snippet ranking factors [current year]`
   - `Google AI Mode citation patterns [current year]`
   - `GEO generative engine optimization [current year]`
3. Compare findings against trend-intelligence.md:
   - NEW discovery not in file → Add as new TREND entry with ACTIVE status
   - Existing trend CONTRADICTED by new data → Mark as EXPIRED, add replacement
   - Existing trend CONFIRMED → Update "Last verified" date
   - Nothing new → Proceed with current active trends
4. If any active trend was added or expired, note in Teaching Report
```

**2. `master-writer-agent.md` Part 4 Teaching — Rewrite:**
```
## PART 4: TEACHING — Update Memory (NOT Agent Files)

After scoring and competitor analysis:

### 4A: Trend Status Update
- Read memory/episodic/trend-intelligence.md
- For each active trend: did this article confirm or contradict the trend?
- Update "Last verified" dates for confirmed trends
- If a trend clearly no longer applies, mark EXPIRED with reason

### 4B: Candidate Rules (NOT direct agent file edits)
- If you identified a pattern that would improve future articles:
  → Append to memory/episodic/candidate-rules.md (NOT agent files directly)
  → Include: evidence, proposed rule, target file, date
- Agent files are only updated when user promotes a candidate rule

### 4C: Production Log
- Append to memory/episodic/content-log.md:
  Date, keyword/slug, word count, QA result, trends applied, fixes from qa-patterns.md

### 4D: Teaching Report (output to user — same format as before)
- Add "Trends Applied" section listing which active trends were used
- Add "Trend Status Changes" section listing any new/expired trends
```

**3. `seo-writing-agent.md` — Add "Pre-Write Trend + Pattern Check":**
```
## Pre-Write Memory Check
Before drafting:
1. Read memory/episodic/trend-intelligence.md — apply all ACTIVE trends
2. Read memory/episodic/qa-patterns.md — pre-check outline against top recurring failures
3. If outline would trigger a known QA pattern, fix BEFORE writing
```

**4. `qa-agent.md` — Add Section 2D "Trend Compliance" + Post-QA writes:**
```
## SECTION 2D: TREND COMPLIANCE (applies to "knowledgebase" content type)

Read memory/episodic/trend-intelligence.md. For each ACTIVE trend:
- Check if the article satisfies the trend's "Impact on writing" requirement
- Report: PASS or FAIL per trend, with specific fix if failing

## POST-QA MEMORY WRITE
After completing QA:
1. NEW failure pattern found → Append to memory/episodic/qa-patterns.md
2. Broken URL discovered → Append to memory/episodic/link-failures.md
3. Correction made → Append to memory/episodic/corrections.md
```

**5. `brief-check-agent.md` — Add trend check to Section 2:**
```
## 2f. Active Trend Alignment
Read memory/episodic/trend-intelligence.md.
For each ACTIVE trend, check if the brief structures the article to satisfy it.
- Does brief include comparison section? (TREND-001)
- Does brief plan date stamps on all figures? (TREND-002)
- Does brief identify .gov/.edu authority links? (TREND-003)
- Does brief include Expert Advice attribution? (TREND-006)
Report: PASS or IMPROVE per trend.
```

**6. `reddit-research-agent.md` — Add dedup check:**
```
## Dedup Check
Before searching, read memory/episodic/reddit-patterns.md.
Skip themes already documented with 3+ sources.
Focus research on genuinely new angles.
After research, append ONLY new themes to reddit-patterns.md.
```

**7. Session start behavior — Add to MEMORY.md:**
```
## Session Start
1. Check memory/episodic/candidate-rules.md for PENDING entries with 3+ occurrences
   → Present to user for approval/rejection
2. Check memory/episodic/trend-intelligence.md for trends not verified in 30+ days
   → Flag for re-verification during Pre-Flight
```

### Phase 3 Validation:
- [ ] Produce a test article → verify `content-log.md` grew by 1 entry
- [ ] Produce a test article → verify Teaching Report includes "Trends Applied" section
- [ ] Pre-Flight discovers a new trend → verify `trend-intelligence.md` gets new entry
- [ ] Introduce a deliberate QA failure → verify `qa-patterns.md` gained new entry
- [ ] Run Reddit research on previously-researched topic → verify dedup works
- [ ] Check `candidate-rules.md` → verify pending entries presented at session start
- [ ] QA report includes Section 2D Trend Compliance → verify all active trends checked

---

## The Trend vs Rule Distinction (Key Design Decision)

The current system conflates two things:

| | Permanent Rule | Active Trend |
|---|---|---|
| Example | "brightplace always lowercase" | "comparison tables earn 25.7% more AI citations" |
| Lifespan | Forever | Until search engines change |
| Lives in | `memory/semantic/` | `memory/episodic/trend-intelligence.md` |
| Updated by | User promoting a candidate rule | Pre-Flight scan every session |
| Can expire? | No | Yes |

Currently, both are baked into `seo-writing-agent.md` as static lines. When Google's next core update changes AI citation patterns, the hardcoded "25.7%" stat stays in the agent file forever, potentially causing the writing agent to optimize for an outdated pattern.

With the memory system: Pre-Flight reads trend-intelligence.md, searches for updates, and marks trends EXPIRED when they no longer apply. The writing agent always reads the current active trends, not stale hardcoded stats.

---

## Source File Reference

| File | Location | What Changes |
|---|---|---|
| `content-writing-guidelines.md` | `Agents/` | Loses Section 1 brand rules + duplicated trend refs → memory references |
| `seo-writing-agent.md` | `Agents/` | Loses inline brand rules + hardcoded trend stats → memory references + Pre-Write check |
| `qa-agent.md` | `Agents/` | Loses inline rules + broken URLs, GAINS Section 2D Trend Compliance + Post-QA writes |
| `master-writer-agent.md` | `Agents/` | Part 1 rewired to read/write trend-intelligence.md, Part 4 rewired to candidate-rules + trend updates |
| `WORKFLOW.md` | `Agents/` | Loses URL tables → link-registry.md reference |
| `brief-check-agent.md` | `Agents/` | GAINS Section 2f trend alignment check |
| `reddit-research-agent.md` | `Agents/` | GAINS dedup check against reddit-patterns.md |
| `MEMORY.md` | `.claude/.../memory/` | Becomes pointer file + session start behavior |

---

## Estimated Effort

| Phase | Files Created | Files Modified | Lines Removed | Lines Added |
|---|---|---|---|---|
| Phase 1 | 14 | 0 | 0 | ~500 (extracted + bootstrapped content) |
| Phase 2 | 0 | 7 | ~280 | ~50 (memory references) |
| Phase 3 | 0 | 7 | ~30 (Pre-Flight/Teaching rewrite) | ~100 (memory read/write steps + trend checks) |

---

## Implementation Order for Codex

1. **Phase 1** — Create all 14 memory files. Extract content from source files. Bootstrap trend-intelligence.md with 6 hardcoded trends from agent files.
2. **Phase 2** — Slim agent files. Replace inline rules with memory references. Remove hardcoded trend stats.
3. **Phase 3** — Add read/write behavior. Rewrite Pre-Flight and Teaching. Add trend compliance to QA. Add Pre-Write check to writing agent.

Each phase is independently valuable. Phase 1 alone gives agents a reference library. Phase 2 eliminates duplication. Phase 3 adds learning and trend awareness.

---

## Codex Execution Guide

### Pre-Implementation: Read These Files First

Before writing any code, read these files in order. Each tells you what to extract.

| File to Read | Path | What to Look For |
|---|---|---|
| content-writing-guidelines.md | `brightplace intelligence/Agents/` | Section 1 (lines 9-63) = brand rules to extract. Lines 67-300+ = content standards to extract. Lines 205-209 = duplicated trend data to remove in Phase 2. |
| seo-writing-agent.md | `brightplace intelligence/Agents/` | Lines 50-95 = AEO section with hardcoded trend stats to extract. Lines 98-146 = brand rules to remove. Lines 285-289 = duplicated trend data. Self-review checklist (lines 508-547) = KEEP in agent file. |
| qa-agent.md | `brightplace intelligence/Agents/` | Lines 24-80 = brand compliance rules to extract. Lines 366-378 = broken URL list to extract. Line 358 = HTML comment with correction history. All 6 QA section structures = KEEP. |
| master-writer-agent.md | `brightplace intelligence/Agents/` | Lines 18-35 = Pre-Flight to rewrite. Lines 98-128 = known working links to extract. Lines 219-246 = Teaching section to rewrite. Lines 74-129 = Stage 3 rules (mix of brand rules to extract + writing logic to keep). |
| WORKFLOW.md | `brightplace intelligence/Agents/` | Lines 462-493 = broken URL tables to extract. Lines 497-506 = approved URLs to extract. Lines 154-158 = ranking rules to extract. All stage descriptions = KEEP. |
| brief-check-agent.md | `brightplace intelligence/Agents/` | Section 2 AEO/GEO Validation = add trend check. No major extractions needed. |
| reddit-research-agent.md | `brightplace intelligence/Agents/` | Line 94 = HTML comment with correction history. Add dedup check at top. |
| MEMORY.md | `.claude/projects/-Users-matiullahkhan-Desktop-brightplace/memory/` | Lines 8-16 = CMS config. Lines 23-32 = brand rules (duplicated). Lines 34-44 = link data (duplicated). Lines 64-73 = ranking rules (duplicated). Lines 97-99 = keyword strategy. |
| QA Reports (4 files) | `brightplace intelligence/QA Reports/` | Read all 4, extract recurring failure patterns for qa-patterns.md bootstrap |
| Reddit Research (4 files) | `brightplace intelligence/Reddit Research/` | Read all 4, extract recurring themes for reddit-patterns.md bootstrap |

---

### Key Extract #1: Complete Brand Rules (for `memory/semantic/brand-rules.md`)

Copy these verbatim — this is the canonical set from all 4 source files combined:

```markdown
# Brand Rules — brightplace (Zero Tolerance)

> Source of truth. All agent files reference this instead of embedding rules inline.
> Last updated: 2026-09-16

## Naming
- brightplace is ALWAYS lowercase. Even at the start of a sentence. Even in headings. No exceptions.
- brightplace is an "AI-powered rental search tool" — NEVER say "listing site", "listing platform", "listings", "browse listings"

## Punctuation
- NEVER use em dashes. Not as `--` and not as the unicode character `—`.
- Replace with commas, periods, semicolons, colons, or parentheses.
  - Wrong: "The neighborhood is walkable -- something rare in Texas."
  - Right: "The neighborhood is walkable, something rare in Texas."

## Banned Word
- NEVER use the word "signal" in any form (signal, signals, signaling, signaled).
- Alternatives: "indicator," "suggests," "points to," "reflects."

## Banned Phrases
Never use any of the following:
- "deep dive" / "dive into"
- "navigate" (as metaphor)
- "landscape" (as metaphor)
- "unlock" / "leverage" (as verbs)
- "whether you're X or Y"
- "from X to Y" (as a range framing device)
- "it's worth noting that"
- "it should be mentioned"
- "interestingly" / "notably" / "arguably"
- "hidden gem" / "best-kept secret"
- "vibrant" / "bustling" / "thriving"
- "In this article, we will cover..."
- "Let's take a look at..."
- "Without further ado"
- "In today's [anything]"
- "nestled"
- "boasts"
- "plethora" / "myriad"
- "elevate"
- "tailor" / "tailored"
- "robust"
- "streamline"
- "spearhead"
- "foster"
- "paramount"
- "beacon"
- "tapestry"
- "moreover" / "furthermore"
- "in terms of"
- "at the end of the day"
- "in today's market"

## Title and Heading Rules
- Never use ranking language: no "Top X", "Best", "Ultimate Guide", "#1", "Everything You Need to Know"
- Use curation framing: inform, present options, guide
- SEO title MUST differ from H1 (duplicate triggers site audit warning)
- SEO title must end with ` | brightplace` (pipe separator, not dash)

## Banned Sources (Never Cite or Link To)
**ILS Platforms:** Apartments.com, Zillow, Trulia, Rent.com, Zumper, Apartment List, HotPads, RentCafe, Realtor.com, ForRent.com, Padmapper

**Review Aggregators:** ApartmentRatings, Yelp, Google Reviews (as citation source), Niche, AreaVibes, Crime Grade, Openigloo

**Score Sites:** Walk Score, Bike Score, Transit Score, GreatSchools (as primary citation)

**Forums:** Reddit, City-Data, BiggerPockets

## Fair Housing Compliance
- Never describe neighborhoods by who lives there (race, ethnicity, religion, national origin, familial status, sex, disability, sexual orientation)
- Never include crime statistics, safety ratings, or safety-adjacent language ("safe area", "low crime", "avoid after dark")
- Never use "gentrification" language. Use market dynamics framing instead.
- Describe neighborhoods by lifestyle infrastructure only: walkability, dining, nightlife, transit, parks, grocery, coffee, fitness, coworking, schools (for family content), pet infrastructure (for pet content)
```

---

### Key Extract #2: Complete Broken URL Table (for `memory/semantic/link-registry.md`)

From `WORKFLOW.md` lines 462-506 and `qa-agent.md` lines 350-378:

```markdown
## Known Non-Existent Internal URLs (NEVER link to)
- `/resources/studio-apartments`
- `/resources/pet-friendly-houses-for-rent`
- `/resources/1-bedroom-apartments-near-me`
- `/guides/studio-apartments`

## Known Broken External URLs (use replacement)

| Broken URL | Replacement |
|---|---|
| `consumerfinance.gov/consumer-tools/renting/` | `consumerfinance.gov/housing/housing-insecurity/help-for-renters/` |
| `consumerfinance.gov/housing/renting/` | `consumerfinance.gov/housing/housing-insecurity/help-for-renters/` |
| `consumer.ftc.gov/articles/renting-home` | `consumerfinance.gov/housing/housing-insecurity/help-for-renters/` |
| `ftc.gov/news-events/topics/consumer-protection` | `consumerfinance.gov/housing/housing-insecurity/help-for-renters/` |
| `consumer.ftc.gov/articles/what-know-about-homeowners-renters-insurance` | `consumerfinance.gov/housing/housing-insecurity/help-for-renters/` |
| `azag.gov/consumer/landlord-tenant` | `azag.gov/civil-rights/fair-housing` |
| `dhcd.virginia.gov/landlord-tenant` | `dhcd.virginia.gov/landlord-tenant-resources` |
| `hud.gov/program_offices/comm_planning/affordablehousing/` | `hud.gov/topics/rental_assistance` |
| `sandiego.gov/park-and-recreation/parks/regional/mission-bay` | `sandiego.gov/parks-and-recreation` |
| `sandiego.gov/treasurer/short-term-residential-occupancy-tax` | `sandiego.gov/treasurer/short-term-residential-occupancy` |
| `mecknc.gov/CodeEnforcement/Pages/default.aspx` | `mecknc.gov/luesa/codeenforcement/` |
| `ridetransit.org` | `charlottenc.gov/cats/home/` |
| `hcr.ny.gov/tenant-protection` | `hcr.ny.gov/` |
| `hcr.ny.gov/system/files/documents/2020/11/fact-sheet-07-09-2020.pdf` | `hcr.ny.gov/` |
| `nyc.gov/site/dca/about/about-dca.page` | `nyc.gov/site/dca/` |
| Any `nyc.gov/site/hpd/...` deep link | `nyc.gov/hpd` (deep links return 403) |
| `greenvillerec.com/swamp-rabbit-trail/` | `greenvillerec.com/` |
| `sjcfl.us/Parks/TreatyPark` | `sjcfl.us/Beaches` |
| `redstone.army.mil` | Remove link, keep text (domain dead) |
| `tdhca.texas.gov` | `texas.gov` (domain dead) |
| `texasattorneygeneral.gov/.../renters-rights` | `texas.gov` (domain dead) |
| `trec.texas.gov` | `texas.gov` (domain dead) |
| `scps.k12.fl.us` | `scps.us` (domain moved) |

## Approved External URLs (confirmed working July 2026)
- `hud.gov/topics/rental_assistance`
- `hud.gov/program_offices/fair_housing_equal_opp`
- `consumerfinance.gov/housing/housing-insecurity/help-for-renters/`
- `consumerfinance.gov/consumer-tools/credit-reports-and-scores/`
- `floodsmart.gov`
- `annualcreditreport.com`
- `rentguidelinesboard.cityofnewyork.us/`

## Known Working Internal URLs (from master-writer-agent.md)
- `/resources/how-to-rent-an-apartment`
- `/resources/pet-deposit-vs-pet-fee`
- `/resources/renters-insurance-with-roommates`
- `/resources/short-term-lease-agreement`
- `/resources/move-in-specials-apartments`
- `/resources/apartments-with-no-credit-check`
- `/resources/homes-for-rent-no-deposit`
- `/resources/what-does-income-restricted-mean`
- `/resources/prorated-rent`
- `/resources/cheap-one-bedroom-apartments`
- `/resources/affordable-places-to-live-in-florida`
- `/resources/one-bedroom-apartment-nyc`
- `/resources/sublet-apartments-nyc`
- `/resources/cat-friendly-apartments`
- `/resources/apartments-with-dog-parks`
- `/resources/questions-to-ask-when-touring-an-apartment`
- `/resources/rent-affordability-18-an-hour`
- `/resources/month-to-month-vs-12-month-lease`

## Pages Under /guides/ (NOT /resources/)
your-true-monthly-cost, how-to-rent-an-apartment, brooklyn-neighborhood-guide, denver-city-orientation, phoenix-renters-orientation, austin-young-professionals, dallas-families, houston-city-orientation, charlotte-affordable-neighborhoods, nashville-corporate-relocation-neighborhoods, relocating-to-austin, miami-city-orientation, chicago-pet-owners, huntsville-renters-orientation, knoxville-young-professionals, philadelphia-city-orientation, tampa-renters-orientation, kansas-city-young-professionals, dog-friendly-neighborhoods-san-diego
```

---

### Key Extract #3: CMS Config (for `memory/semantic/cms-config.md`)

```markdown
## Webflow CMS Configuration

**Site ID:** 69d6907887b739e09622100f

### Collections
- **Resources:** `69fcfcef26d35b66ba874f9d` (ALL new content goes here)
- **Guides:** `69dccfeabed64ec697c4f7d2` (RESTRICTED — do not push)
- **News:** `6a32f0722779d53e287b5cc5`

### Author
- **Katie Mikles:** `69dcd70089c4135f7a4158bc` (ALWAYS set as author-2)

### Categories
- Top Apartments: `69df6fa543a7bf3d08de2528` (property-specific articles)
- Renter Advice: `69df6feb55f0f6d5f4e0d20d` (how-to guides, data articles)
- Neighborhood Guides: `69df6ef62355bc3a757acebe` (city/neighborhood content)
- Renters Corner: `6a1852a0e900a98e33e475b2` (Katie interview pieces)
- Lifestyle: `6a0223968011f8b2c9af166e`
- Property: `6a022353abefb2d114e7b04a`
- News: `6a33e903e1454372f37cf6e8`

### Field Mapping
| Markdown Field | CMS Field | Notes |
|---|---|---|
| `title` | `name` | Article title, max 256 chars |
| `slug` | `slug` | URL slug |
| `meta_description` | `meta-description` | Under 160 chars |
| Article title | `seo-title` | Format: [Short Title] \| brightplace, max 60 chars |
| `primary_keyword` | `focus-keyword` | Exact keyword from brief |
| First paragraph (plain text) | `post-summary` | Summary for grid display |
| Article body (HTML) | `post-body` | Rich text, exclude schema blocks |

### HTML Rules (Webflow RichText)
- **NEVER** use `<ul><li>` tags (Webflow strips them — content disappears)
- Convert all lists to `<p><strong>Label:</strong> text</p>` format
- `<ol><li>` is OK for numbered lists only
- No `<h1>` in post-body (Webflow uses `name` field for H1)
- No `<script>` tags (Webflow strips from RichText)
- Push as **DRAFT only** (user adds featured image before publishing)
```

---

### Key Extract #4: 6 Trend Entries (for `memory/episodic/trend-intelligence.md`)

Already fully written in the Phase 1 section above (TREND-001 through TREND-006). Copy that entire block verbatim.

---

### Codex Implementation Checklist

Phase 1:
1. `mkdir -p "brightplace intelligence/memory/semantic"`
2. `mkdir -p "brightplace intelligence/memory/episodic"`
3. `mkdir -p "brightplace intelligence/memory/procedural"`
4. Create `brand-rules.md` using Key Extract #1 above
5. Create `link-registry.md` using Key Extract #2 above
6. Create `cms-config.md` using Key Extract #3 above
7. Create `keyword-strategy.md` — extract from MEMORY.md lines 97-99
8. Create `ranking-rules.md` — extract from MEMORY.md lines 64-73 + WORKFLOW.md lines 154-158
9. Create `content-standards.md` — extract from content-writing-guidelines.md lines 67-300 + seo-writing-agent.md AEO section
10. Create `trend-intelligence.md` using Key Extract #4 (TREND-001 through TREND-006 from plan)
11. Create `qa-patterns.md` — read 4 QA reports in `QA Reports/`, extract failure patterns
12. Create `content-log.md` — read git log for Complete Articles, build log
13. Create `corrections.md` — read HTML comments in qa-agent.md (line 358) and reddit-research-agent.md (line 94)
14. Create `link-failures.md` — subset of link-registry broken URLs with dates
15. Create `reddit-patterns.md` — read 4 Reddit Research files, extract themes
16. Create `candidate-rules.md` — empty with header template
17. Create `workflow-reference.md` — short pointer to WORKFLOW.md
18. Verify: all 14 files exist, no agent files modified

Phase 2:
1. Read each agent file listed in "Files to MODIFY"
2. For each: remove the specified line ranges, add Memory References header
3. For seo-writing-agent.md: also remove hardcoded trend stats (lines 67-94 stats, keep AEO structure rules)
4. For MEMORY.md: replace duplicated sections with pointers
5. Verify: grep tests pass, line counts reduced

Phase 3:
1. Rewrite master-writer-agent.md Part 1 Pre-Flight (use the exact text from Phase 3 section)
2. Rewrite master-writer-agent.md Part 4 Teaching (use the exact text from Phase 3 section)
3. Add Pre-Write Memory Check to seo-writing-agent.md (use exact text from Phase 3)
4. Add Section 2D Trend Compliance to qa-agent.md (use exact text from Phase 3)
5. Add Post-QA Memory Write to qa-agent.md (use exact text from Phase 3)
6. Add Section 2f to brief-check-agent.md (use exact text from Phase 3)
7. Add Dedup Check to reddit-research-agent.md (use exact text from Phase 3)
8. Add Session Start behavior to MEMORY.md (use exact text from Phase 3)
9. Verify: full production smoke test
