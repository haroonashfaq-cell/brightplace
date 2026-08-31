import json
import logging
from datetime import datetime

import httpx
from anthropic import Anthropic
from supabase import create_client

from app.config import get_settings
from app.services.dataforseo import dataforseo_client

logger = logging.getLogger(__name__)


def _get_supabase():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_key)


def _get_anthropic():
    settings = get_settings()
    return Anthropic(api_key=settings.anthropic_api_key)


async def run_research(
    project_id: str,
    keyword_id: str,
    keyword: str,
    user_id: str,
) -> dict:
    """Run full research pipeline: SERP analysis + PAA + Reddit."""
    sb = _get_supabase()

    # Create or update research report
    existing = (
        sb.table("research_reports")
        .select("id")
        .eq("keyword_id", keyword_id)
        .eq("project_id", project_id)
        .execute()
    )

    if existing.data:
        report_id = existing.data[0]["id"]
        sb.table("research_reports").update({
            "status": "running",
            "updated_at": datetime.utcnow().isoformat(),
        }).eq("id", report_id).execute()
    else:
        result = sb.table("research_reports").insert({
            "keyword_id": keyword_id,
            "project_id": project_id,
            "keyword": keyword,
            "status": "running",
        }).execute()
        report_id = result.data[0]["id"]

    # Update pipeline job
    _update_job(sb, project_id, keyword_id, "research", "running")

    try:
        # Run all three research steps
        serp_data = await _run_serp_analysis(keyword)
        paa_data = await _extract_paa(keyword, serp_data)
        reddit_data = await _run_reddit_research(keyword)

        # Save results
        sb.table("research_reports").update({
            "serp_data": serp_data,
            "paa_data": paa_data,
            "reddit_data": reddit_data,
            "status": "completed",
            "updated_at": datetime.utcnow().isoformat(),
        }).eq("id", report_id).execute()

        _update_job(sb, project_id, keyword_id, "research", "done", {
            "report_id": report_id,
        })

        # Update selected keyword status
        sb.table("selected_keywords").update({
            "status": "researched",
        }).eq("id", keyword_id).execute()

        return _get_report(sb, report_id)

    except Exception as e:
        logger.error(f"Research failed for '{keyword}': {e}")
        sb.table("research_reports").update({
            "status": "failed",
            "updated_at": datetime.utcnow().isoformat(),
        }).eq("id", report_id).execute()
        _update_job(sb, project_id, keyword_id, "research", "failed", error=str(e))
        raise


async def get_research_report(
    project_id: str,
    keyword_id: str,
    user_id: str,
) -> dict | None:
    """Get research report for a keyword."""
    sb = _get_supabase()
    result = (
        sb.table("research_reports")
        .select("*")
        .eq("keyword_id", keyword_id)
        .eq("project_id", project_id)
        .execute()
    )
    if not result.data:
        return None
    return result.data[0]


# ============================================================
# SERP Analysis
# ============================================================

async def _run_serp_analysis(keyword: str) -> dict:
    """Analyze SERP results for the keyword via DataForSEO."""
    try:
        data = await dataforseo_client._post(
            "/serp/google/organic/live/advanced",
            [{
                "keyword": keyword,
                "location_code": 2840,
                "language_code": "en",
                "depth": 10,
            }]
        )

        organic_results = []
        featured_snippet = None
        paa_questions = []

        tasks = data.get("tasks", [])
        if tasks and tasks[0].get("result"):
            for res in tasks[0]["result"]:
                for item in res.get("items", []):
                    item_type = item.get("type", "")

                    if item_type == "organic":
                        organic_results.append({
                            "position": item.get("rank_absolute", 0),
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "description": item.get("description", ""),
                            "domain": item.get("domain", ""),
                        })

                    elif item_type == "featured_snippet":
                        featured_snippet = {
                            "title": item.get("title", ""),
                            "description": item.get("description", ""),
                            "url": item.get("url", ""),
                        }

                    elif item_type == "people_also_ask":
                        for paa_item in item.get("items", []):
                            paa_questions.append(paa_item.get("title", ""))

        return {
            "organic_results": organic_results[:10],
            "featured_snippet": featured_snippet,
            "paa_questions_raw": paa_questions,
            "total_results": len(organic_results),
        }

    except Exception as e:
        logger.error(f"SERP analysis failed for '{keyword}': {e}")
        return {"organic_results": [], "featured_snippet": None, "paa_questions_raw": [], "total_results": 0}


# ============================================================
# PAA Extraction
# ============================================================

async def _extract_paa(keyword: str, serp_data: dict) -> dict:
    """Extract and analyze PAA questions using Claude."""
    paa_raw = serp_data.get("paa_questions_raw", [])
    organic = serp_data.get("organic_results", [])

    competitor_titles = [r.get("title", "") for r in organic[:10]]
    competitor_descriptions = [r.get("description", "") for r in organic[:10]]

    try:
        client = _get_anthropic()
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": f"""Analyze the People Also Ask questions for the keyword "{keyword}".

PAA questions found in SERP:
{json.dumps(paa_raw, indent=2)}

Top 10 competitor titles:
{json.dumps(competitor_titles, indent=2)}

Top 10 competitor descriptions:
{json.dumps(competitor_descriptions, indent=2)}

Return a JSON object with:
1. "questions" — array of objects with:
   - "question": the PAA question
   - "competitor_answers": true if competitors seem to answer this based on titles/descriptions
   - "gap": true if this is a content gap (competitors don't cover it well)
   - "priority": "high", "medium", or "low" based on relevance to the keyword
2. "additional_questions" — array of 5-10 additional questions users might ask about this topic that weren't in PAA

Return ONLY valid JSON, no markdown."""
            }],
        )

        text = message.content[0].text.strip()
        # Clean potential markdown wrapping
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        return json.loads(text)

    except Exception as e:
        logger.error(f"PAA extraction failed: {e}")
        # Fallback: return raw PAA questions
        return {
            "questions": [
                {"question": q, "competitor_answers": False, "gap": True, "priority": "medium"}
                for q in paa_raw
            ],
            "additional_questions": [],
        }


# ============================================================
# Reddit Research
# ============================================================

async def _run_reddit_research(keyword: str) -> dict:
    """Research Reddit threads about the keyword for real user insights."""
    try:
        # Step 1: Find Reddit threads via DataForSEO SERP
        reddit_urls = await _find_reddit_threads(keyword)

        if not reddit_urls:
            return _empty_reddit_data()

        # Step 2: Fetch thread content
        threads = []
        async with httpx.AsyncClient(timeout=15.0) as client:
            for url in reddit_urls[:8]:
                thread = await _fetch_reddit_thread(client, url)
                if thread:
                    threads.append(thread)

        if not threads:
            return _empty_reddit_data()

        # Step 3: Claude extracts insights
        return await _analyze_reddit_threads(keyword, threads)

    except Exception as e:
        logger.error(f"Reddit research failed for '{keyword}': {e}")
        return _empty_reddit_data()


async def _find_reddit_threads(keyword: str) -> list[str]:
    """Find relevant Reddit threads via DataForSEO SERP search."""
    try:
        data = await dataforseo_client._post(
            "/serp/google/organic/live/advanced",
            [{
                "keyword": f'site:reddit.com "{keyword}"',
                "location_code": 2840,
                "language_code": "en",
                "depth": 10,
            }]
        )

        urls = []
        tasks = data.get("tasks", [])
        if tasks and tasks[0].get("result"):
            for res in tasks[0]["result"]:
                for item in res.get("items", []):
                    if item.get("type") == "organic":
                        url = item.get("url", "")
                        if "reddit.com/r/" in url and "/comments/" in url:
                            urls.append(url)

        return urls[:8]

    except Exception as e:
        logger.error(f"Reddit thread search failed: {e}")
        return []


async def _fetch_reddit_thread(client: httpx.AsyncClient, url: str) -> dict | None:
    """Fetch a Reddit thread via JSON API."""
    try:
        # Reddit JSON API: append .json to URL
        json_url = url.rstrip("/") + ".json"
        resp = await client.get(
            json_url,
            headers={"User-Agent": "SEOResearchBot/1.0"},
            follow_redirects=True,
        )
        if resp.status_code != 200:
            return None

        data = resp.json()
        if not isinstance(data, list) or len(data) < 2:
            return None

        # Extract post
        post_data = data[0]["data"]["children"][0]["data"]
        title = post_data.get("title", "")
        selftext = post_data.get("selftext", "")[:1000]
        subreddit = post_data.get("subreddit", "")
        score = post_data.get("score", 0)

        # Extract top comments
        comments = []
        for child in data[1]["data"]["children"][:10]:
            if child.get("kind") != "t1":
                continue
            comment = child["data"]
            body = comment.get("body", "")[:500]
            if body and comment.get("score", 0) >= 1:
                comments.append({
                    "body": body,
                    "score": comment.get("score", 0),
                })

        return {
            "title": title,
            "selftext": selftext,
            "subreddit": subreddit,
            "score": score,
            "url": url,
            "comments": comments,
        }

    except Exception as e:
        logger.warning(f"Failed to fetch Reddit thread {url}: {e}")
        return None


async def _analyze_reddit_threads(keyword: str, threads: list[dict]) -> dict:
    """Use Claude to extract insights from Reddit threads."""
    # Prepare thread summaries for Claude
    thread_summaries = []
    for t in threads:
        summary = f"Subreddit: r/{t['subreddit']} (score: {t['score']})\n"
        summary += f"Title: {t['title']}\n"
        if t['selftext']:
            summary += f"Post: {t['selftext']}\n"
        summary += "Top comments:\n"
        for c in t['comments'][:5]:
            summary += f"  - (score {c['score']}) {c['body']}\n"
        thread_summaries.append(summary)

    try:
        client = _get_anthropic()
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": f"""Analyze these Reddit threads about "{keyword}" and extract insights for writing an SEO article.

THREADS:
{chr(10).join(thread_summaries)}

Return a JSON object with:
1. "pain_points" — array of real frustrations/problems users mention (5-10 items)
2. "real_numbers" — array of specific numbers, costs, timeframes users share (3-8 items)
3. "misconceptions" — array of common wrong beliefs users have (3-5 items)
4. "advice" — array of practical tips from experienced users (5-10 items)
5. "common_questions" — array of questions users frequently ask (5-8 items)
6. "sentiment" — overall sentiment: "positive", "negative", "mixed", or "neutral"
7. "thread_count" — number of threads analyzed

RULES:
- Extract genuinely useful data points, not generic statements
- Include specific numbers when users mention them (costs, timeframes, percentages)
- Focus on insights that would make an article more helpful than competitors

Return ONLY valid JSON, no markdown."""
            }],
        )

        text = message.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        result = json.loads(text)
        result["thread_count"] = len(threads)
        return result

    except Exception as e:
        logger.error(f"Reddit analysis failed: {e}")
        return _empty_reddit_data()


def _empty_reddit_data() -> dict:
    return {
        "pain_points": [],
        "real_numbers": [],
        "misconceptions": [],
        "advice": [],
        "common_questions": [],
        "sentiment": "neutral",
        "thread_count": 0,
    }


# ============================================================
# Helpers
# ============================================================

def _update_job(
    sb,
    project_id: str,
    keyword_id: str,
    step: str,
    status: str,
    result: dict | None = None,
    error: str | None = None,
):
    """Create or update a pipeline job."""
    existing = (
        sb.table("pipeline_jobs")
        .select("id")
        .eq("project_id", project_id)
        .eq("keyword_id", keyword_id)
        .eq("step", step)
        .execute()
    )

    now = datetime.utcnow().isoformat()
    update_data = {"status": status}

    if status == "running":
        update_data["started_at"] = now
    elif status in ("done", "failed"):
        update_data["completed_at"] = now

    if result is not None:
        update_data["result"] = result
    if error is not None:
        update_data["error"] = error

    if existing.data:
        sb.table("pipeline_jobs").update(update_data).eq("id", existing.data[0]["id"]).execute()
    else:
        sb.table("pipeline_jobs").insert({
            "project_id": project_id,
            "keyword_id": keyword_id,
            "step": step,
            **update_data,
        }).execute()


def _get_report(sb, report_id: str) -> dict:
    result = sb.table("research_reports").select("*").eq("id", report_id).single().execute()
    return result.data
