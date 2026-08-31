# Data Sources

**Last Updated:** August 2026

---

## Where Keywords, SERP, and Competitor Data Come From

### Recommended: Hybrid Approach

```
Keyword Data:        DataForSEO (cheap, real-time)
SERP Scraping:       DataForSEO + custom Playwright scraper
Competitor Analysis: DataForSEO Labs API
PAA Questions:       Extracted from SERP results (DataForSEO)
AI Mode Analysis:    Direct API calls to ChatGPT + Claude
Reddit Research:     Custom scraper (Reddit RSS + JSON API)
Site Audit:          Custom crawler (Playwright + Lighthouse)
Image Generation:    OpenAI DALL-E 3 or Ideogram API
```

---

## Option A: Semrush API (Premium)

| What You Get | Endpoint | Cost Per Call |
|---|---|---|
| Keyword volume + KD + intent | /keywords_batch | $0.01-0.05 |
| Competitor keyword gaps | /domain_domains | $0.05 |
| SERP results for a keyword | /keywords_serps | $0.02 |
| Backlink data | /backlinks_overview | $0.02 |
| Site audit data | /audit | Custom pricing |

**Pros:** Most comprehensive data, trusted by SEOs, includes intent classification
**Cons:** Expensive at scale ($200-500/mo API minimum), rate limited

---

## Option B: DataForSEO API (Budget-Friendly) — RECOMMENDED

| What You Get | Endpoint | Cost Per Call |
|---|---|---|
| Keyword volume + KD | /keywords_data | $0.002 |
| SERP results (top 100) | /serp/google/organic | $0.002 |
| Competitor keywords | /dataforseo_labs/competitors | $0.003 |
| People Also Ask | Included in SERP results | $0.000 |
| AI Overview detection | Included in SERP results | $0.000 |
| Domain keyword gap | /dataforseo_labs/domain_intersection | $0.003 |
| Long-tail suggestions | /dataforseo_labs/keyword_suggestions | $0.002 |
| Site crawl/audit | /on_page/task_post | $0.004 |

**Pros:** 10-25x cheaper than Semrush, real-time SERP data, includes AI Overview detection
**Cons:** Less brand recognition, some data less refined

**Monthly cost estimate:** $50-150 for 10,000-25,000 API calls

---

## AI Mode Analysis (Custom — Our Unique Feature)

Nobody offers this. Here's how it works:

```python
async def analyze_ai_mode(keyword: str) -> dict:
    """Query AI engines and analyze what they say + cite."""

    # 1. Ask ChatGPT
    chatgpt_response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": keyword}]
    )

    # 2. Ask Claude
    claude_response = await anthropic_client.messages.create(
        model="claude-sonnet-4-6",
        messages=[{"role": "user", "content": keyword}]
    )

    # 3. Get Google AI Overview via DataForSEO SERP
    serp_data = await dataforseo_client.serp(keyword)
    ai_overview = serp_data.get("ai_overview", None)

    # 4. Extract citations from all three
    chatgpt_citations = extract_urls(chatgpt_response.content)
    claude_citations = extract_urls(claude_response.content[0].text)
    aio_citations = extract_urls(ai_overview) if ai_overview else []

    # 5. Check if user's domain is cited anywhere
    all_citations = chatgpt_citations + claude_citations + aio_citations
    user_cited = any(user_domain in url for url in all_citations)

    # 6. Identify what's missing (citation gaps)
    gaps = identify_content_gaps(
        chatgpt_response, claude_response, ai_overview
    )

    return {
        "chatgpt": {
            "response": chatgpt_response.content,
            "citations": chatgpt_citations,
            "cites_user": user_domain in str(chatgpt_citations),
        },
        "claude": {
            "response": claude_response.content[0].text,
            "citations": claude_citations,
            "cites_user": user_domain in str(claude_citations),
        },
        "ai_overview": {
            "present": ai_overview is not None,
            "citations": aio_citations,
            "cites_user": user_domain in str(aio_citations),
        },
        "user_cited_anywhere": user_cited,
        "citation_gaps": gaps,
        "competitor_citations": list(set(all_citations)),
    }
```

---

## Reddit Research (Custom)

```python
async def research_reddit(keyword: str, subreddits: list = None) -> dict:
    """Search Reddit for real discussions about the keyword."""

    # Default subreddits for rental/housing topics
    if not subreddits:
        subreddits = [
            "ApartmentHunting", "renting", "personalfinance",
            "FirstTimeRenter", "Frugal"
        ]

    results = []

    # 1. Search via Google (site:reddit.com keyword)
    search_results = await dataforseo_client.serp(
        f"site:reddit.com {keyword}",
        num=20
    )

    # 2. For each thread, fetch via Reddit JSON API
    for result in search_results:
        if "reddit.com" not in result.get("url", ""):
            continue

        thread_url = result["url"].rstrip("/") + ".json"
        try:
            thread_data = await fetch_json(thread_url, headers={
                "User-Agent": "ResearchBot/1.0"
            })

            # 3. Extract top comments (sorted by upvotes)
            comments = extract_top_comments(
                thread_data, min_upvotes=5, max_comments=20
            )

            results.append({
                "title": result.get("title"),
                "url": result.get("url"),
                "subreddit": extract_subreddit(result["url"]),
                "comments": comments,
            })
        except Exception:
            continue

    # 4. Use Claude to analyze all collected discussions
    analysis = await anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        messages=[{
            "role": "user",
            "content": f"""Analyze these Reddit discussions about "{keyword}".
            Extract:
            1. Real questions users ask (exact phrasing)
            2. Pain points and frustrations
            3. Specific numbers cited (dollars, timeframes)
            4. Common misconceptions
            5. Language patterns (how real people talk about this)
            6. Heavily upvoted advice

            Discussions: {json.dumps(results[:10])}"""
        }]
    )

    return {
        "threads_analyzed": len(results),
        "subreddits_covered": list(set(r["subreddit"] for r in results)),
        "analysis": analysis.content[0].text,
        "raw_threads": results,
    }
```

---

## Site Audit (Custom Crawler)

```python
async def run_site_audit(domain: str) -> dict:
    """Crawl site and check for SEO + AI readiness issues."""

    issues = []

    # 1. Check robots.txt for AI crawler access
    robots = await fetch_text(f"https://{domain}/robots.txt")
    ai_crawlers = ["GPTBot", "ClaudeBot", "PerplexityBot", "OAI-SearchBot"]
    for crawler in ai_crawlers:
        if f"User-agent: {crawler}" in robots and "Disallow: /" in robots:
            issues.append({
                "type": "ai_access",
                "severity": "high",
                "message": f"{crawler} is blocked in robots.txt"
            })

    # 2. Check for llms.txt
    llms_txt = await fetch_text(f"https://{domain}/llms.txt")
    if not llms_txt:
        issues.append({
            "type": "ai_access",
            "severity": "medium",
            "message": "No llms.txt file found"
        })

    # 3. Check Bing indexation
    bing_results = await dataforseo_client.serp(
        f"site:{domain}", search_engine="bing"
    )
    if not bing_results:
        issues.append({
            "type": "indexation",
            "severity": "high",
            "message": "Site not indexed in Bing (ChatGPT data source)"
        })

    # 4. Crawl pages for schema, content quality, links
    pages = await crawl_sitemap(domain)
    for page in pages:
        html = await fetch_html(page["url"])

        # Check for FAQ schema
        if "FAQPage" not in html:
            issues.append({
                "type": "schema",
                "severity": "low",
                "page": page["url"],
                "message": "Missing FAQPage schema"
            })

        # Check content length
        text = extract_text(html)
        if len(text.split()) < 300:
            issues.append({
                "type": "content",
                "severity": "medium",
                "page": page["url"],
                "message": f"Thin content ({len(text.split())} words)"
            })

    # 5. Calculate health score
    score = calculate_health_score(issues)

    return {
        "score": score,
        "issues": issues,
        "pages_crawled": len(pages),
        "ai_readiness": {
            "llms_txt": bool(llms_txt),
            "ai_crawlers_allowed": check_ai_access(robots),
            "bing_indexed": bool(bing_results),
        }
    }
```

---

## Cost Summary Per Article

| Service | Cost |
|---|---|
| DataForSEO (keyword + SERP + competitor data) | $0.10-0.20 |
| Claude API (research + brief + writing + QA) | $0.30-0.80 |
| OpenAI API (AI Mode analysis) | $0.05-0.15 |
| OpenAI API (image generation) | $0.04-0.08 |
| Reddit scraping | $0.00 (free) |
| **Total per article** | **$0.50-1.25** |

At $149/mo plan with 20 articles = $10-25 in API costs = ~85% margin
