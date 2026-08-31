# Module 2: Research & Writing Pipeline

**Priority:** MVP — ships first (alongside Module 1)
**Depends on:** Module 1 (selected keyword) + Project setup (business context)
**Feeds into:** CMS Publish module (Phase 2)

---

## What This Module Does

Takes a selected keyword and runs the full content production pipeline: SERP research → AI Mode analysis → Reddit research → Content brief → Article writing → QA check. This is the core engine of the product.

---

## The Pipeline (7 Steps)

```
Selected Keyword
    ↓
Step 1: SERP Analysis Agent
    ↓ (runs in parallel with steps 2-4)
Step 2: AI Mode Analysis Agent
    ↓
Step 3: PAA Extraction Agent
    ↓
Step 4: Reddit Research Agent
    ↓
Step 5: Brief Generator Agent (takes output from 1-4 + business context)
    ↓
Step 6: Writing Agent (takes brief + Reddit insights)
    ↓
Step 7: QA Agent (validates everything)
    ↓
Output: Complete article ready for export or publish
```

---

## User Flow

```
User clicks "Research & Write" on a selected keyword
    ↓
Screen: Research Progress (live updates via WebSocket)
    ↓
Screen: Brief Preview (user reviews, edits, approves)
    ↓
Screen: Article Editor (live preview + SEO score)
    ↓
Screen: QA Report (pass/fail, fix issues)
    ↓
Screen: Export / Publish
```

---

## Screen 1: Research Progress

When user clicks "Research & Write," they see live progress:

```
┌─────────────────────────────────────────────────────────────┐
│  RESEARCHING: "what does income restricted mean"             │
│                                                              │
│  ┌────────────────────────────────────────────┬────────┐    │
│  │ SERP Analysis                              │  Done  │    │
│  │ Analyzed 10 competitors, avg 1,400 words   │   ✓    │    │
│  ├────────────────────────────────────────────┼────────┤    │
│  │ AI Mode Analysis                           │  Done  │    │
│  │ ChatGPT: not citing you. Claude: not       │   ✓    │    │
│  │ citing you. 3 citation gaps found.         │        │    │
│  ├────────────────────────────────────────────┼────────┤    │
│  │ PAA Questions                              │  Done  │    │
│  │ 12 questions found, 8 unanswered by       │   ✓    │    │
│  │ competitors                                │        │    │
│  ├────────────────────────────────────────────┼────────┤    │
│  │ Reddit Research                            │Running │    │
│  │ Found 6 threads, analyzing comments...     │   ⟳    │    │
│  ├────────────────────────────────────────────┼────────┤    │
│  │ Brief Generation                           │Waiting │    │
│  │                                            │   ○    │    │
│  └────────────────────────────────────────────┴────────┘    │
│                                                              │
│  Estimated time remaining: ~45 seconds                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Screen 2: Research Report (expandable)

After research completes, user can review findings before brief:

```
┌─────────────────────────────────────────────────────────────┐
│  RESEARCH REPORT: "what does income restricted mean"         │
│                                                              │
│  [SERP Analysis ▼]                                          │
│  ┌────────────────────────────────────────────────────┐     │
│  │ Top 10 Results:                                    │     │
│  │ 1. leaserunner.com (3,200 words, definition guide) │     │
│  │ 2. lifestepsusa.org (2,100 words, guide)           │     │
│  │ 3. apartmentguide.com (1,800 words, guide)         │     │
│  │ ...                                                │     │
│  │ Content Gaps Found:                                │     │
│  │ • No competitor explains LIHTC rent formula        │     │
│  │ • No competitor covers minimum income requirement  │     │
│  │ • No competitor explains 2008 HERA exemption       │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  [AI Mode Analysis ▼]                                       │
│  ┌────────────────────────────────────────────────────┐     │
│  │ ChatGPT says: [summary]                            │     │
│  │ ChatGPT cites: HUD.gov, affordablehousing.com      │     │
│  │ YOU cited by ChatGPT: NO ✗                         │     │
│  │                                                    │     │
│  │ Claude says: [summary]                             │     │
│  │ Claude cites: HUD.gov, GoSection8.com              │     │
│  │ YOU cited by Claude: NO ✗                          │     │
│  │                                                    │     │
│  │ Citation Opportunity: First to publish LIHTC       │     │
│  │ rent formula + 2008 exemption = citation slot      │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  [PAA Questions ▼]  [Reddit Research ▼]                     │
│                                                              │
│  [Generate Brief →]                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Screen 3: Brief Preview & Editor

```
┌─────────────────────────────────────────────────────────────┐
│  CONTENT BRIEF                                               │
│                                                              │
│  ┌─ Title Options ──────────────────────────────────────┐   │
│  │ ○ What Income Restricted Means for Apartment Renters │   │
│  │ ● How Income Restricted Apartments Actually Work     │   │
│  │ ○ What Does Income Restricted Mean? A Renter's Guide │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─ H2 Structure (drag to reorder) ────────────────────┐   │
│  │ ≡ What Does Income Restricted Mean?                  │   │
│  │ ≡ How Does AMI Determine Eligibility?                │   │
│  │ ≡ What Is the Difference Between Income Restricted   │   │
│  │   and Income Based?                                  │   │
│  │ ≡ Who Qualifies for Income Restricted Apartments?    │   │
│  │ ≡ How Is Rent Calculated?                            │   │
│  │ ≡ What Happens If Your Income Goes Up?               │   │
│  │ ≡ How Do You Find and Apply?                         │   │
│  │ ≡ Frequently Asked Questions                         │   │
│  │ [+ Add Section]                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─ Content Gaps to Fill ──────────────────────────────┐   │
│  │ ✓ LIHTC 1.5-persons-per-bedroom rent formula        │   │
│  │ ✓ 2008 HERA recertification exemption               │   │
│  │ ✓ Minimum income requirements (2-2.5x rent)         │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─ FAQ Questions (10) ────────────────────────────────┐   │
│  │ ✓ Are income restricted apartments easier to get?   │   │
│  │ ✓ Does income restricted mean Section 8?            │   │
│  │ ✓ What does 80% AMI mean?                           │   │
│  │ ... (7 more)                                        │   │
│  │ [+ Add Question]                                    │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─ Rules ─────────────────────────────────────────────┐   │
│  │ DO: Question-format H2s, 10+ FAQs, 7+ internal     │   │
│  │     links, entity density 12+, date-stamp all $     │   │
│  │ DON'T: em dashes, "signal", banned phrases, ILS    │   │
│  │        citations, <ul><li> tags                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  [Edit Brief]  [Approve & Write →]                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Screen 4: Article Editor (Split View)

```
┌────────────────────────────────────┬────────────────────────┐
│  ARTICLE PREVIEW                   │  SEO SCORE: 87/100     │
│                                    │                        │
│  # What Income Restricted Means    │  ✓ Keyword in first    │
│  for Apartment Renters             │    sentence             │
│                                    │  ✓ Entity density: 14x │
│  Last reviewed: August 2026        │    (target: 12+)       │
│                                    │  ✓ FAQ count: 10       │
│  ## What Does Income Restricted    │    (target: 10+)       │
│  Mean?                             │  ⚠ Word count: 1,180   │
│                                    │    (target: 1,200+)    │
│  Income restricted means a rental  │  ✓ Internal links: 7   │
│  unit has a legal cap on both who  │  ✓ H2s: question format│
│  can move in and what the landlord │  ✓ No banned phrases   │
│  can charge...                     │  ✓ All $ date-stamped  │
│                                    │  ✓ No <ul><li> tags    │
│  [Click any section to edit]       │  ✓ Schema: 3 present   │
│                                    │                        │
│  ## How Does AMI Determine...      │  ┌──────────────────┐  │
│                                    │  │ ENTITY DENSITY   │  │
│  Area Median Income is the         │  │ income restricted │  │
│  household income at the midpoint  │  │ ████████████ 14x │  │
│  ...                               │  │ AMI              │  │
│                                    │  │ █████████ 10x    │  │
│                                    │  │ LIHTC            │  │
│                                    │  │ ██████ 6x        │  │
│                                    │  │ HUD              │  │
│                                    │  │ ████ 4x          │  │
│                                    │  └──────────────────┘  │
│                                    │                        │
│                                    │  [Regenerate All]      │
│                                    │  [Run QA →]            │
│                                    │  [Export ▼]            │
├────────────────────────────────────┴────────────────────────┤
│  Section Actions:                                           │
│  [↻ Regenerate This Section] [✎ Edit Manually] [✗ Delete]  │
└─────────────────────────────────────────────────────────────┘
```

**Key UX Features:**
- Click any H2 section → inline edit or regenerate just that section
- SEO score updates live as content changes
- Entity density bar chart shows real-time counts
- Warning badges for issues (word count low, missing date stamps, etc.)

---

## Screen 5: QA Report

```
┌─────────────────────────────────────────────────────────────┐
│  QA REPORT                                                   │
│                                                              │
│  Overall: 22/24 checks passed                                │
│                                                              │
│  ┌─ Brand Compliance ──────────────────────────── PASS ──┐  │
│  │ ✓ Brand name lowercase (7 instances)                   │  │
│  │ ✓ No em dashes                                         │  │
│  │ ✓ No banned word "signal"                              │  │
│  │ ✓ No banned phrases                                    │  │
│  │ ✓ No ILS citations                                     │  │
│  │ ✓ Title framing (no superlatives)                      │  │
│  │ ✓ Fair Housing compliant                               │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌─ SEO Structure ─────────────────────────── 1 WARNING ─┐  │
│  │ ✓ Primary keyword in first sentence                    │  │
│  │ ✓ Entity density within range                          │  │
│  │ ✓ Meta description: 149 chars (under 155)              │  │
│  │ ✓ SEO title: 47 chars, differs from H1                 │  │
│  │ ✓ Heading hierarchy correct                            │  │
│  │ ✓ Question-format H2s                                  │  │
│  │ ✓ No markdown tables                                   │  │
│  │ ✓ All figures date-stamped                             │  │
│  │ ✓ 10 FAQ pairs present                                 │  │
│  │ ⚠ Word count: 1,180 (target: 1,200-1,400)             │  │
│  │ ✓ All 3 schemas present                                │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌─ Link Audit ────────────────────────────── 1 WARNING ─┐  │
│  │ ✓ 7 internal links (all valid)                         │  │
│  │ ✓ 3 CTAs using app.brightplace.ai                      │  │
│  │ ✓ No /knowledgebase/ paths                             │  │
│  │ ⚠ External: huduser.gov (flag for manual verification) │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌─ Math Verification ────────────────────────── PASS ───┐  │
│  │ ✓ $75,660 x 30% / 12 = $1,891/mo (correct)            │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌─ AI Watermark Risk ─────────────────────── MEDIUM ────┐  │
│  │ ⚠ Content is 100% AI-generated                         │  │
│  │ Recommendation: edit intro + conclusion manually        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  [Auto-Fix Issues]  [Approve]  [Export ▼]  [Generate Image] │
└─────────────────────────────────────────────────────────────┘
```

---

## Agent Definitions

### Agent 1: SERP Analysis Agent

```
Input:  keyword (string)
Tools:  DataForSEO SERP API
Output: {
    top_10_results: [
        { url, title, domain, word_count, headings[], content_format, da_score }
    ],
    featured_snippet: { present, holder_url, format, word_count },
    ai_overview: { present, citations[] },
    paa_questions: string[],
    content_gaps: string[],
    avg_word_count: number,
    dominant_format: string
}
```

### Agent 2: AI Mode Analysis Agent

```
Input:  keyword (string), user_domain (string)
Tools:  OpenAI API, Anthropic API, DataForSEO (AI Overview)
Output: {
    chatgpt: { response, citations[], cites_user: bool },
    claude: { response, citations[], cites_user: bool },
    ai_overview: { present, citations[], cites_user: bool },
    citation_gaps: string[],
    recommendation: string
}
```

### Agent 3: Reddit Research Agent

```
Input:  keyword (string), niche_subreddits (string[])
Tools:  DataForSEO SERP (site:reddit.com), Reddit JSON API, Claude (analysis)
Output: {
    threads_analyzed: number,
    questions: [{ text, subreddit, upvotes }],
    pain_points: string[],
    real_numbers: [{ stat, context }],
    misconceptions: [{ myth, reality }],
    language_patterns: [{ renter_says, industry_says }],
    enrichment_recommendations: string[]
}
```

### Agent 4: Brief Generator Agent

```
Input:  research_report, reddit_report, business_context, existing_articles[]
Tools:  Claude API
Output: {
    title_options: string[3],
    h2_structure: [{ heading, writing_instruction, content_gap: bool }],
    entity_targets: { entity: count }[],
    faq_questions: string[10],
    internal_links: string[],
    cta_placements: string[3],
    do_rules: string[],
    dont_rules: string[],
    word_count_target: { min, max },
    schema_types: string[]
}
```

### Agent 5: Writing Agent

```
Input:  approved_brief, reddit_insights, business_context
Tools:  Claude API
System prompt includes:
  - Brand voice and rules from business_context
  - Ranking optimization rules (question H2s, entity density, snippet paragraphs)
  - Content gaps to fill from brief
  - Reddit language patterns to incorporate
  - Internal links to include
Output: {
    content_md: string (full markdown article),
    content_html: string (HTML for CMS),
    schemas: { faq: {}, article: {}, webpage: {} },
    seo_score: number,
    entity_counts: { entity: count }[],
    word_count: number
}
```

### Agent 6: QA Agent

```
Input:  article (md + html), brief, business_context, qa_rules[]
Tools:  Claude API, URL checker, math parser
Output: {
    overall_score: number,
    sections: {
        brand_compliance: { pass: bool, checks: [] },
        seo_structure: { pass: bool, checks: [] },
        link_audit: { pass: bool, internal: [], external: [], ctas: [] },
        math_verification: { pass: bool, calculations: [] },
        watermark_risk: { level: "low"|"medium"|"high", recommendation: string }
    },
    auto_fixable_issues: [],
    manual_review_needed: []
}
```

---

## Business Context Object (passed to every agent)

```json
{
    "domain": "brightplace.ai",
    "niche": "Apartment rentals & renter education",
    "brand_name": "brightplace",
    "brand_rules": {
        "name_case": "always lowercase",
        "banned_words": ["signal"],
        "banned_phrases": ["deep dive", "navigate", "landscape", ...],
        "cta_domain": "app.brightplace.ai",
        "brand_domain": "brightplace.ai",
        "url_path": "/resources/",
        "fair_housing": true
    },
    "voice": "Knowledgeable friend giving honest advice. Confident, specific, never promotional.",
    "existing_articles": [
        { "slug": "prorated-rent", "keyword": "what is prorated rent" },
        { "slug": "income-based-homes-charlotte-nc", "keyword": "income based homes charlotte" },
        ...
    ],
    "qa_rules": [
        { "type": "no_ul_li", "description": "Never use <ul><li> in CMS HTML" },
        { "type": "date_stamp", "description": "Date-stamp all dollar figures" },
        ...
    ]
}
```

---

## API Endpoints (Backend)

```
# Research
POST   /api/keywords/{id}/research
       → Triggers all 4 research agents in parallel
       → Returns job_id for WebSocket tracking

GET    /api/jobs/{job_id}/status
       → Returns current status of all agents

GET    /api/keywords/{id}/research-report
       → Returns compiled research report

# Brief
POST   /api/keywords/{id}/brief
       → Generate brief from research report
       → Returns brief JSON

PUT    /api/briefs/{id}
       → Update brief (user edits)

POST   /api/briefs/{id}/approve
       → Mark brief as approved, ready for writing

# Writing
POST   /api/briefs/{id}/write
       → Triggers writing agent
       → Returns job_id for WebSocket tracking

GET    /api/articles/{id}
       → Returns article content (md, html, schemas)

PUT    /api/articles/{id}/sections/{section_index}
       → Regenerate or update a specific section

# QA
POST   /api/articles/{id}/qa
       → Run QA checks
       → Returns QA report

POST   /api/articles/{id}/qa/auto-fix
       → Auto-fix simple issues

# Export
GET    /api/articles/{id}/export?format=md
GET    /api/articles/{id}/export?format=html
GET    /api/articles/{id}/export?format=json
```

---

## Database Tables for This Module

```sql
-- Research Reports
CREATE TABLE research_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keyword_id UUID REFERENCES selected_keywords(id),
    serp_analysis JSONB,
    ai_mode_analysis JSONB,
    paa_questions JSONB,
    reddit_research JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Briefs
CREATE TABLE briefs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keyword_id UUID REFERENCES selected_keywords(id),
    research_report_id UUID REFERENCES research_reports(id),
    title TEXT,
    structure JSONB,         -- H2s, FAQs, entities, rules
    status TEXT DEFAULT 'draft',  -- draft, approved, writing, completed
    created_at TIMESTAMPTZ DEFAULT NOW(),
    approved_at TIMESTAMPTZ
);

-- Articles
CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brief_id UUID REFERENCES briefs(id),
    content_md TEXT,
    content_html TEXT,
    schemas JSONB,
    seo_score INTEGER,
    word_count INTEGER,
    entity_counts JSONB,
    qa_report JSONB,
    status TEXT DEFAULT 'draft',  -- draft, qa_passed, exported, published
    published_url TEXT,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Jobs (for async agent tracking)
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type TEXT NOT NULL,       -- research, brief, writing, qa
    keyword_id UUID,
    status TEXT DEFAULT 'pending',  -- pending, running, completed, failed
    progress JSONB DEFAULT '{}',    -- { agent_name: status }
    result JSONB,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Acceptance Criteria

- [ ] User clicks "Research & Write" and sees live progress for all 4 research agents
- [ ] Research completes within 90 seconds for all agents
- [ ] Research report is viewable and expandable
- [ ] Brief generates with correct structure (titles, H2s, FAQs, entities, rules)
- [ ] User can edit brief (reorder H2s, add/remove FAQs, change title)
- [ ] User can approve brief to trigger writing
- [ ] Article generates with all ranking optimizations applied
- [ ] Live SEO score updates as content changes
- [ ] User can click any section to regenerate or edit manually
- [ ] QA runs automatically and shows pass/fail report
- [ ] Auto-fix works for simple issues
- [ ] Export works in MD, HTML, and JSON formats
- [ ] Watermark risk assessment shows on QA report
- [ ] All agents use business context for brand-specific rules
- [ ] WebSocket progress updates work without delays
