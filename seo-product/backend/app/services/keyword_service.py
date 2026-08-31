import logging

from supabase import create_client

from app.config import get_settings
from app.services.dataforseo import dataforseo_client, DataForSEOClient
from app.services.project_service import get_project, get_competitors

logger = logging.getLogger(__name__)


def _get_supabase():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_key)


async def get_categories(project_id: str, user_id: str) -> list[dict]:
    """Get distinct categories with counts for a project's keyword gaps."""
    project = await get_project(project_id, user_id)
    if not project:
        return []

    sb = _get_supabase()
    result = (
        sb.table("keyword_gaps")
        .select("category")
        .eq("project_id", project_id)
        .execute()
    )

    # Count categories manually since Supabase REST doesn't support GROUP BY
    counts: dict[str, int] = {}
    for row in result.data:
        cat = row.get("category") or "General"
        counts[cat] = counts.get(cat, 0) + 1

    return [
        {"category": cat, "count": count}
        for cat, count in sorted(counts.items(), key=lambda x: -x[1])
    ]


async def get_keyword_gaps(
    project_id: str,
    user_id: str,
    page: int = 1,
    page_size: int = 20,
    kd_min: int | None = None,
    kd_max: int | None = None,
    vol_min: int | None = None,
    vol_max: int | None = None,
    intent: str | None = None,
    search: str | None = None,
    category: str | None = None,
    sort_by: str = "volume",
    sort_dir: str = "desc",
) -> dict:
    """Get filtered, sorted, paginated keyword gaps from DB."""
    project = await get_project(project_id, user_id)
    if not project:
        return {"items": [], "total_count": 0, "page": page, "page_size": page_size}

    sb = _get_supabase()
    query = sb.table("keyword_gaps").select("*", count="exact").eq(
        "project_id", project_id
    )

    if kd_min is not None:
        query = query.gte("kd", kd_min)
    if kd_max is not None:
        query = query.lte("kd", kd_max)
    if vol_min is not None:
        query = query.gte("volume", vol_min)
    if vol_max is not None:
        query = query.lte("volume", vol_max)
    if intent:
        query = query.eq("intent", intent)
    if search:
        query = query.ilike("keyword", f"%{search}%")
    if category:
        query = query.eq("category", category)

    is_desc = sort_dir == "desc"
    query = query.order(sort_by, desc=is_desc)

    offset = (page - 1) * page_size
    query = query.range(offset, offset + page_size - 1)

    result = query.execute()

    return {
        "items": result.data,
        "total_count": result.count or 0,
        "page": page,
        "page_size": page_size,
    }


async def import_keywords(
    project_id: str, user_id: str, keywords: list, replace: bool = False
) -> dict:
    """Import keywords from user CSV upload."""
    project = await get_project(project_id, user_id)
    if not project:
        return {"imported": 0}

    sb = _get_supabase()

    if replace:
        sb.table("keyword_gaps").delete().eq("project_id", project_id).execute()

    records = []
    for kw in keywords:
        keyword = kw.keyword if hasattr(kw, "keyword") else kw.get("keyword", "")
        volume = kw.volume if hasattr(kw, "volume") else kw.get("volume", 0)
        kd = kw.kd if hasattr(kw, "kd") else kw.get("kd", 0)
        cpc = kw.cpc if hasattr(kw, "cpc") else kw.get("cpc", 0)
        intent = kw.intent if hasattr(kw, "intent") else kw.get("intent")
        category = kw.category if hasattr(kw, "category") else kw.get("category")
        city = kw.city if hasattr(kw, "city") else kw.get("city")

        if not keyword:
            continue

        enriched = DataForSEOClient.enrich_keyword(keyword, volume, kd, cpc)
        # User-provided category/city takes priority over auto-detected
        if category:
            enriched["category"] = category
        if city:
            enriched["city"] = city

        records.append({
            "project_id": project_id,
            "keyword": keyword,
            "volume": volume,
            "kd": kd,
            "intent": intent or enriched.get("intent"),
            "competitor_domains": [],
            "cpc": enriched["cpc"],
            "difficulty": enriched["difficulty"],
            "category": enriched["category"],
            "city": enriched["city"],
            "is_long_tail": enriched["is_long_tail"],
            "tier": enriched["tier"],
            "word_count": enriched["word_count"],
        })

    for i in range(0, len(records), 500):
        sb.table("keyword_gaps").insert(records[i:i+500]).execute()

    logger.info(f"Imported {len(records)} keywords for project {project_id}")
    return {"imported": len(records)}


async def refresh_keyword_gaps(project_id: str, user_id: str) -> dict:
    """Re-fetch keyword gaps from DataForSEO and update DB."""
    project = await get_project(project_id, user_id)
    if not project:
        return {"items": [], "total_count": 0}

    competitors = await get_competitors(project_id, user_id)
    if not competitors:
        return {"items": [], "total_count": 0}

    domain = project["domain"].replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")
    comp_domains = [c["domain"] for c in competitors if c["domain"].replace("www.", "").rstrip("/") != domain]

    niche = project.get("niche") or "general"
    seed_keywords = _get_niche_seeds(niche)

    # 1. Fetch keyword ideas from niche seed terms (like SEMrush)
    logger.info(f"Fetching keyword ideas for seeds: {seed_keywords[:5]}")
    raw_keywords = await dataforseo_client.get_keyword_ideas(
        seed_keywords=seed_keywords[:5],
        limit=300,
    )

    # 2. Also fetch competitor gaps for keywords they rank for but we don't
    if comp_domains:
        gap_result = await dataforseo_client.get_keyword_gaps(
            competitors=comp_domains,
            exclude_domain=domain,
            limit=100,
        )
        seen = {kw["keyword"] for kw in raw_keywords}
        for item in gap_result.get("items", []):
            if item["keyword"] not in seen:
                raw_keywords.append(item)
                seen.add(item["keyword"])

    if not raw_keywords:
        return {"items_count": 0, "total_count": 0}

    # 3. Clean & deduplicate keywords
    niche_lower = niche.lower()
    raw_keywords = _clean_keywords(raw_keywords, niche_lower)
    logger.info(f"After cleaning: {len(raw_keywords)} keywords")

    # 4. Get keyword difficulty for all keywords in bulk
    kw_list = [kw["keyword"] for kw in raw_keywords]
    logger.info(f"Fetching KD for {len(kw_list)} keywords")
    kd_map = await dataforseo_client.get_bulk_keyword_difficulty(kw_list)

    # 5. Merge KD scores and enrich
    sb = _get_supabase()
    sb.table("keyword_gaps").delete().eq("project_id", project_id).execute()

    records = []
    for item in raw_keywords:
        keyword = item["keyword"]
        volume = item.get("volume", 0) or 0
        kd = kd_map.get(keyword, item.get("kd", 0)) or 0
        cpc = item.get("cpc", 0) or 0

        enriched = DataForSEOClient.enrich_keyword(keyword, volume, kd, cpc)

        records.append({
            "project_id": project_id,
            "keyword": keyword,
            "volume": volume,
            "kd": kd,
            "intent": item.get("intent"),
            "competitor_domains": item.get("competitor_domains", comp_domains),
            "cpc": enriched["cpc"],
            "difficulty": enriched["difficulty"],
            "category": enriched["category"],
            "city": enriched["city"],
            "is_long_tail": enriched["is_long_tail"],
            "tier": enriched["tier"],
            "word_count": enriched["word_count"],
        })

    # Insert in batches (Supabase has row limits)
    for i in range(0, len(records), 500):
        sb.table("keyword_gaps").insert(records[i:i+500]).execute()

    logger.info(f"Stored {len(records)} keywords for project {project_id}")
    return {
        "items_count": len(records),
        "total_count": len(records),
    }


def _clean_keywords(keywords: list[dict], niche: str) -> list[dict]:
    """Deduplicate and filter irrelevant keywords."""
    # 1. Remove single-word keywords (too generic)
    keywords = [kw for kw in keywords if len(kw["keyword"].split()) >= 2]

    # 2. Remove zero-volume keywords
    keywords = [kw for kw in keywords if (kw.get("volume") or 0) >= 10]

    # 3. Deduplicate by normalized keyword (sort words to catch reorderings)
    seen: dict[str, dict] = {}
    for kw in keywords:
        # Normalize: sort words, lowercase
        words = sorted(kw["keyword"].lower().split())
        norm = " ".join(words)
        if norm not in seen or (kw.get("volume") or 0) > (seen[norm].get("volume") or 0):
            seen[norm] = kw
    keywords = list(seen.values())

    # 4. Filter out keywords irrelevant to the niche
    irrelevant_patterns = [
        "weather", "zip code", "time zone", "population",
        "area code", "news", "jobs", "salary", "indeed",
        "walmart", "target", "costco", "amazon",
        "restaurant", "food", "pizza", "coffee",
        "hospital", "doctor", "dentist", "pharmacy",
        "school district", "high school", "middle school",
        "gym", "movie", "theater", "park near",
        "water park", "auto parts", "car wash",
    ]
    # Only apply niche filter if niche is specific enough
    if any(w in niche for w in ["apartment", "rental", "rent", "plumb", "real estate"]):
        niche_relevance = _get_niche_relevance_words(niche)
        filtered = []
        for kw in keywords:
            kw_lower = kw["keyword"].lower()
            # Skip if matches irrelevant patterns
            if any(p in kw_lower for p in irrelevant_patterns):
                continue
            # Keep if matches niche relevance OR is a "how to" / educational query
            is_educational = any(p in kw_lower for p in ["how to", "what is", "what does", "what are", "guide", "tips", "vs ", "cost", "price", "average"])
            is_niche = any(w in kw_lower for w in niche_relevance)
            if is_niche or is_educational:
                filtered.append(kw)
        keywords = filtered

    return keywords


def _get_niche_relevance_words(niche: str) -> list[str]:
    """Words that indicate a keyword is relevant to the niche."""
    niche_lower = niche.lower()
    if any(w in niche_lower for w in ["apartment", "rental", "renter", "housing", "rent"]):
        return [
            "apartment", "rent", "lease", "tenant", "landlord", "renter",
            "bedroom", "studio", "condo", "townhouse", "duplex", "loft",
            "pet friendly", "furnished", "unfurnished", "move in",
            "eviction", "credit check", "income", "section 8", "hud",
            "sublease", "sublet", "roommate", "deposit", "prorated",
            "housing", "home for rent", "house for rent", "near me",
            "luxury", "affordable", "cheap", "low income", "senior",
        ]
    if any(w in niche_lower for w in ["plumb", "pipe", "drain"]):
        return [
            "plumb", "pipe", "drain", "faucet", "toilet", "sink",
            "water heater", "sewer", "leak", "clog", "repair",
            "install", "fix", "replace", "bathroom", "kitchen",
            "garbage disposal", "septic", "backflow", "valve",
            "tankless", "boiler", "copper", "pvc",
        ]
    if any(w in niche_lower for w in ["real estate", "property", "home"]):
        return [
            "home", "house", "property", "real estate", "mortgage",
            "buy", "sell", "listing", "agent", "broker", "mls",
            "inspection", "appraisal", "closing", "escrow", "title",
            "foreclosure", "investment", "flip", "condo", "townhouse",
        ]
    return niche_lower.split()


def _get_niche_seeds(niche: str) -> list[str]:
    """Return seed keywords for a niche to expand keyword research."""
    niche_lower = niche.lower()

    # Apartment / rental niches
    if any(w in niche_lower for w in ["apartment", "rental", "renter", "housing", "rent"]):
        return [
            "apartments for rent",
            "pet friendly apartments",
            "cheap apartments near me",
            "1 bedroom apartments",
            "luxury apartments",
            "student apartments",
            "furnished apartments",
            "income restricted apartments",
            "short term lease apartments",
            "how to find an apartment",
        ]

    # Plumbing niches
    if any(w in niche_lower for w in ["plumb", "pipe", "drain"]):
        return [
            "plumber near me",
            "emergency plumber",
            "drain cleaning",
            "water heater repair",
            "toilet repair",
            "leaking pipe fix",
            "sewer line repair",
            "garbage disposal installation",
            "bathroom plumbing",
            "commercial plumbing services",
        ]

    # Real estate niches
    if any(w in niche_lower for w in ["real estate", "property", "home", "house"]):
        return [
            "homes for sale",
            "first time home buyer",
            "how to buy a house",
            "real estate agent near me",
            "home inspection checklist",
            "mortgage rates today",
            "sell my house fast",
            "property management",
        ]

    # Generic fallback — use niche as seed
    return [
        niche,
        f"{niche} near me",
        f"best {niche}",
        f"how to find {niche}",
        f"cheap {niche}",
        f"{niche} cost",
        f"{niche} tips",
        f"{niche} guide",
    ]


async def get_long_tail(
    project_id: str, gap_id: str, user_id: str
) -> list[dict]:
    """Get long-tail keywords for a keyword gap. Fetches from DataForSEO if not cached."""
    project = await get_project(project_id, user_id)
    if not project:
        return []

    sb = _get_supabase()

    # Check if we already have long-tail keywords stored
    existing = (
        sb.table("long_tail_keywords")
        .select("*")
        .eq("keyword_gap_id", gap_id)
        .execute()
    )
    if existing.data:
        return existing.data

    # Get the parent keyword
    gap = sb.table("keyword_gaps").select("keyword").eq("id", gap_id).single().execute()
    if not gap.data:
        return []

    # Fetch from DataForSEO
    suggestions = await dataforseo_client.get_keyword_suggestions(
        gap.data["keyword"]
    )

    # Store results
    if suggestions:
        records = [
            {
                "keyword_gap_id": gap_id,
                "keyword": s["keyword"],
                "volume": s["volume"],
                "kd": s["kd"],
                "intent": s.get("intent"),
            }
            for s in suggestions
        ]
        sb.table("long_tail_keywords").insert(records).execute()

        stored = (
            sb.table("long_tail_keywords")
            .select("*")
            .eq("keyword_gap_id", gap_id)
            .execute()
        )
        return stored.data

    return []


async def add_selected_keyword(
    project_id: str,
    user_id: str,
    keyword: str,
    volume: int,
    kd: int,
    intent: str | None,
    long_tail_keywords: list[dict],
) -> dict | None:
    project = await get_project(project_id, user_id)
    if not project:
        return None

    sb = _get_supabase()
    result = (
        sb.table("selected_keywords")
        .insert(
            {
                "project_id": project_id,
                "keyword": keyword,
                "volume": volume,
                "kd": kd,
                "intent": intent,
                "long_tail_keywords": long_tail_keywords,
            }
        )
        .execute()
    )
    return result.data[0]


async def get_selected_keywords(project_id: str, user_id: str) -> list[dict]:
    project = await get_project(project_id, user_id)
    if not project:
        return []

    sb = _get_supabase()
    result = (
        sb.table("selected_keywords")
        .select("*")
        .eq("project_id", project_id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data


async def delete_selected_keyword(
    project_id: str, keyword_id: str, user_id: str
) -> bool:
    project = await get_project(project_id, user_id)
    if not project:
        return False

    sb = _get_supabase()
    sb.table("selected_keywords").delete().eq("id", keyword_id).eq(
        "project_id", project_id
    ).execute()
    return True
