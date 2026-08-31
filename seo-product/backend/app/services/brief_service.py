import json
import logging
import re
from datetime import datetime

from anthropic import Anthropic
from supabase import create_client

from app.config import get_settings
from app.services.research_service import _update_job

logger = logging.getLogger(__name__)


def _get_supabase():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_key)


def _get_anthropic():
    settings = get_settings()
    return Anthropic(api_key=settings.anthropic_api_key)


async def generate_brief(
    project_id: str,
    keyword_id: str,
    user_id: str,
) -> dict:
    """Generate a content brief from research data."""
    sb = _get_supabase()

    # Get research report
    report = (
        sb.table("research_reports")
        .select("*")
        .eq("keyword_id", keyword_id)
        .eq("project_id", project_id)
        .single()
        .execute()
    )
    if not report.data:
        raise ValueError("No research report found. Run research first.")

    research = report.data
    keyword = research["keyword"]

    # Get project context
    project = sb.table("projects").select("*").eq("id", project_id).single().execute()
    project_data = project.data

    _update_job(sb, project_id, keyword_id, "brief", "running")

    try:
        brief_data = await _generate_brief_with_claude(
            keyword=keyword,
            serp_data=research.get("serp_data", {}),
            paa_data=research.get("paa_data", {}),
            reddit_data=research.get("reddit_data", {}),
            niche=project_data.get("niche", ""),
            domain=project_data.get("domain", ""),
            brand_context=project_data.get("brand_context", {}),
        )

        # Check for existing brief
        existing = (
            sb.table("briefs")
            .select("id")
            .eq("research_report_id", research["id"])
            .eq("project_id", project_id)
            .execute()
        )

        brief_record = {
            "research_report_id": research["id"],
            "project_id": project_id,
            "keyword": keyword,
            "title": brief_data.get("title", ""),
            "seo_title": brief_data.get("seo_title", ""),
            "meta_description": brief_data.get("meta_description", ""),
            "slug": brief_data.get("slug", ""),
            "outline": brief_data.get("outline", []),
            "target_keywords": brief_data.get("target_keywords", {}),
            "entities": brief_data.get("entities", []),
            "faqs": brief_data.get("faqs", []),
            "ctas": brief_data.get("ctas", []),
            "internal_links": brief_data.get("internal_links", []),
            "word_count_target": brief_data.get("word_count_target", 1500),
            "snippet_paragraph": brief_data.get("snippet_paragraph", ""),
            "status": "draft",
        }

        if existing.data:
            brief_id = existing.data[0]["id"]
            brief_record["updated_at"] = datetime.utcnow().isoformat()
            sb.table("briefs").update(brief_record).eq("id", brief_id).execute()
        else:
            result = sb.table("briefs").insert(brief_record).execute()
            brief_id = result.data[0]["id"]

        _update_job(sb, project_id, keyword_id, "brief", "done", {"brief_id": brief_id})

        return sb.table("briefs").select("*").eq("id", brief_id).single().execute().data

    except Exception as e:
        logger.error(f"Brief generation failed for '{keyword}': {e}")
        _update_job(sb, project_id, keyword_id, "brief", "failed", error=str(e))
        raise


async def get_brief(project_id: str, brief_id: str, user_id: str) -> dict | None:
    sb = _get_supabase()
    result = (
        sb.table("briefs")
        .select("*")
        .eq("id", brief_id)
        .eq("project_id", project_id)
        .execute()
    )
    return result.data[0] if result.data else None


async def update_brief(
    project_id: str, brief_id: str, user_id: str, updates: dict
) -> dict | None:
    sb = _get_supabase()
    update_data = {k: v for k, v in updates.items() if v is not None}
    if not update_data:
        return await get_brief(project_id, brief_id, user_id)

    update_data["updated_at"] = datetime.utcnow().isoformat()
    sb.table("briefs").update(update_data).eq("id", brief_id).eq("project_id", project_id).execute()
    return await get_brief(project_id, brief_id, user_id)


async def approve_brief(project_id: str, brief_id: str, user_id: str) -> dict | None:
    sb = _get_supabase()
    sb.table("briefs").update({
        "status": "approved",
        "updated_at": datetime.utcnow().isoformat(),
    }).eq("id", brief_id).eq("project_id", project_id).execute()
    return await get_brief(project_id, brief_id, user_id)


async def get_brief_by_keyword(project_id: str, keyword_id: str, user_id: str) -> dict | None:
    sb = _get_supabase()
    report = (
        sb.table("research_reports")
        .select("id")
        .eq("keyword_id", keyword_id)
        .eq("project_id", project_id)
        .execute()
    )
    if not report.data:
        return None

    result = (
        sb.table("briefs")
        .select("*")
        .eq("research_report_id", report.data[0]["id"])
        .eq("project_id", project_id)
        .execute()
    )
    return result.data[0] if result.data else None


# ============================================================
# Claude Brief Generation — Matching Real Brief Format
# ============================================================

async def _generate_brief_with_claude(
    keyword: str,
    serp_data: dict,
    paa_data: dict,
    reddit_data: dict,
    niche: str,
    domain: str,
    brand_context: dict,
) -> dict:
    """Generate a detailed content brief matching the production brief format."""
    organic = serp_data.get("organic_results", [])
    competitor_info = "\n".join([
        f"  {i+1}. {r.get('title', '')} — {r.get('url', '')} — {r.get('description', '')}"
        for i, r in enumerate(organic[:10])
    ])

    paa_questions = paa_data.get("questions", [])
    paa_info = "\n".join([
        f"  - {q.get('question', '')} (gap: {q.get('gap', False)}, priority: {q.get('priority', 'medium')})"
        for q in paa_questions
    ])

    additional_q = paa_data.get("additional_questions", [])

    reddit_points = reddit_data.get("pain_points", [])
    reddit_numbers = reddit_data.get("real_numbers", [])
    reddit_advice = reddit_data.get("advice", [])
    reddit_misconceptions = reddit_data.get("misconceptions", [])
    reddit_questions = reddit_data.get("common_questions", [])

    slug = re.sub(r'[^a-z0-9]+', '-', keyword.lower()).strip('-')
    brand_name = brand_context.get("brand_name", domain.replace("https://", "").replace("http://", "").split(".")[0])
    quarter = f"Q{(datetime.utcnow().month - 1) // 3 + 1} {datetime.utcnow().year}"

    client = _get_anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8000,
        messages=[{
            "role": "user",
            "content": f"""You are a Senior SEO, GEO & AEO Content Strategist. Generate a detailed content brief for the keyword "{keyword}".

CONTEXT:
- Domain: {domain}
- Niche: {niche}
- Brand: {brand_name}
- Current quarter: {quarter}

SERP DATA (top 10 organic results):
{competitor_info}

Featured snippet: {json.dumps(serp_data.get('featured_snippet'))}

PAA QUESTIONS:
{paa_info}

Additional questions identified:
{json.dumps(additional_q)}

REDDIT INSIGHTS:
Pain points: {json.dumps(reddit_points)}
Real numbers: {json.dumps(reddit_numbers)}
Misconceptions: {json.dumps(reddit_misconceptions)}
Practical advice: {json.dumps(reddit_advice)}
Common questions: {json.dumps(reddit_questions)}

---

Generate the brief as a JSON object following this EXACT structure. Be thorough, specific, and data-driven.

CRITICAL RULES FOR THE BRIEF:
1. WORD COUNT: Analyze competitor word counts from the SERP. Set word_count_target to match the SERP average. Typical: 1,100-1,500 words. NEVER exceed 1,500 unless competitors average 2,000+. Specify exact word count per H2 section.
2. Each H2 section gets 120-180 words of instruction with exact content to cover.
3. Identify 2-3 specific CONTENT GAPS that no competitor covers.
4. Every data point, dollar figure must note "(as of {quarter})".
5. FAQ answers must be exactly 40-60 words each.

Return this JSON:
{{
  "title": "H1 title (curation framing, no superlatives, contains primary keyword)",
  "seo_title": "SEO title under 60 chars, DIFFERENT from H1, contains keyword",
  "meta_description": "Under 155 chars, contains keyword, ends with value proposition",
  "slug": "{slug}",
  "serp_analysis": {{
    "dominant_format": "what format is ranking (how-to guide, listicle, comparison, etc.)",
    "competitor_word_counts": "summary of competitor word counts from SERP",
    "content_gaps": ["gap 1 no competitor covers", "gap 2", "gap 3"],
    "featured_snippet_available": true,
    "serp_features": ["PAA", "Featured Snippet", "AI Overview"]
  }},
  "target_audience": "1-2 sentence description of who this article is for and their search stage",
  "outline": [
    {{
      "heading": "Question-format or descriptive H2",
      "level": 2,
      "word_count": 150,
      "instructions": "Detailed 2-3 sentence writing instruction. What to open with (40-60 word answer), what data to include, what content gap to fill. Be specific about numbers, comparisons, and structure.",
      "subsections": [
        {{"heading": "H3 heading", "level": 3, "word_count": 80, "instructions": "Specific instruction for this subsection"}}
      ]
    }}
  ],
  "target_keywords": {{
    "primary": "{keyword}",
    "secondary": ["3-5 secondary keywords from PAA and related searches"],
    "lsi": ["3-5 LSI/semantic terms"]
  }},
  "entities": ["specific entities to mention 3-8x: brand name, cities, property types, financial terms"],
  "content_gaps": [
    {{"gap": "description of what no competitor covers", "where_to_address": "which H2 section covers this"}}
  ],
  "proof_points": [
    "Specific numerical claim to include with date stamp, e.g. 'Average 1BR rent in Austin: $1,450/mo (as of {quarter})'",
    "Another specific data point"
  ],
  "faqs": [
    {{"question": "Exact question from PAA or research", "answer": "40-60 word direct answer starting with yes/no or specific number. No hedging."}}
  ],
  "ctas": [
    {{"position": "after_first_h2", "text": "contextual CTA text", "url": "https://app.brightplace.ai"}},
    {{"position": "mid_article", "text": "contextual CTA text", "url": "https://app.brightplace.ai"}},
    {{"position": "end", "text": "contextual CTA text", "url": "https://app.brightplace.ai"}}
  ],
  "internal_links": [
    {{"text": "natural anchor text", "url": "/resources/slug", "context": "place in which section"}}
  ],
  "word_count_target": 1300,
  "snippet_paragraph": "49-55 word featured snippet paragraph that directly answers the primary keyword query with at least one specific data point. This goes right after the H1.",
  "writer_rules": {{
    "tone": "knowledgeable friend, utilitarian first, specific always",
    "sentence_length": "average 18 words, mix 8-12 and 18-25",
    "paragraph_length": "2-4 sentences max",
    "no_filler": "first sentence must contain keyword and begin answering. No scene-setting.",
    "section_openings": "every H2 opens with answer in first sentence (40-60 words). No lead-up.",
    "date_stamps": "every dollar figure gets (as of {quarter})"
  }}
}}

Set word_count_target based on your SERP analysis. If competitors average 1,200 words, set 1,200-1,400. NEVER inflate beyond what the SERP shows.

Return ONLY valid JSON, no markdown."""
        }],
    )

    text = message.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        fixed = text
        open_braces = fixed.count("{") - fixed.count("}")
        open_brackets = fixed.count("[") - fixed.count("]")
        if fixed.rstrip().endswith(","):
            fixed = fixed.rstrip().rstrip(",")
        fixed += "]" * max(0, open_brackets)
        fixed += "}" * max(0, open_braces)
        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse brief JSON. Length: {len(text)}")
            raise
