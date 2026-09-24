# brightplace Content Writing Guidelines

**Version:** 2.0
**Last Updated:** May 2026
**Applies to:** All content published at brightplace.ai/guides/ and brightplace.ai/resources/

---

## Memory References

Paths are relative to `brightplace intelligence/`, not the `Agents/` directory.
Read these files before this agent runs; missing memory must be reported, not guessed.
- `memory/semantic/brand-rules.md`
- `memory/semantic/content-standards.md`
- `memory/semantic/ranking-rules.md`
- `memory/semantic/cms-config.md`
- `memory/semantic/link-registry.md`
- `memory/episodic/trend-intelligence.md`
Canonical memory takes precedence over legacy examples. Follow the memory contract
in `Agents/WORKFLOW.md`; no permanent rule changes without explicit user approval.

## 1. Brand Rules (Zero Tolerance)

See `memory/semantic/brand-rules.md` for all brand restrictions.
Active, verified trends: `memory/episodic/trend-intelligence.md`.

---

## 2. Voice and Tone

You write like a **knowledgeable friend** who has done the research and is being direct about what they found.

- **Lead with information, not personality.** The reader came from a search engine with a specific question. Answer it.
- **Be utilitarian first, warm second.** Short declarative sentences. Get to the point.
- **Use specifics constantly.** Dollar amounts, distances, time durations, counts, names of actual places.
  - Bad: "great dining options nearby"
  - Good: "14 restaurants within a 10-minute walk, including three along Main Street"
- **Include honest tradeoffs.** Renters trust content that acknowledges downsides plainly.
- **Never be promotional about brightplace.** The article earns trust by being useful, not by selling.

---

## 3. SEO Structure Requirements

### 3.1 First Paragraph Rule
The very first sentence must:
1. Contain the primary keyword
2. Begin answering the searcher's query directly

The first 100 words must contain:
1. A direct answer to the keyword query
2. A clear statement of who this article is for
3. At least one specific data point (number, dollar amount, percentage, or named entity)

### 3.2 Heading Hierarchy
- **One H1 only** (the article title)
- All major sections are **H2**
- Subsections are **H3**
- Never skip heading levels (no H1 to H3)
- Every H2 section must open with its key answer in the first sentence (40-60 words)

### 3.3 Meta Description
- Under **155 characters**
- Must contain the **primary keyword**
- End with a clear value proposition
- No questions, no clickbait

### 3.4 Keyword Density and Placement
- **Exact-match keyword must appear 7-12 times** in a 1,200-1,500 word article (0.5-1.0% density)
- **H1 title must contain the exact keyword** (not a variation)
- **First 100 words must contain the exact keyword**
- **At least 2 H2 headings** must contain keyword words
- Mix exact-match and natural variations (e.g., "2 bedroom apartments Bloomington" + "2 bedroom apartments in Bloomington")
- Never force a keyword where it reads awkwardly; if it doesn't fit, use a close variant
- Do NOT exceed 1.5% density (keyword stuffing penalty risk)

### 3.5 Comparison Formatting
- **Default to bold-label bullet points** for comparison/pricing/feature data
- Example: `**Studio:** $2,550/mo (as of Q2 2026). Stone countertops, LVP flooring.`
- The old hard ban existed because Webflow RichText could not render tables. Vercel
  renders them fine, so a table is no longer a rendering failure. Bold-label bullets
  stay the editorial default for their AEO value: each line is independently
  extractable, where a table row often is not.
- Relaxing this to allow tables outright is logged in `episodic/candidate-rules.md`
  and needs the user's decision. Until then, keep using bold-label bullets.

### 3.6 URL Slug
- Lowercase, hyphen-separated
- Contains the primary keyword
- No stop words unless needed for readability
- Example: `brightplace.ai/guides/pet-friendly-apartments-greenville-sc`

---

## 4. Linking Requirements (Google 2026 Standards)

### 4.1 Internal Links
**Target: 5-10 internal links per 1,000 words of content**

For a standard 1,200-1,500 word article: **8-12 internal links**

| Article Length | Minimum Internal Links | Ideal Internal Links |
|---|---|---|
| 800-1,000 words | 5 | 7-8 |
| 1,000-1,300 words | 7 | 8-10 |
| 1,300-1,600 words | 8 | 10-12 |
| 1,600-2,000 words | 10 | 12-15 |

**Rules:**
- Use natural anchor text that describes the destination content
- Never use "click here" or "read more" as anchor text
- Link only on first mention of a topic within a section
- Place links mid-sentence where they feel natural
- Do not cluster multiple links in one paragraph
- Never link to the article's own URL
- Link to real URLs from the brightplace sitemap (check `/guides/` and `/resources/`)
- Use `[INTERNAL LINK: topic description]` placeholder only when no sitemap match exists

**Priority link targets (always try to include):**
- `/guides/how-to-rent-an-apartment` (renting process)
- `/guides/your-true-monthly-cost` (budgeting/fees)
- Relevant city or neighborhood guide from sitemap
- Relevant topical guide (pet-friendly, family, student, etc.)

### 4.2 External Links
**Target: 3-5 external links per 1,000 words of content**

For a standard 1,200-1,500 word article: **4-6 external links**

| Article Length | Minimum External Links | Ideal External Links |
|---|---|---|
| 800-1,000 words | 3 | 4-5 |
| 1,000-1,300 words | 4 | 5-6 |
| 1,300-1,600 words | 5 | 6-7 |
| 1,600-2,000 words | 5 | 7-8 |

**Rules:**
- All external links must open in a new tab: `target="_blank" rel="noopener"`
- Link only to authoritative sources: `.gov`, `.edu`, official transit authorities, official property management sites, state/county government pages
- **NEVER link to competitors or send traffic to competing platforms.** This includes all ILS platforms, review aggregators, score sites, forums, and vacation rental platforms listed in `memory/semantic/brand-rules.md`. We do not badmouth competitors, but we do not give them our audience either.
- Never link to banned sources (see `memory/semantic/brand-rules.md`)
- Prioritize:
  - Government sites (.gov, .edu)
  - Official transit authorities (MBTA, WMATA, DART, CATS, etc.)
  - State park and recreation sites
  - Official property management company sites
  - HUD, state attorney general consumer protection pages
  - SBA.gov for commercial content

### 4.3 CTA Links (brightplace)
- Place **3 brightplace CTAs** per article:
  1. After the first H2 (once the reader has context)
  2. After the comparison/neighborhood section (mid-article)
  3. End of article (after FAQ or as final paragraph)
- **One domain.** `app.brightplace.ai` was merged into the main site and must never
  appear in a link — it 308s to www and costs a needless redirect hop. Bare apex
  `brightplace.ai` redirects too. Every href uses `https://www.brightplace.ai`.
  Write "brightplace.ai" in link *text* where the brand reads better.
- **Two CTA targets:**
  - `https://www.brightplace.ai` — brand mentions and general references ("learn more at brightplace.ai")
  - `https://www.brightplace.ai/search` — action CTAs where the reader should search ("start searching at brightplace.ai")
  - At least one CTA per article should link to `/search` to drive search traffic
- Use informational framing only: "See what is available on brightplace" / "brightplace tracks current availability" / "Start searching at brightplace.ai"
- Never use: "Sign up," "Get started," "Don't wait," "Find your dream home"
- brightplace CTAs do NOT count toward the internal link target

---

## 5. Content Quality Standards (Google E-E-A-T 2026)

### 5.1 Experience Indicators
- Frame data as brightplace's own research: "Based on brightplace's review of Greenville apartment communities..."
- Include practical guidance that reflects real-world knowledge (what to ask during a tour, what to check before signing)
- Use "what renters ask" framing to reflect genuine engagement with searcher behavior
- Include at least one honest tradeoff or limitation per article
- **Named expert attribution:** Credit only an actual reviewer; never invent review or credentials.

### 5.1.1 Original Contribution
- Every article must include at least one data point, comparison, or insight not available on competing pages.
- Prioritize: proprietary brightplace data, original rent comparisons, first-hand market observations, worked cost examples, and specific local details competitors omit.

### 5.2 Expertise Indicators
- Every dollar figure, rent range, or statistic must include a **date stamp**: `(as of Q2 2026)`
- Define technical terms in a single clear sentence at first use
- Include specific numerical claims with sources (unit counts, square footage, AMI thresholds)
- Provide worked examples (total 12-month cost, rent conversion formulas)

### 5.3 Authoritativeness Indicators
- Use external links to authoritative sources (government, transit, official)
- Reference specific named entities (property names, addresses, management companies)
- Include structured comparisons with verifiable data
- Cite California/Texas/state-specific laws by name and number when relevant (AB 1482, AB 12)

### 5.4 Trustworthiness Indicators
- All frontmatter must include: `author: brightplace` and `last_reviewed: "[Month Year]"`
- Include "Last reviewed: [Month Year]" note at article footer
- Flag uncertain data with `[VERIFY BEFORE PUBLISH]` rather than fabricating
- Never present stale pricing as current
- Direct readers to verify with the leasing office for any time-sensitive data

---

## 6. Writing Mechanics

### 6.1 Paragraph Rules
- **2-4 sentences per paragraph maximum.** No wall-of-text paragraphs.
- Vary paragraph length. Mix 1-sentence, 2-sentence, and 3-4 sentence paragraphs.

### 6.2 Sentence Rules
- Prefer **short declarative sentences.** Two short sentences are better than one compound sentence.
- Vary sentence length deliberately. Follow a long sentence with a short one.
- Never start three consecutive sentences with the same word or structure.
- Never start a sentence with "It is" or "There are" when a more direct construction exists.

### 6.3 List Rules
- Use bullet lists only for genuinely parallel items (features, options, steps).
- Never use bullets as a substitute for prose explanation.
- Numbered lists for sequential steps only.

### 6.4 Comparison Format
- Use bold-label paragraphs; follow `memory/semantic/cms-config.md` for CMS HTML.
- Do not use Markdown tables in published bodies.

---

## 7. FAQ Section Requirements

- Place as the **last H2 before schema blocks**
- Use exact questions from the content brief (sourced from PAA data)
- Each answer must be **40-60 words** (featured snippet extraction sweet spot)
- Write each answer as a **complete, standalone response**
- Do not reference other sections of the article
- Lead each answer with the direct response in the first sentence
- Target: see `memory/semantic/ranking-rules.md` (10+ preferred, minimum 6–8 with brief justification)

---

## 8. Schema Markup (Required on Every Article)

### 8.1 FAQPage Schema (JSON-LD)
- Include every Q&A pair from the FAQ section
- Answers must match the article's FAQ answers word-for-word
- Search-engine claims and verification state live in `memory/episodic/trend-intelligence.md`.

### 8.2 Article Schema (JSON-LD)
- `headline`: Article title
- `description`: Meta description
- `author`: `{"@type": "Organization", "name": "brightplace", "url": "https://brightplace.ai"}`
- `publisher`: Same as author
- `datePublished` and `dateModified`: YYYY-MM-DD format

### 8.3 WebPage Schema (JSON-LD)
- Include breadcrumb (Home > Resources > Article Title)
- Include speakable specification targeting `.article-intro` and `.faq-section`
- Include canonical URL

---

## 9. Anti-AI-Detection Patterns

Google's Helpful Content system flags AI-generated content patterns. Actively avoid:

- **No symmetric structures.** Vary section lengths. Do not give every section the same paragraph count.
- **No hedge stacking.** Do not write "However, it is important to note that while some may find..." Just state the fact.
- **No false balance.** If one option is clearly better, say so plainly.
- **No transition word addiction.** "Furthermore," "Moreover," "Additionally" used repeatedly is an AI tell.
- **No conclusion that restates the intro.** The closing paragraph should add a final practical insight or next step.
- **Specificity over abstraction.** "Rent prices have been rising" is filler. "Average 1BR rent in Austin increased 4.2% year-over-year to $1,580 as of Q1 2026" is useful.
- **Vary your H2 openings.** Do not start more than two H2 sections with the same sentence structure.

---

## 10. Markdown Output Format

Every article must follow this exact structure:

```
---
title: "[Article Title]"
meta_description: "[Under 155 characters, includes primary keyword]"
slug: "[url-friendly-slug]"
primary_keyword: "[exact primary keyword]"
schema_types: ["Article", "FAQPage", "WebPage"]
word_count_target: [number from brief]
last_reviewed: "[Month Year]"
date_published: YYYY-MM-DD
date_modified: YYYY-MM-DD
author: brightplace
---

# [Article Title - H1]

## [First H2 - opens with 40-60 word direct answer]

[Article body sections following brief outline...]

## Frequently Asked Questions About [Topic]

### [Question 1]
[40-60 word standalone answer]

### [Question 2]
[40-60 word standalone answer]

[...FAQ pairs per ranking-rules.md...]

---

## FAQ Schema (JSON-LD)
[FAQPage JSON-LD block]

## Article Schema (JSON-LD)
[Article JSON-LD block]

## WebPage Schema (JSON-LD)
[WebPage JSON-LD block with breadcrumb and speakable]
```

---

## 11. Pre-Publish QA Checklist

Run every check before submitting. If any check fails, fix it before outputting.

### Brand Compliance
- [ ] All checks in `memory/semantic/brand-rules.md` pass.

### SEO/AEO Compliance
- [ ] First sentence contains the primary keyword and begins answering the query
- [ ] Primary keyword appears in: H1, first sentence, first H2, meta description
- [ ] Meta description is under 155 characters and contains the primary keyword
- [ ] Every H2 section opens with its answer in the first sentence
- [ ] Every dollar figure and statistic has a date stamp `(as of Q2 YYYY)`

### Structure Compliance
- [ ] Only one H1 in the document
- [ ] H2/H3 structure matches the content brief outline exactly
- [ ] Word count is within the target range from the brief
- [ ] FAQ section meets `memory/semantic/ranking-rules.md` targets, each answer 40-60 words

### Linking Compliance
- [ ] 8-12 internal links to brightplace.ai/guides/ pages (real URLs from sitemap)
- [ ] 4-6 external links to authoritative sources (all with `target="_blank" rel="noopener"`)
- [ ] 3 brightplace CTA placements (after first H2, mid-article, end of article)
- [ ] No three consecutive sentences start with the same word

### Schema Compliance
- [ ] FAQPage JSON-LD schema present with all FAQ pairs (answers match word-for-word)
- [ ] Article JSON-LD schema present with correct dates and author
- [ ] WebPage JSON-LD schema present with breadcrumb and speakable
- [ ] All frontmatter fields are populated

### Content Quality (Google E-E-A-T 2026)
- [ ] Article demonstrates first-hand experience (brightplace data framing)
- [ ] At least one honest tradeoff or limitation included
- [ ] Technical terms defined at first use
- [ ] Structured comparison included where relevant
- [ ] No symmetric AI-pattern structures (varied section lengths)
- [ ] No filler introductions or conclusion that restates the intro

---

## 12. Content Output

See `memory/semantic/cms-config.md` for the output location, frontmatter schema, body
rules and routing. Webflow is retired — finished articles go to
`brightplace content/<collection>/` as `.md` + `.html` + image, and the git commit
publishes them.

---

## 13. brightplace Sitemap (Internal Link Reference)

See `memory/semantic/link-registry.md` for inventories and exact-path checks.
Consult `memory/episodic/link-failures.md` for newer observations.
