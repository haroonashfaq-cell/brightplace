import logging

from supabase import create_client

from app.config import get_settings
from app.services.dataforseo import dataforseo_client

logger = logging.getLogger(__name__)


def _get_supabase():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_key)


async def create_project(user_id: str, domain: str, niche: str | None) -> dict:
    sb = _get_supabase()
    result = (
        sb.table("projects")
        .insert({"user_id": user_id, "domain": domain, "niche": niche})
        .execute()
    )
    return result.data[0]


async def get_projects(user_id: str) -> list[dict]:
    sb = _get_supabase()
    result = (
        sb.table("projects")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data


async def get_project(project_id: str, user_id: str) -> dict | None:
    sb = _get_supabase()
    result = (
        sb.table("projects")
        .select("*")
        .eq("id", project_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    return result.data


async def detect_competitors(project_id: str, user_id: str) -> list[dict]:
    """Auto-detect competitors via DataForSEO and store them."""
    project = await get_project(project_id, user_id)
    if not project:
        return []

    domain = project["domain"]
    # Normalize domain for comparison (strip protocol, www, trailing slash)
    clean_domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")
    raw = await dataforseo_client.detect_competitors(clean_domain)

    sb = _get_supabase()
    competitors = []
    for item in raw[:5]:
        comp_domain = item.get("domain", "")
        comp_clean = comp_domain.replace("www.", "").rstrip("/")
        if not comp_domain or comp_clean == clean_domain:
            continue

        metrics = item.get("full_domain_metrics", {})
        organic = metrics.get("organic", {})

        etv = organic.get("etv")
        count = organic.get("count")
        record = {
            "project_id": project_id,
            "domain": comp_domain,
            "dr_score": int(etv) if etv is not None else None,
            "indexed_pages": int(count) if count is not None else None,
            "auto_detected": True,
        }
        result = sb.table("competitors").insert(record).execute()
        competitors.append(result.data[0])

    return competitors


async def add_competitor(
    project_id: str, user_id: str, domain: str
) -> dict | None:
    project = await get_project(project_id, user_id)
    if not project:
        return None

    sb = _get_supabase()
    result = (
        sb.table("competitors")
        .insert(
            {
                "project_id": project_id,
                "domain": domain,
                "auto_detected": False,
            }
        )
        .execute()
    )
    return result.data[0]


async def get_competitors(project_id: str, user_id: str) -> list[dict]:
    project = await get_project(project_id, user_id)
    if not project:
        return []

    sb = _get_supabase()
    result = (
        sb.table("competitors")
        .select("*")
        .eq("project_id", project_id)
        .order("created_at")
        .execute()
    )
    return result.data


async def delete_project(project_id: str, user_id: str) -> bool:
    project = await get_project(project_id, user_id)
    if not project:
        return False

    sb = _get_supabase()
    # CASCADE will handle competitors, keyword_gaps, selected_keywords, long_tail_keywords
    sb.table("projects").delete().eq("id", project_id).execute()
    return True


async def delete_competitor(
    project_id: str, competitor_id: str, user_id: str
) -> bool:
    project = await get_project(project_id, user_id)
    if not project:
        return False

    sb = _get_supabase()
    sb.table("competitors").delete().eq("id", competitor_id).eq(
        "project_id", project_id
    ).execute()
    return True
