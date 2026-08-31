from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse

from app.dependencies import get_current_user
from app.schemas.pipeline import (
    ResearchReportResponse,
    BriefResponse,
    BriefUpdate,
    ArticleResponse,
    PipelineStatusResponse,
    PipelineJobResponse,
)
from pydantic import BaseModel

from app.services import research_service, brief_service, writing_service, qa_service
from app.services import sitemap_service
from app.services.project_service import get_project


class SitemapRequest(BaseModel):
    sitemap_url: str


class GuidelinesUpdate(BaseModel):
    writing_guidelines: dict | None = None
    qa_guidelines: dict | None = None

router = APIRouter(prefix="/api/projects/{project_id}", tags=["pipeline"])


# ============================================================
# Pipeline Status
# ============================================================

@router.get("/keywords/{keyword_id}/pipeline")
async def get_pipeline_status(
    project_id: str,
    keyword_id: str,
    user: dict = Depends(get_current_user),
):
    """Get full pipeline status for a keyword."""
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    from supabase import create_client
    from app.config import get_settings
    settings = get_settings()
    sb = create_client(settings.supabase_url, settings.supabase_service_key)

    # Get selected keyword
    kw = (
        sb.table("selected_keywords")
        .select("*")
        .eq("id", keyword_id)
        .eq("project_id", project_id)
        .execute()
    )
    if not kw.data:
        raise HTTPException(status_code=404, detail="Keyword not found")

    keyword_data = kw.data[0]

    # Get pipeline jobs
    jobs = (
        sb.table("pipeline_jobs")
        .select("*")
        .eq("keyword_id", keyword_id)
        .eq("project_id", project_id)
        .execute()
    )
    steps = {}
    for job in jobs.data:
        steps[job["step"]] = job

    # Get research report
    research = (
        sb.table("research_reports")
        .select("*")
        .eq("keyword_id", keyword_id)
        .eq("project_id", project_id)
        .execute()
    )

    # Get brief (via research report)
    brief = None
    article = None
    if research.data:
        brief_result = (
            sb.table("briefs")
            .select("*")
            .eq("research_report_id", research.data[0]["id"])
            .eq("project_id", project_id)
            .execute()
        )
        if brief_result.data:
            brief = brief_result.data[0]
            # Get article
            article_result = (
                sb.table("articles")
                .select("*")
                .eq("brief_id", brief["id"])
                .eq("project_id", project_id)
                .execute()
            )
            if article_result.data:
                article = article_result.data[0]

    return {
        "keyword_id": keyword_id,
        "keyword": keyword_data["keyword"],
        "steps": steps,
        "research_report": research.data[0] if research.data else None,
        "brief": brief,
        "article": article,
    }


# ============================================================
# Research
# ============================================================

@router.post("/keywords/{keyword_id}/research", response_model=ResearchReportResponse)
async def start_research(
    project_id: str,
    keyword_id: str,
    user: dict = Depends(get_current_user),
):
    """Start research for a keyword."""
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get keyword text
    from supabase import create_client
    from app.config import get_settings
    settings = get_settings()
    sb = create_client(settings.supabase_url, settings.supabase_service_key)

    kw = (
        sb.table("selected_keywords")
        .select("keyword")
        .eq("id", keyword_id)
        .eq("project_id", project_id)
        .single()
        .execute()
    )
    if not kw.data:
        raise HTTPException(status_code=404, detail="Keyword not found")

    result = await research_service.run_research(
        project_id=project_id,
        keyword_id=keyword_id,
        keyword=kw.data["keyword"],
        user_id=user["id"],
    )
    return result


@router.get("/keywords/{keyword_id}/research", response_model=ResearchReportResponse | None)
async def get_research(
    project_id: str,
    keyword_id: str,
    user: dict = Depends(get_current_user),
):
    """Get research report for a keyword."""
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await research_service.get_research_report(project_id, keyword_id, user["id"])
    if not result:
        raise HTTPException(status_code=404, detail="No research report found")
    return result


# ============================================================
# Brief
# ============================================================

@router.post("/keywords/{keyword_id}/brief", response_model=BriefResponse)
async def generate_brief(
    project_id: str,
    keyword_id: str,
    user: dict = Depends(get_current_user),
):
    """Generate a content brief from research data."""
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await brief_service.generate_brief(project_id, keyword_id, user["id"])
    return result


@router.get("/briefs/{brief_id}", response_model=BriefResponse)
async def get_brief(
    project_id: str,
    brief_id: str,
    user: dict = Depends(get_current_user),
):
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await brief_service.get_brief(project_id, brief_id, user["id"])
    if not result:
        raise HTTPException(status_code=404, detail="Brief not found")
    return result


@router.put("/briefs/{brief_id}", response_model=BriefResponse)
async def update_brief(
    project_id: str,
    brief_id: str,
    body: BriefUpdate,
    user: dict = Depends(get_current_user),
):
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await brief_service.update_brief(
        project_id, brief_id, user["id"], body.model_dump(exclude_none=True)
    )
    if not result:
        raise HTTPException(status_code=404, detail="Brief not found")
    return result


@router.post("/briefs/{brief_id}/approve", response_model=BriefResponse)
async def approve_brief(
    project_id: str,
    brief_id: str,
    user: dict = Depends(get_current_user),
):
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await brief_service.approve_brief(project_id, brief_id, user["id"])
    if not result:
        raise HTTPException(status_code=404, detail="Brief not found")
    return result


# ============================================================
# Write
# ============================================================

@router.post("/briefs/{brief_id}/write", response_model=ArticleResponse)
async def write_article(
    project_id: str,
    brief_id: str,
    user: dict = Depends(get_current_user),
):
    """Write an article from an approved brief."""
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await writing_service.write_article(project_id, brief_id, user["id"])
    return result


@router.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(
    project_id: str,
    article_id: str,
    user: dict = Depends(get_current_user),
):
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await writing_service.get_article(project_id, article_id, user["id"])
    if not result:
        raise HTTPException(status_code=404, detail="Article not found")
    return result


# ============================================================
# QA
# ============================================================

@router.post("/articles/{article_id}/qa", response_model=ArticleResponse)
async def run_qa(
    project_id: str,
    article_id: str,
    user: dict = Depends(get_current_user),
):
    """Run QA checks on an article."""
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await qa_service.run_qa(project_id, article_id, user["id"])
    return result


# ============================================================
# Rewrite (auto-fix QA failures)
# ============================================================

@router.post("/articles/{article_id}/rewrite", response_model=ArticleResponse)
async def rewrite_article(
    project_id: str,
    article_id: str,
    user: dict = Depends(get_current_user),
):
    """Rewrite article to fix QA failures, then re-run QA."""
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await writing_service.rewrite_from_qa(project_id, article_id, user["id"])
    return result


# ============================================================
# Export
# ============================================================

@router.get("/articles/{article_id}/export")
async def export_article(
    project_id: str,
    article_id: str,
    format: str = Query("md", regex="^(md|html)$"),
    user: dict = Depends(get_current_user),
):
    """Export article as MD or HTML."""
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await writing_service.export_article(project_id, article_id, user["id"], format)
    if not result:
        raise HTTPException(status_code=404, detail="Article not found")

    return PlainTextResponse(
        content=result["content"],
        media_type=result["content_type"],
        headers={
            "Content-Disposition": f'attachment; filename="{result["filename"]}"'
        },
    )


# ============================================================
# Sitemap
# ============================================================

@router.post("/sitemap")
async def save_sitemap(
    project_id: str,
    body: SitemapRequest,
    user: dict = Depends(get_current_user),
):
    """Save sitemap URL and fetch/cache all URLs."""
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await sitemap_service.save_sitemap_url(project_id, user["id"], body.sitemap_url)
    return result


@router.get("/sitemap")
async def get_sitemap(
    project_id: str,
    user: dict = Depends(get_current_user),
):
    """Get cached sitemap URLs."""
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    urls = await sitemap_service.get_sitemap_urls(project_id)
    return {"urls": urls, "count": len(urls)}


# ============================================================
# Guidelines
# ============================================================

DEFAULT_WRITING_GUIDELINES = {
    "brand_name_lowercase": True,
    "no_em_dashes": True,
    "banned_word": "signal",
    "banned_phrases": [
        "deep dive", "dive into", "navigate", "landscape", "unlock", "leverage",
        "whether you're", "it's worth noting", "interestingly", "notably",
        "hidden gem", "vibrant", "bustling", "thriving", "without further ado",
        "in today's", "let's take a look at", "in this article",
    ],
    "banned_sources": [
        "apartments.com", "zillow.com", "trulia.com", "rent.com", "zumper.com",
        "yelp.com", "reddit.com", "walkscore.com", "niche.com",
    ],
    "cta_domains": {
        "brand": "brightplace.ai",
        "action": "app.brightplace.ai",
    },
    "url_path": "/resources/",
    "fair_housing": True,
    "max_word_count": 2500,
    "faq_count": "6-8",
    "cta_count": 3,
    "internal_links": "5-10",
    "external_links": "3-5 (.gov/.edu)",
    "snippet_length": "49-55 words",
    "section_length": "120-180 words per H2",
}

DEFAULT_QA_GUIDELINES = {
    "checks": [
        {"name": "Brand Compliance", "enabled": True, "description": "Lowercase brand name, no em dashes, no banned phrases"},
        {"name": "SEO Structure", "enabled": True, "description": "H1 != SEO title, word count, entity density, internal links"},
        {"name": "Content Quality", "enabled": True, "description": "FAQ count, snippet paragraph, date stamps, CTAs"},
        {"name": "Math Verification", "enabled": True, "description": "Verify calculations and statistics"},
        {"name": "Link Audit", "enabled": True, "description": "Internal links exist, external links are .gov/.edu, no banned sources"},
        {"name": "Infrastructure", "enabled": True, "description": "No http://, correct URL paths, frontmatter valid"},
    ],
    "broken_urls": [
        "/resources/studio-apartments",
        "/resources/pet-friendly-houses-for-rent",
        "/resources/1-bedroom-apartments-near-me",
        "/guides/studio-apartments",
    ],
}


@router.get("/guidelines")
async def get_guidelines(
    project_id: str,
    user: dict = Depends(get_current_user),
):
    """Get project writing and QA guidelines."""
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    brand_context = project.get("brand_context", {}) or {}
    return {
        "writing": brand_context.get("writing_guidelines", DEFAULT_WRITING_GUIDELINES),
        "qa": brand_context.get("qa_guidelines", DEFAULT_QA_GUIDELINES),
    }


@router.put("/guidelines")
async def update_guidelines(
    project_id: str,
    body: GuidelinesUpdate,
    user: dict = Depends(get_current_user),
):
    """Update project writing and QA guidelines."""
    project = await get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    from supabase import create_client as sc
    from app.config import get_settings as gs
    settings = gs()
    sb = sc(settings.supabase_url, settings.supabase_service_key)

    brand_context = project.get("brand_context", {}) or {}
    if body.writing_guidelines is not None:
        brand_context["writing_guidelines"] = body.writing_guidelines
    if body.qa_guidelines is not None:
        brand_context["qa_guidelines"] = body.qa_guidelines

    sb.table("projects").update({"brand_context": brand_context}).eq("id", project_id).execute()
    return {
        "writing": brand_context.get("writing_guidelines", DEFAULT_WRITING_GUIDELINES),
        "qa": brand_context.get("qa_guidelines", DEFAULT_QA_GUIDELINES),
    }
