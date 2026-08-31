# 03 — Pipeline Detail

## The Content Pipeline (Step by Step)

### Step 1: Keyword Research
**Agent:** keyword-agent.md
**Input:** Operator ID (properties, markets, competitors from Supabase)
**Process:**
1. Pull operator's property data from database
2. Call Semrush API for keyword suggestions (phrase_related, phrase_questions)
3. Call Semrush API for KD + volume on each keyword (phrase_kdi, phrase_these)
4. Categorize into 4 tiers (Quick Wins, Long Tail, Informational, Gap)
5. Filter: only keywords where Google shows editorial results (not listings)
6. Filter: KD < 40 (realistic to rank)
7. Sort by volume/KD ratio (best opportunities first)
8. Save to `keywords` table with status = "suggested"

**Output:** List of 10-20 keywords per operator with real volume + KD

**Frequency:** Monthly (or on-demand)

---

### Step 2: Operator Approval
**Agent:** None (UI interaction)
**Input:** Keyword list from Step 1
**Process:**
1. Operator sees keywords in dashboard table
2. Each row shows: keyword, volume, KD, suggested title, reasoning
3. Operator clicks "Approve" or "Reject" per keyword
4. Approved keywords status → "approved"

**Output:** Approved keywords ready for writing

---

### Step 3: Brief Generation
**Agent:** brief-agent.md
**Input:** Approved keyword + operator context + property data
**Process:**
1. Take the keyword and pull operator brand/context from Supabase
2. Call Claude API with Brief Agent prompt + keyword data
3. Claude generates: H1, SEO title, H2 structure, content gaps, FAQ suggestions, entity list
4. Brief saved to `articles` table with status = "draft", content = brief JSON

**Output:** Complete content brief (no human writing needed)

**Trigger:** Automatic when keyword approved

---

### Step 4: Article Writing
**Agent:** writing-agent.md
**Input:** Brief + brand guidelines + property data
**Process:**
1. Load brief, brand context, and property data
2. Call Claude API with Writing Agent prompt + all context
3. Claude writes 1,500-2,500 word article following all SEO/AEO rules
4. Article saved as markdown to `articles` table, status = "written"

**Output:** Complete article in markdown

**Trigger:** Automatic after brief generated

---

### Step 5: Quality Assurance
**Agent:** qa-agent.md
**Input:** Written article + property data (for accuracy checking)
**Process:**
1. Call Claude API with QA Agent prompt + article + property data
2. Claude runs 6-section check:
   - Brand compliance
   - SEO structure
   - Content accuracy (prices, plans, addresses match data)
   - Link audit
   - Infrastructure
   - AI readiness
3. If all PASS → status = "qa_passed"
4. If any FAIL → Claude auto-fixes, re-runs failed checks

**Output:** QA report. Article status updated.

**Trigger:** Automatic after writing complete

---

### Step 6: Image Generation
**Agent:** image-agent.md
**Input:** Article title + primary keyword + property type
**Process:**
1. Call Claude API with Image Agent prompt
2. Claude generates 3 image prompt options
3. Option A auto-selected (or operator chooses in dashboard)
4. Image prompt sent to image generation service (DALL-E, Midjourney, or manual)

**Output:** Featured image prompt + alt text

**Trigger:** Automatic after QA passes

---

### Step 7: Publishing
**Agent:** publish-agent.md
**Input:** Article (markdown) + image + metadata
**Process:**
1. Convert markdown to format required by operator's site
2. For Next.js/Vercel: create data file, update sitemap, update llms.txt, git push
3. For Webflow: call Webflow CMS API
4. For WordPress: call WP REST API
5. Verify live URL loads correctly
6. Update `articles` table: status = "published", published_url = URL

**Output:** Live article at operator's site

**Trigger:** Automatic after image ready (or operator clicks "Publish" in dashboard)

---

### Step 8: Analytics Tracking
**Agent:** None (automated data collection)
**Input:** Published article URLs
**Process:**
1. Daily: pull page views from Vercel Analytics API
2. Daily: pull search impressions/clicks from Google Search Console API
3. Weekly: check AI citation (search ChatGPT/Perplexity for related queries)
4. Save to `analytics` table

**Output:** Dashboard data for operator reports

**Trigger:** Automated daily/weekly cron job

---

## Pipeline Timing

| Step | Duration | Trigger |
|---|---|---|
| Keyword Research | 2-3 min (API calls) | Monthly or on-demand |
| Operator Approval | 1-5 min (human) | After research |
| Brief Generation | 30 sec (Claude API) | Auto after approval |
| Article Writing | 2-3 min (Claude API) | Auto after brief |
| QA | 1 min (Claude API) | Auto after writing |
| Image | 30 sec (prompt) + manual generation | Auto after QA |
| Publishing | 1-2 min (git push + deploy) | Auto or manual |
| Analytics | Continuous | Automated |

**Total: Keyword approved → Article live in ~10 minutes** (excluding image generation)

---

## Error Handling

| Error | Action |
|---|---|
| Semrush API fails | Retry 3x, then fall back to manual research |
| Claude API fails | Retry 3x, then queue for later |
| QA fails | Auto-fix and re-run. If fails 3x, flag for human review |
| Git push fails | Retry, then alert developer team |
| Published URL 404 | Alert immediately, check deploy logs |
