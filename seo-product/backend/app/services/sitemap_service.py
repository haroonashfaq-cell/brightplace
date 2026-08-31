import logging
import xml.etree.ElementTree as ET

import httpx
from supabase import create_client

from app.config import get_settings

logger = logging.getLogger(__name__)


def _get_supabase():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_key)


async def fetch_sitemap(project_id: str, user_id: str) -> list[str]:
    """Fetch and parse sitemap URLs for a project."""
    sb = _get_supabase()
    project = sb.table("projects").select("domain, brand_context").eq("id", project_id).single().execute()
    if not project.data:
        return []

    brand_context = project.data.get("brand_context", {})
    sitemap_url = brand_context.get("sitemap_url", "")

    if not sitemap_url:
        # Try common sitemap locations
        domain = project.data["domain"].rstrip("/")
        if not domain.startswith("http"):
            domain = f"https://{domain}"
        sitemap_url = f"{domain}/sitemap.xml"

    return await _parse_sitemap(sitemap_url)


async def save_sitemap_url(project_id: str, user_id: str, sitemap_url: str) -> dict:
    """Save sitemap URL to project brand_context."""
    sb = _get_supabase()
    project = sb.table("projects").select("brand_context").eq("id", project_id).single().execute()
    if not project.data:
        return {}

    brand_context = project.data.get("brand_context", {}) or {}
    brand_context["sitemap_url"] = sitemap_url

    # Fetch and cache sitemap URLs
    urls = await _parse_sitemap(sitemap_url)
    brand_context["sitemap_urls"] = urls

    sb.table("projects").update({
        "brand_context": brand_context,
    }).eq("id", project_id).execute()

    return {"sitemap_url": sitemap_url, "url_count": len(urls)}


async def get_sitemap_urls(project_id: str) -> list[str]:
    """Get cached sitemap URLs from brand_context."""
    sb = _get_supabase()
    project = sb.table("projects").select("brand_context").eq("id", project_id).single().execute()
    if not project.data:
        return []

    brand_context = project.data.get("brand_context", {}) or {}
    cached = brand_context.get("sitemap_urls", [])

    if cached:
        return cached

    # Try fetching if not cached
    sitemap_url = brand_context.get("sitemap_url", "")
    if sitemap_url:
        urls = await _parse_sitemap(sitemap_url)
        brand_context["sitemap_urls"] = urls
        sb.table("projects").update({"brand_context": brand_context}).eq("id", project_id).execute()
        return urls

    return []


def format_sitemap_for_prompt(urls: list[str]) -> str:
    """Format sitemap URLs for the writing agent prompt."""
    if not urls:
        return "No sitemap available. Use [INTERNAL LINK: topic description] placeholders for internal links."

    # Filter to /resources/ pages only for linking
    resource_urls = [u for u in urls if "/resources/" in u]
    other_urls = [u for u in urls if "/resources/" not in u and u not in resource_urls]

    lines = ["Available internal link targets (use these exact URLs):"]
    for url in resource_urls:
        # Extract slug for readability
        slug = url.split("/resources/")[-1].rstrip("/") if "/resources/" in url else url
        lines.append(f"  - {url} ({slug})")

    if other_urls:
        lines.append("\nOther site pages:")
        for url in other_urls[:20]:
            lines.append(f"  - {url}")

    return "\n".join(lines)


async def _parse_sitemap(sitemap_url: str) -> list[str]:
    """Parse sitemap XML and return all URLs."""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                sitemap_url,
                headers={"User-Agent": "SEOProductBot/1.0"},
                follow_redirects=True,
            )
            if resp.status_code != 200:
                logger.warning(f"Sitemap fetch failed ({resp.status_code}): {sitemap_url}")
                return []

            content = resp.text

        # Parse XML
        root = ET.fromstring(content)

        # Handle namespace
        ns = ""
        if root.tag.startswith("{"):
            ns = root.tag.split("}")[0] + "}"

        urls = []

        # Check if this is a sitemap index
        sitemap_tags = root.findall(f"{ns}sitemap")
        if sitemap_tags:
            # Sitemap index - fetch child sitemaps
            for sitemap_tag in sitemap_tags:
                loc = sitemap_tag.find(f"{ns}loc")
                if loc is not None and loc.text:
                    child_urls = await _parse_sitemap(loc.text.strip())
                    urls.extend(child_urls)
            return urls

        # Regular sitemap - extract URLs
        for url_tag in root.findall(f"{ns}url"):
            loc = url_tag.find(f"{ns}loc")
            if loc is not None and loc.text:
                urls.append(loc.text.strip())

        logger.info(f"Parsed {len(urls)} URLs from {sitemap_url}")
        return urls

    except Exception as e:
        logger.error(f"Sitemap parsing failed for {sitemap_url}: {e}")
        return []
