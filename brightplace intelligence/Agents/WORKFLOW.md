# brightplace Content Production Workflow

**Version:** 1.1
**Last Updated:** September 2026
**Purpose:** This document defines the exact steps Claude Code follows when producing content for brightplace. Follow every step in order. Do not skip steps. Do not improvise the process.

---

## Memory References

Paths are relative to `brightplace intelligence/`, not the `Agents/` directory.
Read these files before this agent runs; missing memory must be reported, not guessed.
- `memory/semantic/brand-rules.md`
- `memory/semantic/cms-config.md`
- `memory/semantic/link-registry.md`
- `memory/semantic/ranking-rules.md`
- `memory/episodic/trend-intelligence.md`
- `memory/procedural/workflow-reference.md`
Canonical memory takes precedence over legacy examples. Follow the memory contract
in `Agents/WORKFLOW.md`; no permanent rule changes without explicit user approval.

## Overview

At every entry point, run Session Start and Master Writer Pre-Flight before Stage 0
or 1. After production, run Master Writer Teaching to persist memory and report it.

The workflow has 10 stages. Every article passes through all stages before it is considered complete.

```
0. Content Brief Agent → 1. Pull Brief → 2. Brief Check → 2.5 Reddit Research → 3. Writing Agent → 4. QA Agent → 5. Image Prompt → 5.5 HTML Generation → 6. Content Output → 7. GitHub Commit
```

**Stage 0 is optional when a brief already exists.** If the user provides a keyword without a brief, run Stage 0 first. If the user provides a pre-written brief, skip to Stage 1.

---

## Memory Contract and Session Start

Scope is `brightplace intelligence/` only. All `memory/...` paths below resolve
from that directory. This workflow owns the procedure; the procedural memory file
only points here. Memory is read and written by agents during a run, not a background
service. No database, automatic crawler, or new workflow stage is introduced.

### Session Start
1. Read `memory/procedural/workflow-reference.md` and this contract.
2. Read `memory/episodic/candidate-rules.md`; present PENDING entries with 3+ distinct
   occurrences for user approval/rejection. Do not block unrelated writing on them.
3. Read `memory/episodic/trend-intelligence.md`; flag unknown or >30-day verification
   dates for Pre-Flight. Only supported, in-scope, fresh ACTIVE trends are enforceable.
4. Retrieve required semantic files, then relevant ACTIVE QA patterns and topic-specific
   research episodes. Never import another property's numbers or policies by similarity.

### Read / Write Integration (existing stages)
| Stage | Reads | Writes |
|---|---|---|
| Pre-Flight (Master Writer) | `episodic/trend-intelligence.md`, `episodic/candidate-rules.md` | `episodic/trend-intelligence.md` with source evidence |
| 0 Brief | `semantic/keyword-strategy.md`, `semantic/link-registry.md`, `episodic/trend-intelligence.md` | None |
| 2 Brief Check | `semantic/brand-rules.md`, `semantic/link-registry.md`, `episodic/qa-patterns.md`, `episodic/trend-intelligence.md` | `episodic/candidate-rules.md` for new evidenced gaps |
| 2.5 Reddit | `episodic/reddit-patterns.md` | New themes; merge distinct source IDs into matching themes |
| 3 Writing | All six `semantic/` files; `episodic/qa-patterns.md`, `episodic/trend-intelligence.md` | None |
| 4 QA | `semantic/brand-rules.md`, `semantic/link-registry.md`, `episodic/qa-patterns.md`, `episodic/trend-intelligence.md` | `episodic/qa-patterns.md`, `episodic/link-failures.md`, `episodic/corrections.md` |
| Teaching (Master Writer) | `episodic/trend-intelligence.md`, QA report | `episodic/trend-intelligence.md`, `episodic/content-log.md`, `episodic/candidate-rules.md` |

### Record and retrieval rules
- Required semantic files are never skipped to save context. For growing episodic
  logs, search by ID/topic/scope first, then load at most 10 relevant records plus all
  applicable active trends. Expand when needed; record exclusions, not silent omission.
- Record date precision honestly, source/report path, article/revision/run ID, scope,
  and observed vs inferred status. A migration timestamp is not a verification date.
- Dedup by stable record/evidence IDs. Count distinct articles/events, not retries or
  repeated mentions. Read the current file immediately before appending; preserve
  concurrent edits and report conflicts rather than overwriting someone else's work.
- Existing semantic rules outrank episodes and trends; current user instructions
  outrank stored policy. No memory record grants tool, publication, or commit permission.
- New permanent rules remain PENDING candidates until explicit user promotion. Store
  decision provenance, changed target and rollback reference. Rejecting preserves history.
- Do not copy credentials, private user details, or unverified renter assertions into
  reusable facts. Verify prices, dates and policies against appropriate current sources.
- Never replace missing evidence with an invented metric, date, attribution, or outcome.
- Record memory IDs read/applied/written in QA/Teaching artifacts. If memory access fails,
  report blocked reads or pending writes explicitly; never claim learning was persisted.
- Keep original reports as evidence. Corrections and expiry retain prior history.

---

## Stage 0: Content Brief Agent (Auto-Generate Brief from Keyword)

**Trigger:** User provides a keyword without a pre-written brief (e.g., "write about foxchase apartments alexandria va" or "keyword: pet friendly apartments greenville sc")

**Agent file:** `brightplace intelligence/Agents/content-brief-agent.md`

**Process:**
1. Hit DataForSEO API with the primary keyword to get live SERP data (organic results, PAA, featured snippets, AI Overview, related searches)
2. Run variant keyword searches (reviews, pet policy, amenities, parking for property keywords)
3. Analyze what AI engines are currently answering for this keyword
4. Fetch and analyze top 5 competitor pages (word count, headings, gaps)
5. Fetch brightplace sitemap for internal link targets (7+)
6. Find and verify external authority links (3-5 .gov/.edu)
7. Compile everything into a structured content brief

**DataForSEO API call:**
```bash
curl -X POST "https://api.dataforseo.com/v3/serp/google/organic/live/advanced" \
  -H "Authorization: Basic YmVuQGJhc2VvcGVyYXRpb25zLmNvbTo5YjFmZTRiNzU0MjA2NDBj" \
  -H "Content-Type: application/json" \
  -d '[{"location_name": "United States", "language_code": "en", "keyword": "[KEYWORD]", "device": "desktop", "depth": 100, "parse": true}]'
```

**Output:** Save brief to `brightplace intelligence/Content Brief/[keyword-slug]-brief.md`

**Decision rule:**
- Brief generated → proceed to Stage 1 (or skip Stage 1 since brief is already local)
- API fails → fall back to web search for SERP data, then build brief manually
- SERP shows listings/tools instead of articles → STOP, tell user this keyword won't work for blog content, suggest alternative angle

**Property detection:** If the keyword contains a specific apartment community name, the brief agent automatically includes the 4 mandatory property sections (pet policy, amenities, parking, walkability) in the outline.

---

## Stage 1: Pull the Content Brief

**Trigger:** User says "I pushed a new brief" or "pull the briefs"

**Action:**
```bash
git pull origin main
```

**Check:** Confirm new files appeared in `brightplace intelligence/Content Brief/`

**Output:** Read the brief file completely before proceeding.

---

## Stage 2: Brief Check Agent

**Purpose:** Validate the brief's strategic quality before writing. Catch keyword gaps, missing entities, weak AEO structure, and link issues BEFORE they become article problems.

**Agent file:** `brightplace intelligence/Agents/brief-check-agent.md`

**What to check (6 sections):**

1. **Keyword Coverage** — Is the primary keyword right? Are secondary keywords missing? Are entities complete?
2. **AEO/GEO Validation** — Will this article get cited by AI engines? Are sections self-contained? Are definitions extractable? Are proof points specific enough?
3. **SERP Intent Match** — Does the format match what's ranking? Are PAA questions covered? Are content gaps genuine?
4. **Brand & Compliance** — Title framing correct? CTAs point to `https://www.brightplace.ai/search`? Internal link targets identified?
5. **Competitive Depth** — Enough competitor analysis? Clear differentiation strategy?
6. **Independent Research** — Additional keywords to add? Topical authority fit?

**Output format:**
```
# BRIEF CHECK REPORT: [Keyword]
Brief Status: APPROVED / NEEDS REVISION
[Summary of checks, improvements, additional keywords, missing links]
Verdict: [Proceed or revise]
```

**Decision rule:**
- If APPROVED → proceed to Stage 2.5
- If NEEDS REVISION → make improvements yourself during drafting (don't send back to user unless critical issues exist)
- If REJECTED → tell the user the brief needs rework and explain why

---

## Stage 2.5: Reddit Research Agent

**Purpose:** Search Reddit for real renter conversations about the brief's target keywords. Extract authentic questions, pain points, specific numbers, and language patterns. Enrich the brief so the Writing Agent produces content that matches how renters actually talk and think.

**Agent file:** `brightplace intelligence/Agents/reddit-research-agent.md`

**Process:**
1. Take the primary and secondary keywords from the brief
2. Search Reddit (r/ApartmentHunting, r/renting, r/personalfinance, r/FirstTimeRenter, r/Frugal + city-specific subs if relevant)
3. Analyze 5-10 threads with real discussion (10+ comments preferred)
4. Extract: real questions, pain points, specific numbers, misconceptions, language patterns, heavily upvoted advice
5. Compile a Reddit Research Report with enrichment recommendations

**Output:** A structured report with:
- Top renter questions (exact phrasing from threads)
- Pain points and frustrations
- Real numbers cited by renters
- Common misconceptions to address
- Language patterns to use
- Brief enrichment recommendations (new FAQs, new H2s, reframes)

**Rules:**
- Research only — no content is written during this stage
- NEVER cite Reddit as a source in the article (banned source per guidelines)
- NEVER quote Reddit users by username
- NEVER link to Reddit threads in the article
- The Reddit data informs the writing voice and content depth, not sourcing

**Decision rule:**
- Report compiled → proceed to Stage 3 (Writing Agent uses the enriched brief + Reddit report)

---

## Stage 3: Writing Agent

**Purpose:** Draft the complete article following the brief and all content guidelines.

**Reference files:**
- `brightplace intelligence/Agents/content-writing-guidelines.md` — master brand + SEO rules
- `brightplace intelligence/Agents/seo-writing-agent.md` — writing agent prompt with AEO section
- `brightplace intelligence/Agents/renters-corner-guidelines.md` — ONLY for Renter's Corner (interview-based) pieces

**Critical rules during drafting:**

### Content Structure
- H1 title from the brief
- **All H2 headings must be question-format** matching PAA queries (e.g., "What Are the Rent Prices at [Property]?" not "Rent Prices and Unit Types")
- Every H2 opens with its answer in the first sentence (40-60 words)
- **First paragraph after H1 must be 49-55 words**, structured as a standalone featured snippet answer
- Self-contained sections (each works if extracted independently)
- Bold-label bullet points are the editorial preference for comparisons. `<ul><li>`
  and `<table>` are now allowed — that ban existed only because Webflow RichText
  stripped the tags, and Vercel does not.
- **10+ FAQ pairs preferred** (minimum 6-8), each 40-60 words, standalone answers.
  Write each question as an `###` heading so it renders as `<h3>`, matching the corpus.
- **Entity density:** use `memory/semantic/ranking-rules.md` targets naturally

### Ranking Optimization (apply to every article)
- **7+ internal links** per article (aggressive cross-linking builds topical authority)
- **Target correct search intent** — only target keywords where Google shows article/guide content, NOT listings or templates
- **Fill genuine content gaps** — include data, comparisons, and tradeoffs NO competitor covers
- **Question-format H2s** are an editorial target per `memory/semantic/ranking-rules.md`

### Links
- One domain. `app.brightplace.ai` is merged into the main site and **must never
  appear in a link** — it 308s to www and costs a needless redirect hop.
- Canonical host in every href: `https://www.brightplace.ai`. Bare apex
  `https://brightplace.ai` also 308s to www. Write "brightplace.ai" in link *text*
  where the brand reads better; the href stays `www`.
- Search-action CTAs → `https://www.brightplace.ai/search`
- Brand mentions → `https://www.brightplace.ai`
- 3 CTAs: after first H2, mid-article, end of article
- Internal links use `https://www.brightplace.ai/resources/[slug]` or `https://www.brightplace.ai/guides/[slug]`
- NEVER use `/knowledgebase/` path (legacy, causes 404s)
- Reject known non-existent targets in `memory/semantic/link-registry.md`.

### Brand Rules (zero tolerance)
- Read and enforce all rules in `memory/semantic/brand-rules.md`.

### Schema
- All schema URLs use `/resources/` path, NOT `/knowledgebase/`
- Breadcrumb position 2 = "Resources" NOT "Knowledgebase"
- Three schemas required: FAQPage, Article, WebPage
- SEO title MUST differ from H1

### Dates
- All figures dated "(as of Q[N] YYYY)"
- Include "Last reviewed: [Month Year]" in article
- Use current quarter, not the brief's quarter if it's outdated

**Output:** Save to `brightplace intelligence/Complete Articles/[slug].md`

---

## Stage 4: QA Agent (FULL — ALL SECTIONS)

**Purpose:** Catch every issue before the article goes to `brightplace content/`. This is the gate. Nothing passes without a full QA.

This gate matters more than it used to. Under Webflow, a push created a draft a human
still had to publish. Now the commit goes straight live, so QA is the last human-proof
checkpoint before readers see it.

**Agent file:** `brightplace intelligence/Agents/qa-agent.md`

**YOU MUST RUN ALL 6 SECTIONS. DO NOT SKIP ANY.**

### Section 1: Brand Compliance
- Run each canonical check in `memory/semantic/brand-rules.md`.

### Section 2: SEO Structure (knowledgebase only)
- First sentence contains keyword
- Keyword density 7-12 instances
- Meta description under 155 chars
- SEO title under 60 chars and DIFFERENT from H1
- Heading hierarchy (one H1, H2s, H3s)
- H2 opening rule (answer first)
- Body html carries no `<h1>` and no `<script>`
- Date stamps on all figures
- FAQ section (6-8 pairs, 40-60 words each)
- All 3 schemas present with correct URLs

### Section 3: Renter's Corner Structure (Renter's Corner only)
- Source material used
- Cohort in title
- Katie voice throughout
- Section word counts within targets
- Quoted source phrases

### Section 4: Math Verification
- Verify EVERY calculation independently
- Show the math

### Section 5: Link Audit (CRITICAL — DO NOT SKIP)
- **Internal links:** List every brightplace.ai link. Verify against
  `https://www.brightplace.ai/sitemaps/content.xml` — **not** `/sitemap.xml`, which is
  now an index and contains no article URLs. REJECT any `/knowledgebase/` path. REJECT
  any `app.brightplace.ai` host. REJECT known non-existent URLs.
- **External links:** List every non-brightplace link. REJECT banned sources. REJECT known broken URLs from the QA agent's broken URL list. Flag any .gov/.edu link not on the approved list for manual verification.
- **CTA links:** Count them and verify each points to `https://www.brightplace.ai/search`
  or `https://www.brightplace.ai`. Any `app.brightplace.ai` is a FAIL.

### Section 6: Infrastructure Checks (CRITICAL — DO NOT SKIP)
- No `http://` links (all must be `https://`)
- No `app.brightplace.ai` anywhere (body, schema, frontmatter) — merged into the main site
- No legacy `/knowledgebase/` paths anywhere (body, schema, frontmatter)
- Frontmatter consistency (slug, dates, schema_types)
- External link freshness (check against approved list)
- **Output file set** — all three files present (`.md`, `.html`, image), body html has
  no `<h1>` and no `<script>`, no stray `<head>`/`<body>`/`<style>`/`<base>` tags,
  correct collection folder

**Output format:**
```
# QA REPORT: [Article Title]
Content Type: knowledgebase / renters-corner
All checks: [X passed, Y failed]
[Full results table]
[Any fixes made]
```

**Decision rule:**
- All pass → proceed to Stage 5
- Any FAIL → fix immediately, re-run the failed check, confirm PASS, then proceed

---

## Stage 5: Image Generation

**Purpose:** Generate a featured image prompt AND automatically generate the actual image.

**Reference file:** `brightplace intelligence/Agents/blog-image-prompts.md`

**Process (2 steps):**

### Step 1: Generate Prompts
- Build Visual Identity Brief from article content and research files
- Write 3 prompt options (A recommended, B and C alternatives)
- Include alt text and filename
- Save prompts to `brightplace intelligence/Images/[batch]-image-prompts.md`

### Step 2: Generate Image (AUTOMATED)
Run the `generate-image.py` script with Prompt Option A:

```bash
python3 "SUPER SEO Agents/generate-image.py" \
  --prompt "[Prompt Option A]" \
  --output "brightplace intelligence/Images/[keyword-slug]-featured.webp" \
  --alt "[Alt text]"
```

**Requirements:** `OPENAI_API_KEY` in `.env` (already configured), `openai` + `Pillow` packages (already installed).

**Image specs:**
- 1200 x 628 pixels, 16:9 aspect ratio
- WebP format, under 200KB
- No people visible (Fair Housing)
- No text, logos, or watermarks
- Warm editorial photography style
- Uses GPT Image 2 model

**Output:**
- Image file: `brightplace intelligence/Images/[keyword-slug]-featured.webp`
- Metadata: `brightplace intelligence/Images/[keyword-slug]-featured.json`
- Prompts: `brightplace intelligence/Images/[batch]-image-prompts.md`

---

## Stage 5.5: HTML Generation (Production-Ready File)

**Purpose:** Convert the final enriched markdown article (stage 09) into a standalone, self-contained HTML file with its own head, schema and CSS.

⚠️ **This is no longer the publishing artifact for brightplace.ai.** Stage 6 output is.
The Vercel template now builds the head, canonical, Open Graph and JSON-LD from
frontmatter, so a standalone page is redundant for brightplace content — it duplicates
what the template already does, and a stale copy is worse than none.

Keep running this stage for the **AIR Operator pipeline**, where it remains Stage 10 and
is genuinely the deliverable. For brightplace.ai articles it is optional: useful for an
offline preview, never the thing that ships.

**Script:** `AIR operator/generate-html.py`

**Process:**
1. Read the stage-09 final-enriched markdown file
2. Parse YAML frontmatter (title, seo_title, meta_description, slug, dates, keywords)
3. Extract all JSON-LD schemas (FAQPage, Article, WebPage) from the markdown
4. Extract canonical URL from the WebPage schema
5. Convert markdown body to semantic HTML (no external dependencies)
6. Build complete HTML document with all SEO requirements
7. Save as `10-[slug].html` in the same article folder

**Run for all completed articles:**
```bash
cd "AIR operator" && python3 generate-html.py
```

**What the HTML includes (full SEO checklist):**

Head section:
- SEO title (distinct from H1) in `<title>` tag
- `<meta name="description">` with meta description
- `<meta name="keywords">` with primary + all secondary keywords
- `<meta name="robots">` with `max-snippet:-1, max-image-preview:large, max-video-preview:-1`
- `<link rel="canonical">` populated from WebPage schema URL
- `<link rel="alternate" hreflang="en-US">` for language targeting
- Open Graph tags: `og:type`, `og:title`, `og:description`, `og:url`, `og:image` (placeholder), `og:locale`, `article:published_time`, `article:modified_time`, `article:author`
- Twitter Card tags: `summary_large_image`, title, description, image placeholder
- All 3 JSON-LD schemas embedded as `<script type="application/ld+json">`

Body section:
- `<article itemscope itemtype="https://schema.org/Article">` wrapper with microdata
- Author and date in `<header>` with `itemprop` attributes
- First paragraph tagged with `class="article-intro"` (AEO citability + speakable spec target)
- FAQ section wrapped in `<section class="faq-section" aria-label="Frequently Asked Questions">` (speakable spec target)
- "Last reviewed: [Month Year]" in `<footer class="article-footer">`
- Word count in HTML comment for reference
- Single H1 only
- All external links use `target="_blank" rel="noopener"`
- Mobile-responsive CSS (breakpoint at 640px)

**Before publishing (manual steps):**
- Add featured image URL to `og:image` and `twitter:image` (marked with `TODO` comments in the HTML)
- Verify canonical URL matches the actual deployment URL

**Output:** `10-[slug].html` in the same folder as the source article

**For AIR Operator pipeline:** This is Stage 10 in the numbered file convention (after 09-final-enriched.md). The `generate-html.py` script processes ALL stage-09 files across all community folders in one run.

---

## Stage 6: Content Output

**Purpose:** Write the finished article as the three-file set that GitHub ships to the
live site. This replaces the Webflow CMS push. There is no CMS, no API call and no MCP
call in the publishing path any more.

```
Stage 6 writes files → Stage 7 commits → GitHub → Vercel build → live
```

**Destination:** `brightplace content/<collection>/`

```
brightplace content/
├── guides/      → www.brightplace.ai/guides/<slug>     (RESTRICTED — do not write here)
├── news/        → www.brightplace.ai/news/<slug>       (announcements, explicit tasks only)
└── resources/   → www.brightplace.ai/resources/<slug>  (all new content — the default)
```

The folder name is the URL prefix. The file name is the URL segment.

**Configuration:** read `memory/semantic/cms-config.md` for the full frontmatter
schema, body rules, category slugs and routing. Never copy configuration into prompts.

**Process — write three files, one slug:**

### 1. `brightplace content/resources/[slug].md`

The full article with YAML frontmatter. This is the archival record and the source of
every value the page template renders.

```yaml
---
title: "..."                     # renders as the <h1>
seo_title: "... | brightplace"   # <title>. Must differ from title. Under 60 chars.
meta_description: "..."          # under 155 chars
slug: ...                        # matches the file name and the URL segment
primary_keyword: "..."
secondary_keywords: ["...", "..."]
schema_types: ["Article", "FAQPage", "WebPage"]
word_count_target: "1,100-1,300"
last_reviewed: "Month YYYY"
date_published: YYYY-MM-DD
date_modified: YYYY-MM-DD
author: Katie Mikles
category: ...                    # property | lifestyle | neighborhood-guides |
                                 # renter-advice | top-apartments | renter-corner
summary: "..."                   # first paragraph, plain text, under 300 chars
main_image_alt: "..."            # alt text from Stage 5
---
```

⚠️ **`author` is `Katie Mikles`, not `brightplace`.** Webflow used to override the
draft's placeholder byline on publish. Nothing overrides it now — the frontmatter is
the only source. Writing `brightplace` there publishes a wrong byline.

### 2. `brightplace content/resources/[slug].html`

The body only, as a fragment.

- **No `<h1>`.** The template supplies it from `title`. A body with an `<h1>` puts two
  on the page and fails QA Section 2.
- Opens with `<p><em>Last reviewed: Month YYYY</em></p>`, then the first `<h2>`.
- **FAQ questions are `<h3>`, not bold paragraphs.** 82 of the 86 live Resources bodies
  do this, and all 86 contain `<h3>` somewhere. Write them as `###` in the markdown.
- **No `<script>`.** Keep the JSON-LD in the `.md`; the template server-renders schema
  from frontmatter. Never carry a schema block into the body html.
- No `<head>`, `<body>`, `<style>`, `<base>`, no frontmatter, no internal review notes.
- Internal links **site-relative** (`/resources/[slug]`), never absolute apex or `app.`.
- `<ul><li>` and `<table>` are now allowed — that ban existed only because Webflow
  RichText stripped them. Bold-label bullets remain the editorial preference for
  comparisons, but lists no longer break the page.

### 3. `brightplace content/resources/[slug].<ext>`

The featured image from Stage 5, named by slug. `png`, `jpg`, `jpeg` or `webp`.
1200 x 628, under 200KB, no people visible.

**The user no longer adds the featured image separately.** It ships in the commit.

The live URL is `https://www.brightplace.ai/content/<collection>/<slug>.<ext>` — note
`/content/` in the path, not `/resources/<slug>.<ext>`, which 404s. Both `.png` and
`.webp` serve. Put that absolute URL in `main_image` and in the Article schema `image`.

**There is no draft state.** An article is live once committed and built. Anything not
ready to publish stays out of `brightplace content/` and waits in `Complete Articles/`.

---

## Stage 7: GitHub Commit

**Purpose:** Publish. On the new stack, the commit *is* the publication — merging to
`main` triggers the Vercel build that puts the article on the live site.

**Only commit when the user explicitly asks.** This carries more weight than it used to:
under Webflow a push created a draft that a human still had to publish. A commit here
goes live.

**What to commit:**
- `brightplace content/resources/[slug].md`
- `brightplace content/resources/[slug].html`
- `brightplace content/resources/[slug].<ext>`
- `Complete Articles/[slug].md` (the working draft, kept for history)

**Commit message format:**
```
Add [article title] to resources

- [word count] words, QA passed all checks
- [number] content gaps filled: [list them]
- [number] FAQ pairs, [number] CTAs, all URLs use /resources/ path
- Published to brightplace content/resources/

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

**If the GitHub token is expired:** tell the user to update it. Do not attempt to push
with a bad token.

---

## Content Types

| Type | Guide | Author Voice | Lives At |
|---|---|---|---|
| Knowledgebase (Resources) | content-writing-guidelines.md + seo-writing-agent.md | 3rd person, brightplace | /resources/[slug] |
| Renter's Corner | renters-corner-guidelines.md | 1st person, Katie | /resources/[slug] |
| Property Article | seo-writing-agent.md (Property Template section) | 3rd person, brightplace | /resources/[slug] |
| Guest Posts | Manual guidelines | 3rd person, editorial | External sites |
| News | LinkedIn announcements as source | 3rd person, brightplace | News CMS collection |

---

## Property Article Workflow Notes

Property articles follow the same 8-stage workflow as all other content, with these stage-specific differences:

**Stage 1 (Pull Brief):** The brief should target a specific apartment community. The primary keyword includes the property name + modifiers (pet policy, amenities, parking, walkability).

**Stage 2 (Brief Check):** Run the standard brief check PLUS Section 5c (Property Article Completeness Check). The brief must include data on pet policy, amenities, parking, and nearby essentials. FAIL if 2+ of these are missing.

**Stage 2.5 (Reddit Research):** Run Step 1b (Property-Specific Research) IN ADDITION to the standard search. Search for property-name reviews, pet complaints, parking frustrations, amenity feedback, and walkability reports from actual residents. Extract all 12 categories (standard 8 + property-specific 4).

**Stage 3 (Writing):** Use the Property-Specific Article Template in seo-writing-agent.md. The article MUST include all 4 mandatory H2 sections: Pet Policy, Amenities, Parking, and Walkability/Nearby Essentials. All distances must be specific (miles + walk times). All costs must be date-stamped.

**Stage 4 (QA):** Run all 6 standard QA sections PLUS the 6 property-specific self-review checks (items 25-30 in the writing agent checklist). Verify that pet, amenity, parking, and walkability sections contain specific data, not vague claims.

**Stages 5-7:** No changes. Same image prompt, content output, and commit process.

---

## URL Registry

See `memory/semantic/link-registry.md` for all URL inventories, replacements,
and validation rules. Check `memory/episodic/link-failures.md` for newer evidence.

---

## Quick Reference: The Full Flow

**When the user gives you a KEYWORD (no brief):**

0. **Brief Agent** → Hit DataForSEO API, analyze SERP + AI engines + competitors, generate brief → save to `Content Brief/[slug]-brief.md`
1. **Brief Check** → Validate the auto-generated brief (keyword gaps, AEO, property completeness)
1.5. **Reddit Research** → Search Reddit/Quora for real renter questions, pain points, language
2. **Write** → Draft article using brief + Reddit research report
3. **QA** → Run FULL qa-agent.md (ALL 6 sections including link audit)
4. **Image** → Generate 3 image prompts with alt text
4.5. **HTML** → Run `generate-html.py` to create production-ready HTML (stage 10 file)
5. **Output** → Write `.md` + `.html` + image to `brightplace content/resources/`
6. **Commit** → Only when user says "push to GitHub". The commit publishes.

**When the user gives you a PRE-WRITTEN BRIEF:**

1. **Pull** → `git pull origin main`
2. **Brief Check** → Run brief-check-agent.md (keyword gaps, AEO, links)
2.5. **Reddit Research** → Run reddit-research-agent.md
3. **Write** → Draft article using brief + Reddit research report
4. **QA** → Run FULL qa-agent.md (ALL 6 sections including link audit)
5. **Image** → Generate 3 image prompts with alt text
5.5. **HTML** → Run `generate-html.py` to create production-ready HTML (stage 10 file)
6. **Output** → Write `.md` + `.html` + image to `brightplace content/resources/`
7. **Commit** → Only when user says "push to GitHub". The commit publishes.

If any stage fails, fix and re-run that stage before proceeding. Never skip a stage.

---

*This workflow document is the source of truth for how brightplace content is produced. All agents, guidelines, and processes referenced here are stored in the `brightplace intelligence/Agents/` folder.*
