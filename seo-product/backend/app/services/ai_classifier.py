import json
import logging

import anthropic

from app.config import get_settings

logger = logging.getLogger(__name__)


async def classify_keywords(
    keywords: list[dict], niche: str, domain: str
) -> list[dict]:
    """Use Claude to classify keywords into niche-relevant categories."""
    settings = get_settings()
    if not settings.anthropic_api_key:
        logger.warning("Anthropic API key not set, skipping AI classification")
        return keywords

    # Build keyword list for Claude (send keyword + volume + kd)
    kw_lines = []
    for kw in keywords:
        kw_lines.append(
            f"{kw['keyword']}|{kw.get('volume', 0)}|{kw.get('kd', 0)}|{kw.get('cpc', 0)}"
        )
    kw_block = "\n".join(kw_lines)

    prompt = f"""You are an SEO keyword analyst. Analyze these keywords for the domain "{domain}" in the "{niche}" niche.

For each keyword, return a JSON array where each item has:
- "keyword": the exact keyword string
- "category": a niche-relevant category name (create 8-15 categories that make sense for this specific niche/business — NOT generic SEO categories)
- "city": city name if the keyword contains a city/location, otherwise null
- "difficulty": "Very Easy" if KD 0-10, "Easy" if 11-20, "Moderate" if 21-40, "Hard" if 41+
- "tier": "T1" if volume >= 1000, "T2" otherwise
- "is_long_tail": true if 4+ words, false otherwise

IMPORTANT RULES:
- Categories must be specific to the "{niche}" niche. For example, if the niche is apartment rentals, categories might be "Renter Education", "Pet Friendly", "Bedroom Type", "Price & Budget", "Near Me", "Student Housing", "Luxury", "Property Specific", etc.
- If the niche were plumbing, categories would be completely different: "Emergency Repairs", "Drain & Sewer", "Water Heater", "Fixture Installation", "Commercial Plumbing", etc.
- Create categories based on what actually appears in the keyword data
- Every keyword must have a category — use "General" only as last resort
- Return ONLY the JSON array, no other text

Keywords (format: keyword|volume|kd|cpc):
{kw_block}"""

    try:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.content[0].text.strip()

        # Extract JSON from response (handle markdown code blocks)
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]

        classified = json.loads(text)

        # Build lookup by keyword
        lookup = {item["keyword"]: item for item in classified}

        # Merge classifications back into original keywords
        enriched = []
        for kw in keywords:
            cls = lookup.get(kw["keyword"], {})
            word_count = len(kw["keyword"].split())
            enriched.append(
                {
                    **kw,
                    "category": cls.get("category", "General"),
                    "city": cls.get("city"),
                    "difficulty": cls.get("difficulty", _compute_difficulty(kw.get("kd", 0))),
                    "tier": cls.get("tier", "T1" if kw.get("volume", 0) >= 1000 else "T2"),
                    "is_long_tail": cls.get("is_long_tail", word_count >= 4),
                    "word_count": word_count,
                }
            )

        logger.info(
            f"AI classified {len(enriched)} keywords into "
            f"{len(set(e['category'] for e in enriched))} categories"
        )
        return enriched

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response: {e}")
        return _fallback_enrich(keywords)
    except Exception as e:
        logger.error(f"AI classification failed: {e}")
        return _fallback_enrich(keywords)


def _compute_difficulty(kd: int) -> str:
    if kd <= 10:
        return "Very Easy"
    elif kd <= 20:
        return "Easy"
    elif kd <= 40:
        return "Moderate"
    return "Hard"


def _fallback_enrich(keywords: list[dict]) -> list[dict]:
    """Basic enrichment without AI."""
    from app.services.dataforseo import DataForSEOClient

    enriched = []
    for kw in keywords:
        extra = DataForSEOClient.enrich_keyword(
            kw["keyword"], kw.get("volume", 0), kw.get("kd", 0), kw.get("cpc", 0)
        )
        enriched.append({**kw, **extra})
    return enriched
