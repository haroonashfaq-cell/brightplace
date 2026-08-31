import json
import logging
import re
from datetime import datetime

import markdown
from anthropic import Anthropic
from supabase import create_client

from app.config import get_settings
from app.services.research_service import _update_job
from app.services.sitemap_service import get_sitemap_urls, format_sitemap_for_prompt

logger = logging.getLogger(__name__)


def _get_supabase():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_key)


def _get_anthropic():
    settings = get_settings()
    return Anthropic(api_key=settings.anthropic_api_key)


async def write_article(
    project_id: str,
    brief_id: str,
    user_id: str,
) -> dict:
    """Write a full article from an approved brief."""
    sb = _get_supabase()

    # Get brief
    brief = sb.table("briefs").select("*").eq("id", brief_id).eq("project_id", project_id).single().execute()
    if not brief.data:
        raise ValueError("Brief not found")

    brief_data = brief.data
    keyword = brief_data["keyword"]

    if brief_data["status"] not in ("approved", "writing", "completed"):
        raise ValueError("Brief must be approved before writing")

    # Get research report for reddit insights
    research = (
        sb.table("research_reports")
        .select("reddit_data")
        .eq("id", brief_data["research_report_id"])
        .single()
        .execute()
    )
    reddit_data = research.data.get("reddit_data", {}) if research.data else {}

    # Get project context
    project = sb.table("projects").select("*").eq("id", project_id).single().execute()
    project_data = project.data

    # Get sitemap URLs
    sitemap_urls = await get_sitemap_urls(project_id)
    sitemap_text = format_sitemap_for_prompt(sitemap_urls)

    # Get keyword_id from research report
    report = (
        sb.table("research_reports")
        .select("keyword_id")
        .eq("id", brief_data["research_report_id"])
        .single()
        .execute()
    )
    keyword_id = report.data["keyword_id"] if report.data else None

    # Update brief status
    sb.table("briefs").update({
        "status": "writing",
        "updated_at": datetime.utcnow().isoformat(),
    }).eq("id", brief_id).execute()

    if keyword_id:
        _update_job(sb, project_id, keyword_id, "write", "running")

    try:
        content_md = await _write_with_claude(
            brief_data=brief_data,
            reddit_data=reddit_data,
            niche=project_data.get("niche", ""),
            domain=project_data.get("domain", ""),
            brand_context=project_data.get("brand_context", {}),
            sitemap_text=sitemap_text,
        )

        # Convert to HTML
        content_html = markdown.markdown(
            content_md,
            extensions=["extra", "toc", "meta"],
        )

        # Count words (body only, exclude schema blocks)
        body_text = content_md.split("## FAQ Schema")[0] if "## FAQ Schema" in content_md else content_md
        word_count = len(re.findall(r'\b\w+\b', body_text))

        # Check for existing article
        existing = (
            sb.table("articles")
            .select("id")
            .eq("brief_id", brief_id)
            .eq("project_id", project_id)
            .execute()
        )

        article_record = {
            "brief_id": brief_id,
            "project_id": project_id,
            "keyword": keyword,
            "title": brief_data.get("title", ""),
            "content_md": content_md,
            "content_html": content_html,
            "word_count": word_count,
            "status": "draft",
        }

        if existing.data:
            article_id = existing.data[0]["id"]
            article_record["updated_at"] = datetime.utcnow().isoformat()
            sb.table("articles").update(article_record).eq("id", article_id).execute()
        else:
            result = sb.table("articles").insert(article_record).execute()
            article_id = result.data[0]["id"]

        # Update brief status
        sb.table("briefs").update({
            "status": "completed",
            "updated_at": datetime.utcnow().isoformat(),
        }).eq("id", brief_id).execute()

        if keyword_id:
            _update_job(sb, project_id, keyword_id, "write", "done", {"article_id": article_id})
            sb.table("selected_keywords").update({"status": "written"}).eq("id", keyword_id).execute()

        return sb.table("articles").select("*").eq("id", article_id).single().execute().data

    except Exception as e:
        logger.error(f"Writing failed for brief {brief_id}: {e}")
        sb.table("briefs").update({
            "status": "approved",
            "updated_at": datetime.utcnow().isoformat(),
        }).eq("id", brief_id).execute()
        if keyword_id:
            _update_job(sb, project_id, keyword_id, "write", "failed", error=str(e))
        raise


async def get_article(project_id: str, article_id: str, user_id: str) -> dict | None:
    sb = _get_supabase()
    result = (
        sb.table("articles")
        .select("*")
        .eq("id", article_id)
        .eq("project_id", project_id)
        .execute()
    )
    return result.data[0] if result.data else None


async def get_article_by_brief(project_id: str, brief_id: str, user_id: str) -> dict | None:
    sb = _get_supabase()
    result = (
        sb.table("articles")
        .select("*")
        .eq("brief_id", brief_id)
        .eq("project_id", project_id)
        .execute()
    )
    return result.data[0] if result.data else None


async def export_article(project_id: str, article_id: str, user_id: str, fmt: str = "md") -> dict | None:
    """Export article in specified format."""
    article = await get_article(project_id, article_id, user_id)
    if not article:
        return None

    if fmt == "html":
        return {
            "content": article.get("content_html", ""),
            "filename": f"{article.get('keyword', 'article').replace(' ', '-')}.html",
            "content_type": "text/html",
        }
    else:
        return {
            "content": article.get("content_md", ""),
            "filename": f"{article.get('keyword', 'article').replace(' ', '-')}.md",
            "content_type": "text/markdown",
        }


async def rewrite_from_qa(
    project_id: str,
    article_id: str,
    user_id: str,
) -> dict:
    """Rewrite article based on QA failures. Runs QA after rewrite automatically."""
    sb = _get_supabase()

    article = sb.table("articles").select("*").eq("id", article_id).eq("project_id", project_id).single().execute()
    if not article.data:
        raise ValueError("Article not found")

    article_data = article.data
    qa_report = article_data.get("qa_report", {})
    content_md = article_data.get("content_md", "")

    if not qa_report or not qa_report.get("checks"):
        raise ValueError("No QA report found. Run QA first.")

    # Collect all failures
    failed_checks = [c for c in qa_report["checks"] if not c["passed"]]
    if not failed_checks:
        return article_data  # All passed, nothing to rewrite

    # Build fix instructions from failures
    fix_instructions = []
    for check in failed_checks:
        fix_instructions.append(f"\n### {check['name']} — FAILED")
        for issue in check["issues"]:
            fix_instructions.append(f"  - ISSUE: {issue}")
        for sug in check["suggestions"]:
            fix_instructions.append(f"  - FIX: {sug}")

    fix_text = "\n".join(fix_instructions)

    # Get brief for context
    brief = sb.table("briefs").select("*").eq("id", article_data["brief_id"]).single().execute()
    brief_data = brief.data if brief.data else {}

    # Get keyword_id for job tracking
    keyword_id = None
    if brief_data:
        report = sb.table("research_reports").select("keyword_id").eq("id", brief_data.get("research_report_id", "")).execute()
        if report.data:
            keyword_id = report.data[0]["keyword_id"]

    # Fetch sitemap if internal links are failing
    sitemap_section = ""
    has_link_issue = any("internal links" in str(c.get("issues", [])).lower() for c in failed_checks)
    if has_link_issue:
        from app.services.sitemap_service import get_sitemap_urls, format_sitemap_for_prompt
        sitemap_urls = await get_sitemap_urls(project_id)
        if sitemap_urls:
            sitemap_section = f"""

=== SITEMAP (use these for internal links) ===
{format_sitemap_for_prompt(sitemap_urls)}

When fixing internal links: insert real markdown links using URLs from the sitemap above.
Format: [anchor text](URL). Use natural anchor text. Add 7-10 internal links throughout the article body.
Only link to URLs that exist in the sitemap. Use /resources/ path always."""

    logger.info(f"Rewriting article {article_id} to fix {len(failed_checks)} QA failures")

    try:
        client = _get_anthropic()
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=16000,
            messages=[{
                "role": "user",
                "content": f"""You are a senior content editor. Below is an article that FAILED QA checks. Your job is to fix EVERY issue listed below and return the corrected article.

=== QA FAILURES TO FIX ===
{fix_text}

=== ARTICLE CONTEXT ===
Keyword: {article_data.get('keyword', '')}
Title: {article_data.get('title', '')}
Word count target: {brief_data.get('word_count_target', 1500)}

{sitemap_section}

=== CURRENT ARTICLE ===
{content_md}

=== FIX INSTRUCTIONS ===

Fix EVERY issue listed above. Specific rules:

1. **Brand name lowercase**: Replace every instance of uppercase brand name with lowercase. Even at sentence start.
2. **Em dashes**: Replace ALL em dashes (— and --) with commas, periods, semicolons, or parentheses. Search the entire document.
3. **Banned phrases**: Remove or rephrase every banned phrase. Replace "signal" with "indicator/suggests/reflects".
4. **Internal links**: If the issue is missing internal links AND a sitemap is provided above, insert real markdown links using URLs from the sitemap. Add 7-10 internal links. Use natural anchor text mid-sentence. If no sitemap is provided, use [INTERNAL LINK: topic] placeholders.
5. **FAQs**: If FAQ count is too low, add more FAQ pairs. Each answer must be 40-60 words, start with a direct answer.
6. **Date stamps**: Add "(as of Q3 2026)" after EVERY dollar figure, rent range, and statistic that doesn't already have one.
7. **Frontmatter**: If missing, ensure the article starts with --- frontmatter block (not wrapped in ```markdown).
8. **Legacy paths**: Replace /knowledgebase/ with /resources/ and /guides/ with /resources/ everywhere.
9. **Word count**: Stay within 10% of the target. Do NOT add padding.
10. **SEO title vs H1**: Make sure seo_title in frontmatter differs from the H1 title.

IMPORTANT:
- Do NOT wrap output in ```markdown``` code fences. Start directly with ---
- Keep the same structure and content, only fix the issues
- Do NOT add new sections or significantly change the content
- Return ONLY the fixed markdown. No commentary."""
            }],
        )

        fixed_md = message.content[0].text.strip()
        # Strip markdown code fence if Claude added one
        if fixed_md.startswith("```"):
            fixed_md = fixed_md.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        # Convert to HTML
        fixed_html = markdown.markdown(fixed_md, extensions=["extra", "toc", "meta"])

        # Count words (body only)
        body_text = fixed_md.split("## FAQ Schema")[0] if "## FAQ Schema" in fixed_md else fixed_md
        word_count = len(re.findall(r'\b\w+\b', body_text))

        # Update article
        sb.table("articles").update({
            "content_md": fixed_md,
            "content_html": fixed_html,
            "word_count": word_count,
            "status": "draft",
            "updated_at": datetime.utcnow().isoformat(),
        }).eq("id", article_id).execute()

        # Auto-run QA on the fixed article
        from app.services.qa_service import run_qa
        result = await run_qa(project_id, article_id, user_id)

        logger.info(f"Rewrite complete. New QA score: {result.get('seo_score', 0)}%")
        return result

    except Exception as e:
        logger.error(f"Rewrite failed for article {article_id}: {e}")
        raise


# ============================================================
# Claude Writing — Full SEO Writing Agent Prompt
# ============================================================

async def _write_with_claude(
    brief_data: dict,
    reddit_data: dict,
    niche: str,
    domain: str,
    brand_context: dict,
    sitemap_text: str,
) -> str:
    """Use Claude to write the full article using the seo-writing-agent prompt."""
    # Build the content brief section
    brief_text = _build_brief_text(brief_data)

    # Build reddit insights
    reddit_text = _build_reddit_text(reddit_data)

    today = datetime.utcnow().strftime("%Y-%m-%d")
    quarter = f"Q{(datetime.utcnow().month - 1) // 3 + 1} {datetime.utcnow().year}"

    client = _get_anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=16000,
        messages=[{
            "role": "user",
            "content": f"""You are a senior content writer. You are writing a piece for {domain}/resources/, a content layer built to rank on Google and get cited by AI search engines (ChatGPT, Perplexity, Claude, Google AI Overviews).

Brand: {brand_context.get('brand_name', domain.replace('https://', '').replace('http://', '').split('.')[0])}
Niche: {niche or 'general'}
Domain: {domain}

Your output is a complete, publish-ready article in markdown format. A human editor will review it, but your draft should require minimal revision. Treat the content brief below as a contract. Execute every section in the outline. Do not skip, summarize, or combine sections unless the brief explicitly instructs you to.

===== CONTENT BRIEF =====
{brief_text}

===== SITEMAP =====
{sitemap_text}

===== REDDIT INSIGHTS (weave naturally, NEVER cite Reddit, NEVER quote users, NEVER link threads) =====
{reddit_text}

===== WRITING INSTRUCTIONS =====

Follow every instruction below. These are non-negotiable production rules.

---

### VOICE & TONE

Write like a knowledgeable friend who has done the research and is being direct about what they found. You are not a salesperson, a tourism board, or an academic.

- Lead with information, not personality. The reader came from a search engine with a specific question. Answer it.
- Be utilitarian first, warm second. Short declarative sentences. Get to the point.
- Use specifics constantly. Dollar amounts, distances, time durations, counts, names of actual places. Vague claims are never acceptable.
- Include honest tradeoffs where relevant.
- Never be promotional about brightplace.

---

### AEO: AI ENGINE OPTIMIZATION

**BLUF (Bottom Line Up Front):**
- First 2-3 sentences must directly answer the primary keyword query with specific data.
- Every H2 section must open with a BLUF: key answer in first sentence (40-60 words), then supporting detail.

**Self-Contained Sections:**
- Each H2 must function as standalone unit. Follow: definition/answer, detail, specific example or data point.
- Target 120-180 words per section.

**Comparison Data:**
- Use bold-label bullet point format (NO markdown tables, Webflow cannot render them):
  **[Option A]:** $X-$Y/mo (as of {quarter}). [Key detail]. [Tradeoff].

**Entity Repetition:**
- Brand name 3-5 times in body (excluding CTAs).
- Primary keyword 7-12 times across article.

**Freshness Markers:**
- "(as of {quarter})" on every dollar figure, statistic, time-sensitive claim.
- "Last reviewed: {datetime.utcnow().strftime('%B %Y')}" in footer.
- `date_modified: {today}` in frontmatter.

**Outbound Authority Links:**
- 3-5 links to .gov or .edu sources.
- NEVER link to: Apartments.com, Zillow, Trulia, Rent.com, Zumper, Apartment List, HotPads, RentCafe, Realtor.com, Reddit, Yelp, Walk Score, Niche, AreaVibes.

---

### HARD RULES (ZERO TOLERANCE)

**Naming:** brightplace ALWAYS lowercase. Even sentence start. Even headings.

**Punctuation:** NEVER use em dashes (-- or unicode character). Use commas, periods, semicolons, colons, or parentheses.

**Banned word:** NEVER "signal" in any form. Use "indicator," "suggests," "points to," "reflects."

**Banned phrases (never use):**
"deep dive," "dive into," "navigate" (metaphor), "landscape" (metaphor), "unlock," "leverage," "whether you're X or Y," "from X to Y" (range framing), "it's worth noting," "interestingly," "notably," "hidden gem," "vibrant," "bustling," "thriving," "In this article we will cover," "Let's take a look at," "Without further ado," "In today's [anything]"

**Title rules:** No "Top X," "Best," "Ultimate Guide," "#1," "Everything You Need to Know."

**Fair Housing:** Never describe neighborhoods by demographics. Never crime statistics or safety ratings. Describe by lifestyle infrastructure only: walkability, dining, nightlife, transit, parks, grocery.

---

### INTERNAL LINKING RULES (USING SITEMAP)

1. As you write, identify every mention of a topic that another brightplace article covers.
2. Search the sitemap above for a matching URL.
3. If match exists: insert `[anchor text](https://www.brightplace.ai/resources/matching-slug)`. ALWAYS use `/resources/` path, NEVER `/knowledgebase/`.
4. If no match: insert `[INTERNAL LINK: topic description]` placeholder.
5. NEVER link to: `/resources/studio-apartments`, `/resources/pet-friendly-houses-for-rent`, `/resources/1-bedroom-apartments-near-me`, `/guides/studio-apartments`.
6. All internal links use `https://www.brightplace.ai/` (with www).
7. Natural anchor text. Never "click here" or "read more."
8. Link only on first mention per section. 5-10 internal links total.
9. Place links mid-sentence naturally.

### CTA RULES

Place 3 CTAs per article:
1. After first H2 (once reader has context)
2. Mid-article (after comparison/neighborhood section)
3. End of article (after FAQ)

Two link targets:
- `brightplace.ai` for brand mentions
- `app.brightplace.ai` for action CTAs ("Start searching at app.brightplace.ai")
- NEVER both in same line
- NEVER: "Sign up," "Get started," "Don't wait," "Find your dream home"
- Language: informational only ("See what is available on brightplace," "brightplace tracks current availability")

---

### STRUCTURE

**Markdown output format:**
```
---
title: "[Article Title]"
seo_title: "[SEO title, different from H1, under 60 chars]"
meta_description: "[Under 155 chars, includes primary keyword]"
slug: "[url-slug]"
primary_keyword: "[exact primary keyword]"
schema_types: ["Article", "FAQPage", "WebPage"]
word_count_target: [number]
last_reviewed: "{datetime.utcnow().strftime('%B %Y')}"
date_published: {today}
date_modified: {today}
author: brightplace
---

# [Article Title - H1]

[Featured snippet paragraph: 49-55 words answering the primary keyword]

## [First H2 - question format matching PAA]
[40-60 word opening answer, then details]

[... more H2/H3 sections following brief outline ...]

## Frequently Asked Questions About [Topic]

### [Question 1]?
[40-60 word standalone answer]

[... 10+ FAQ pairs ...]

---

## FAQ Schema (JSON-LD)
[FAQPage JSON-LD]

## Article Schema (JSON-LD)
[Article JSON-LD]

## WebPage Schema (JSON-LD)
[WebPage JSON-LD with breadcrumb Home > Resources > Title, speakable targeting .article-intro and .faq-section]
```

**WORD COUNT (STRICT — NON-NEGOTIABLE):**
- The brief specifies an exact word_count_target. You MUST stay within 10% of that number.
- If target is 1,500 words, write 1,350-1,650 words. NOT 2,000. NOT 3,000.
- Each H2 section: 120-180 words as specified in the brief instructions.
- FAQ answers: 40-60 words each.
- Do NOT pad content. Do NOT add extra sections beyond the outline.
- Count your words. If you are over target, cut unnecessary detail.

**Heading hierarchy:** One H1 only. Major sections H2. Subsections H3. Never skip levels.
**Paragraphs:** 2-4 sentences max. Vary length.
**Sentences:** Target 18 words average. Mix short (8-12) and medium (18-25). Avoid 30+.
**Lists:** Bullets for parallel items only. No markdown tables.
**No markdown tables.** Convert ALL comparisons to bold-label bullet points.

---

### ANTI-AI-DETECTION

- No symmetric structures (vary section lengths)
- No hedge stacking
- No false balance (say which option is better when clear)
- No transition word addiction ("Furthermore," "Moreover," "Additionally")
- No conclusion restating intro
- Specificity over abstraction
- Vary H2 openings (max 2 same structure)

---

### SCHEMA OUTPUT

After the article body, output 3 schema blocks:

1. **FAQPage Schema** - Every Q&A from FAQ section, answers word-for-word
2. **Article Schema** - headline, description, author/publisher as brightplace Organization
3. **WebPage Schema** - Breadcrumb: Home > Resources > [Title] (NOT Knowledgebase). Include speakable targeting .article-intro and .faq-section. Canonical URL: https://brightplace.ai/resources/[slug]

---

### SELF-REVIEW CHECKLIST (fix before returning)

1. brightplace lowercase everywhere
2. Zero em dashes
3. "signal" does not appear
4. No banned phrases
5. No ILS/aggregator/forum citations
6. No Fair Housing violations
7. First sentence contains primary keyword + answers query
8. Every H2 opens with answer first
9. Every dollar figure date-stamped
10. 10+ FAQ pairs, 40-60 words each
11. One H1 only
12. H2/H3 matches brief outline
13. Word count within target
14. 5-10 internal links (real URLs from sitemap)
15. 3-5 external .gov/.edu links
16. 3 CTA placements
17. All 3 JSON-LD schemas present
18. All frontmatter populated
19. No markdown tables
20. SEO title differs from H1

Return ONLY the markdown file. No commentary. Start with frontmatter (---) and end with schema blocks."""
        }],
    )

    return message.content[0].text.strip()


def _build_brief_text(brief_data: dict) -> str:
    """Format the brief data for the writing prompt."""
    lines = []
    lines.append(f"Primary keyword: {brief_data.get('keyword', '')}")
    lines.append(f"Title (H1): {brief_data.get('title', '')}")
    lines.append(f"SEO Title: {brief_data.get('seo_title', '')}")
    lines.append(f"Meta Description: {brief_data.get('meta_description', '')}")
    lines.append(f"Slug: {brief_data.get('slug', '')}")
    lines.append(f"Word count target: {brief_data.get('word_count_target', 2000)}")

    target_kw = brief_data.get("target_keywords", {})
    if target_kw:
        lines.append(f"Secondary keywords: {json.dumps(target_kw.get('secondary', []))}")
        lines.append(f"LSI terms: {json.dumps(target_kw.get('lsi', []))}")

    lines.append(f"\nFeatured snippet paragraph:\n{brief_data.get('snippet_paragraph', '')}")

    lines.append(f"\nEntities to mention (repeat 3-8x): {json.dumps(brief_data.get('entities', []))}")

    lines.append("\nContent Outline:")
    for section in brief_data.get("outline", []):
        prefix = "#" * section.get("level", 2)
        lines.append(f"  {prefix} {section.get('heading', '')}")
        if section.get("instructions"):
            lines.append(f"     Instructions: {section['instructions']}")
        for sub in section.get("subsections", []):
            lines.append(f"    ### {sub.get('heading', '')}")
            if sub.get("instructions"):
                lines.append(f"       Instructions: {sub['instructions']}")

    lines.append("\nFAQ pairs (use these exact questions, write 40-60 word answers):")
    for faq in brief_data.get("faqs", []):
        lines.append(f"  Q: {faq.get('question', '')}")
        if faq.get("answer"):
            lines.append(f"  A (guidance): {faq['answer']}")

    lines.append("\nCTA placements:")
    for cta in brief_data.get("ctas", []):
        lines.append(f"  - {cta.get('position', '')}: {cta.get('text', '')} -> {cta.get('url', '')}")

    lines.append("\nInternal link suggestions:")
    for link in brief_data.get("internal_links", []):
        lines.append(f"  - [{link.get('text', '')}]({link.get('url', '')}) - {link.get('context', '')}")

    return "\n".join(lines)


def _build_reddit_text(reddit_data: dict) -> str:
    """Format reddit insights for the writing prompt."""
    if not reddit_data or reddit_data.get("thread_count", 0) == 0:
        return "No Reddit data available."

    lines = []
    if reddit_data.get("pain_points"):
        lines.append("Pain points renters mention:")
        for p in reddit_data["pain_points"]:
            lines.append(f"  - {p}")

    if reddit_data.get("real_numbers"):
        lines.append("Real numbers/costs renters share:")
        for n in reddit_data["real_numbers"]:
            lines.append(f"  - {n}")

    if reddit_data.get("misconceptions"):
        lines.append("Common misconceptions to address:")
        for m in reddit_data["misconceptions"]:
            lines.append(f"  - {m}")

    if reddit_data.get("advice"):
        lines.append("Practical advice from experienced renters:")
        for a in reddit_data["advice"]:
            lines.append(f"  - {a}")

    if reddit_data.get("common_questions"):
        lines.append("Common questions renters ask:")
        for q in reddit_data["common_questions"]:
            lines.append(f"  - {q}")

    return "\n".join(lines)
