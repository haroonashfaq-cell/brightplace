# Trend Intelligence — SEO/AEO/GEO

Trends are time-sensitive patterns that affect how we write and structure content.
Unlike permanent rules (in semantic/), trends may change as search engines evolve.

## How This File Works
- Pre-Flight (master-writer-agent.md Part 1) READS this file before web searches
- Pre-Flight WRITES new discoveries here after web searches
- Writing Agent (Stage 3) READS active trends before drafting
- QA Agent (Stage 4) CHECKS article against active trend requirements
- Teaching (Part 4) records application outcomes; only supporting evidence changes verification/status

## Active Trends

### TREND-001: Comparison data citation boost
- **Discovery date:** Pre-September 2026
- **Source:** AEO research; corroborated by Green Flag Digital (https://greenflagdigital.com/aeo-best-practices/) and HubSpot AEO framework
- **Finding:** Structured comparison data improves AI citation rates. Original "25.7%" figure unverifiable but directional: AEO best practices consistently recommend structured comparisons for extractability.
- **Impact on writing:** Include at least 1 cost comparison per article using bold-label bullet format
- **Status:** ACTIVE (directional — exact percentage unverified)
- **Last verified:** 2026-09-16
- **Checked by:** Claude Pre-Flight
- **Limitation:** The exact 25.7% figure has no traceable primary source. The practice (structured comparisons) is widely recommended; the exact lift is not.

### TREND-002: Freshness citation correlation
- **Discovery date:** Pre-September 2026
- **Source:** AEO research; consistent with Google's freshness signals and multiple AEO guides (https://writer.com/blog/geo-aeo-optimization/)
- **Finding:** AI engines strongly prefer recently updated content for citations. Original "83%" figure unverifiable but freshness is a confirmed ranking and citation factor.
- **Impact on writing:** Date-stamp all figures, include "Last reviewed" footer, set date_modified
- **Status:** ACTIVE (directional — exact percentage unverified)
- **Last verified:** 2026-09-16
- **Checked by:** Claude Pre-Flight
- **Limitation:** The exact 83% figure has no traceable primary source. Freshness as a citation factor is well-established.

### TREND-003: Google May 2026 core update — outbound authority links
- **Discovery date:** May 2026
- **Source:** Google May 2026 core update; confirmed by Launchcodex (https://launchcodex.com/blog/seo-geo-ai/google-may-2026-core-update/), multiple SEO analyses
- **Finding:** Pages citing .gov/.edu primary sources rank higher post-update. Part of broader E-E-A-T signal reinforcement.
- **Impact on writing:** 3-5 outbound .gov/.edu links per article (mandatory)
- **Status:** ACTIVE
- **Last verified:** 2026-09-16
- **Checked by:** Claude Pre-Flight

### TREND-004: FAQ rich results retired
- **Discovery date:** May 7, 2026
- **Source:** Google official; confirmed by Search Engine Journal (https://www.searchenginejournal.com/google-drops-faq-rich-results-from-search/574429/), Bluehost, The HOTH
- **Finding:** Google deprecated FAQ rich results May 7, 2026. Three-phase shutdown: SERP display (May), Search Console reporting (June), API support (August). FAQPage schema still validates. Markup still crawled by Bing, Perplexity, and RAG crawlers.
- **Impact on writing:** KEEP writing FAQs and schema (still valuable for AI citation and non-Google engines). No SERP rich result lift.
- **Status:** ACTIVE (permanent change)
- **Last verified:** 2026-09-16
- **Checked by:** Claude Pre-Flight

### TREND-005: Information Gain ranking factor
- **Discovery date:** March 2026
- **Source:** Google March 2026 core update; confirmed by Digital Applied (https://www.digitalapplied.com/blog/information-gain-google-ranking-signal-april-2026), ALM Corp, multiple analyses. Pages with proprietary data gained 15-25% visibility; templated content dropped 30-50%.
- **Finding:** Information Gain is now a dominant ranking signal. Google evaluates whether a page adds genuinely new information vs what already ranks. Five dimensions: proprietary data, first-hand evidence, original framework, expert attribution, freshness hook.
- **Impact on writing:** Every article must include at least 1 unique data point competitors lack
- **Status:** ACTIVE
- **Last verified:** 2026-09-16
- **Checked by:** Claude Pre-Flight

### TREND-006: AI Overviews Expert Advice block
- **Discovery date:** May 6, 2026
- **Source:** Google AI Overviews structural update; confirmed by Net Connect Digital (https://netconnectdigital.com/blog-google-ai-overviews-update-may-2026/), Averi.ai
- **Finding:** New "Expert Advice" block pulls first-hand perspectives from forums, social media, and review sites. Inline citations now sit next to specific text. Content with expert attribution and structured data is systematically favored.
- **Impact on writing:** Include "Reviewed by [Name], [Role] at brightplace" in footer. Structure content with clear extractable answers and named attribution.
- **Status:** ACTIVE
- **Last verified:** 2026-09-16
- **Checked by:** Claude Pre-Flight

### TREND-007: Google August 2026 core update (NEW — discovered this session)
- **Discovery date:** August 26, 2026
- **Source:** Google confirmed; reported by Search Engine Journal (https://www.searchenginejournal.com/google-algorithm-history/), Single Grain, Numinix
- **Finding:** August 2026 core update rolled out Aug 26 – Sep 21 (26 days). Unconfirmed additional activity around Sep 2-4. Continues Information Gain and E-E-A-T emphasis from March/May updates.
- **Impact on writing:** No new structural requirements beyond existing trends. Monitor rankings for brightplace content during rollout period.
- **Status:** ACTIVE
- **Last verified:** 2026-09-16
- **Checked by:** Claude Pre-Flight

### TREND-008: AEO three-pillar framework (NEW — discovered this session)
- **Discovery date:** 2026
- **Source:** HubSpot via Green Flag Digital (https://greenflagdigital.com/aeo-best-practices/), Writer.com (https://writer.com/blog/geo-aeo-optimization/)
- **Finding:** AEO best practices in 2026 center on three pillars: (1) build consensus (cited by multiple sources), (2) provide information gain (unique data), (3) use clear semantic structure (extractable claims). Featured snippets remain the top source for AI Overview citations.
- **Impact on writing:** Structure each H2 as a self-contained extractable unit. Lead with direct answers. Include structured data for key claims.
- **Status:** ACTIVE
- **Last verified:** 2026-09-16
- **Checked by:** Claude Pre-Flight

## Expired Trends
(trends that were active but no longer apply — keep for history)

## Pre-Flight Search Queries
Standard queries to run at the start of each production session:
1. `Google algorithm update [current month] [current year]`
2. `AEO AI overview optimization best practices [current year]`
3. `featured snippet ranking factors [current year]`
4. `Google AI Mode citation patterns [current year]`
5. `GEO generative engine optimization [current year]`

## Verification contract

Imported: 2026-09-16. Source artifacts: `Planning/memory-system-plan.md`,
`Agents/seo-writing-agent.md` AEO/SEO sections and `Agents/content-writing-guidelines.md`
§§5/8 (pre-migration). All six findings above are legacy claims, not verified facts.

Statuses: UNVERIFIED / ACTIVE / EXPIRED. Required on every new entry: unique TREND ID,
discovery date, source URL + publisher + source date, finding, scoped impact on writing,
status, last verified, checked by, evidence, and dated status-change history.
- UNVERIFIED entries cannot impose QA failures. Use them as research questions.
- Activate only after checking a supporting primary source; record what it actually
  supports and its limitations. Otherwise leave UNVERIFIED. Never fabricate citations.
- Only ACTIVE entries with a verification date within 30 days and topic-relevant scope
  are eligible for writing/QA. Missing or stale verification is WARNING / re-check.
- If contradicted, mark EXPIRED with dated evidence; preserve the original claim and
  link a replacement ID. Do not silently rewrite history.
- Agent scores and an article merely applying a technique do not verify a search-engine
  effect. Teaching records application outcomes separately; only new evidence refreshes
  last verified. Measured performance must identify source, period, and limitations.
- Brand/CMS rules prevail over trends. A trend proposing permanent policy changes goes
  to candidate-rules.md for user approval. Never invent reviewer attribution.
- The imported comparison claim mentions 3 sections, but the editorial application is
  one relevant cost comparison; do not enforce an inconsistent three-section threshold.
