import base64
import logging

import httpx

from app.config import get_settings
from app.utils.cache import cache

logger = logging.getLogger(__name__)

BASE_URL = "https://api.dataforseo.com/v3"


class DataForSEOClient:
    """Client for DataForSEO API with caching."""

    def __init__(self):
        settings = get_settings()
        self.login = settings.dataforseo_login
        self.password = settings.dataforseo_password
        self.enabled = bool(self.login and self.password)

    def _auth_header(self) -> dict:
        creds = base64.b64encode(
            f"{self.login}:{self.password}".encode()
        ).decode()
        return {
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/json",
        }

    async def _post(self, endpoint: str, payload: list[dict]) -> dict:
        """Make a POST request to DataForSEO."""
        if not self.enabled:
            logger.warning("DataForSEO not configured, returning mock data")
            return {"status_code": 20000, "tasks": []}

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{BASE_URL}{endpoint}",
                json=payload,
                headers=self._auth_header(),
            )
            resp.raise_for_status()
            data = resp.json()

            if data.get("status_code") != 20000:
                logger.error(f"DataForSEO error: {data.get('status_message')}")

            cost = data.get("cost", 0)
            if cost:
                logger.info(f"DataForSEO cost: ${cost}")

            return data

    async def detect_competitors(
        self, domain: str, location_code: int = 2840, limit: int = 10
    ) -> list[dict]:
        """Auto-detect organic competitors for a domain."""
        cache_key = f"competitors:{domain}:{location_code}"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        data = await self._post(
            "/dataforseo_labs/google/competitors_domain/live",
            [
                {
                    "target": domain,
                    "location_code": location_code,
                    "language_code": "en",
                    "limit": limit,
                }
            ],
        )

        competitors = []
        tasks = data.get("tasks", [])
        if tasks and tasks[0].get("result"):
            for res in tasks[0]["result"]:
                for item in res.get("items", []):
                    # Skip the target domain itself and generic sites
                    item_domain = item.get("domain", "")
                    skip = {domain, "facebook.com", "youtube.com", "reddit.com",
                            "quora.com", "wikipedia.org", "twitter.com", "x.com",
                            "linkedin.com", "instagram.com", "pinterest.com", "tiktok.com"}
                    if item_domain in skip:
                        continue
                    competitors.append(
                        {
                            "domain": item_domain,
                            "avg_position": item.get("avg_position"),
                            "sum_position": item.get("sum_position"),
                            "intersections": item.get("intersections"),
                            "full_domain_metrics": item.get(
                                "full_domain_metrics", {}
                            ),
                        }
                    )

        if competitors:
            await cache.set(cache_key, competitors)
        return competitors

    async def get_keyword_gaps(
        self,
        competitors: list[str],
        exclude_domain: str,
        location_code: int = 2840,
        limit: int = 100,
        offset: int = 0,
        filters: list | None = None,
        order_by: list[str] | None = None,
    ) -> dict:
        """Get keyword gaps between competitors and target domain."""
        cache_key = (
            f"gaps:{exclude_domain}:{','.join(sorted(competitors))}"
            f":{offset}:{limit}"
        )
        cached = await cache.get(cache_key)
        if cached:
            return cached

        # Filter out the user's own domain from competitors
        comp_list = [c for c in competitors if c != exclude_domain][:3]

        payload: dict = {
            "location_code": location_code,
            "language_code": "en",
            "limit": limit,
            "offset": offset,
        }
        # DataForSEO expects target1, target2, target3 as separate keys
        for i, c in enumerate(comp_list):
            payload[f"target{i + 1}"] = c
        if filters:
            payload["filters"] = filters
        if order_by:
            payload["order_by"] = order_by
        else:
            payload["order_by"] = [
                "keyword_data.keyword_info.search_volume,desc"
            ]

        data = await self._post(
            "/dataforseo_labs/google/domain_intersection/live", [payload]
        )

        result = {"items": [], "total_count": 0}
        tasks = data.get("tasks", [])
        if tasks and tasks[0].get("result"):
            res = tasks[0]["result"][0] if tasks[0]["result"] else {}
            result["total_count"] = res.get("total_count", 0)
            for item in res.get("items", []):
                kw_data = item.get("keyword_data", {})
                kw_info = kw_data.get("keyword_info", {})
                keyword = kw_data.get("keyword", "")
                volume = kw_info.get("search_volume", 0) or 0
                kd = kw_info.get("keyword_difficulty", 0) or 0
                cpc = kw_info.get("cpc", 0) or 0

                enriched = self.enrich_keyword(keyword, volume, kd, cpc)

                result["items"].append(
                    {
                        "keyword": keyword,
                        "volume": volume,
                        "kd": kd,
                        "intent": self._extract_intent(
                            kw_data.get("search_intent_info", {})
                        ),
                        "competitor_domains": comp_list,
                        **enriched,
                    }
                )

        if result["items"]:
            await cache.set(cache_key, result)
        return result

    async def get_keyword_suggestions(
        self,
        keyword: str,
        location_code: int = 2840,
        limit: int = 20,
    ) -> list[dict]:
        """Get long-tail keyword suggestions for a seed keyword."""
        cache_key = f"suggestions:{keyword}:{location_code}"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        data = await self._post(
            "/dataforseo_labs/google/keyword_suggestions/live",
            [
                {
                    "keyword": keyword,
                    "location_code": location_code,
                    "language_code": "en",
                    "limit": limit,
                    "filters": [
                        ["keyword_info.search_volume", ">", 100],
                        ["keyword_info.keyword_difficulty", "<", 30],
                    ],
                }
            ],
        )

        suggestions = []
        tasks = data.get("tasks", [])
        if tasks and tasks[0].get("result"):
            for item in tasks[0]["result"]:
                kw_info = item.get("keyword_info", {})
                suggestions.append(
                    {
                        "keyword": item.get("keyword", ""),
                        "volume": kw_info.get("search_volume", 0),
                        "kd": kw_info.get("keyword_difficulty", 0),
                        "intent": self._extract_intent(
                            item.get("search_intent_info", {})
                        ),
                    }
                )

        if suggestions:
            await cache.set(cache_key, suggestions)
        return suggestions

    async def get_keyword_ideas(
        self,
        seed_keywords: list[str],
        location_code: int = 2840,
        limit: int = 100,
    ) -> list[dict]:
        """Get keyword ideas from seed keywords (like SEMrush keyword magic tool)."""
        cache_key = f"ideas:{','.join(sorted(seed_keywords))}:{location_code}:{limit}"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        data = await self._post(
            "/dataforseo_labs/google/keyword_ideas/live",
            [
                {
                    "keywords": seed_keywords,
                    "location_code": location_code,
                    "language_code": "en",
                    "limit": limit,
                    "include_seed_keyword": True,
                    "order_by": ["keyword_info.search_volume,desc"],
                }
            ],
        )

        keywords = []
        tasks = data.get("tasks", [])
        if tasks and tasks[0].get("result"):
            for res in tasks[0]["result"]:
                for item in res.get("items", []):
                    ki = item.get("keyword_info", {})
                    volume = ki.get("search_volume", 0) or 0
                    cpc = ki.get("cpc", 0) or 0
                    keywords.append(
                        {
                            "keyword": item.get("keyword", ""),
                            "volume": volume,
                            "kd": 0,  # Will be filled by bulk_keyword_difficulty
                            "cpc": cpc,
                            "competition": ki.get("competition", 0),
                            "intent": self._extract_intent(
                                item.get("search_intent_info", {})
                            ),
                        }
                    )

        if keywords:
            await cache.set(cache_key, keywords)
        return keywords

    async def get_bulk_keyword_difficulty(
        self,
        keywords: list[str],
        location_code: int = 2840,
    ) -> dict[str, int]:
        """Get keyword difficulty scores for a batch of keywords."""
        if not keywords:
            return {}

        # DataForSEO allows max 1000 keywords per request
        kd_map: dict[str, int] = {}
        for i in range(0, len(keywords), 1000):
            batch = keywords[i : i + 1000]
            data = await self._post(
                "/dataforseo_labs/google/bulk_keyword_difficulty/live",
                [
                    {
                        "keywords": batch,
                        "location_code": location_code,
                        "language_code": "en",
                    }
                ],
            )

            tasks = data.get("tasks", [])
            if tasks and tasks[0].get("result"):
                for res in tasks[0]["result"]:
                    for item in res.get("items", []):
                        kw = item.get("keyword", "")
                        kd = item.get("keyword_difficulty", 0) or 0
                        kd_map[kw] = kd

        return kd_map

    async def get_search_volume(
        self,
        keywords: list[str],
        location_code: int = 2840,
    ) -> list[dict]:
        """Get search volume and KD for a list of keywords."""
        data = await self._post(
            "/keywords_data/google_ads/search_volume/live",
            [
                {
                    "keywords": keywords,
                    "location_code": location_code,
                    "language_code": "en",
                }
            ],
        )

        results = []
        tasks = data.get("tasks", [])
        if tasks and tasks[0].get("result"):
            for item in tasks[0]["result"]:
                results.append(
                    {
                        "keyword": item.get("keyword", ""),
                        "volume": item.get("search_volume", 0),
                        "competition": item.get("competition", ""),
                    }
                )
        return results

    @staticmethod
    def _extract_intent(intent_info: dict) -> str:
        """Extract primary search intent."""
        if not intent_info:
            return "unknown"
        main_intent = intent_info.get("main_intent", "")
        if main_intent:
            return main_intent
        return "unknown"

    @staticmethod
    def enrich_keyword(keyword: str, volume: int, kd: int, cpc: float = 0) -> dict:
        """Compute derived fields for a keyword."""
        word_count = len(keyword.split())
        is_long_tail = word_count >= 4

        # Difficulty label
        if kd <= 10:
            difficulty = "Very Easy"
        elif kd <= 20:
            difficulty = "Easy"
        elif kd <= 40:
            difficulty = "Moderate"
        else:
            difficulty = "Hard"

        # Tier
        tier = "T1" if volume >= 1000 else "T2"

        # Category classification — covers multiple niches
        kw_lower = keyword.lower()
        category = "General"
        category_rules = [
            # === Apartment / Rental niche ===
            ("pet friendly", ["pet friendly", "pet-friendly", "dog friendly", "cat friendly", "pets allowed", "pet deposit", "pet fee", "pet rent", "pet policy"]),
            ("Bedroom Type", ["1 bedroom", "2 bedroom", "3 bedroom", "4 bedroom", "one bedroom", "two bedroom", "three bedroom", "studio apartment", "studio for rent"]),
            ("Near Me", ["near me", "nearby", "close to", "in my area"]),
            ("Price & Budget", ["cheap", "affordable", "low income", "income restricted", "income based", "section 8", "low cost", "budget", "under $", "price", "how much", "cost of rent", "prorated", "rent affordability"]),
            ("Student & Campus", ["student", "campus", "university", "college", "dorm"]),
            ("Luxury", ["luxury", "high end", "upscale", "penthouse", "high rise"]),
            ("Furnished & Short-Term", ["furnished", "short term", "short-term", "month to month", "temporary", "sublet", "sublease", "corporate housing"]),
            ("Property Type", ["townhouse", "duplex", "condo", "loft", "house for rent", "single family", "mobile home", "tiny home"]),
            ("Renter Education", ["how to", "what is", "what does", "what are", "guide", "tips", "checklist", "vs", "pros and cons", "should i", "can i", "do i need", "questions to ask", "things to know"]),
            # === Plumbing niche ===
            ("Emergency Repairs", ["emergency plumb", "burst pipe", "flooding", "no hot water", "clogged toilet", "sewage backup", "broken pipe", "water leak emergency"]),
            ("Drain & Sewer", ["drain clean", "clogged drain", "sewer", "septic", "drain snake", "main line", "slow drain", "backed up"]),
            ("Water Heater", ["water heater", "tankless", "hot water", "water tank", "boiler"]),
            ("Fixture Installation", ["faucet", "toilet install", "sink install", "shower install", "bathtub", "bidet", "garbage disposal"]),
            ("Bathroom Plumbing", ["bathroom plumb", "shower", "bathtub", "toilet", "bathroom sink", "bathroom faucet", "bathroom remodel plumb"]),
            ("Kitchen Plumbing", ["kitchen plumb", "kitchen sink", "kitchen faucet", "dishwasher install", "kitchen drain"]),
            ("Commercial Plumbing", ["commercial plumb", "restaurant plumb", "office plumb", "industrial plumb", "backflow"]),
            ("Pipe & Leak Repair", ["pipe repair", "leak", "pipe burst", "copper pipe", "pvc pipe", "pipe replace", "repipe", "leak detection"]),
            ("Cost & Pricing", ["plumber cost", "plumbing cost", "how much does", "plumber price", "average cost", "plumbing estimate"]),
            # === Real Estate niche ===
            ("Buying Guide", ["how to buy", "buying a home", "home buying", "house hunting", "offer on house"]),
            ("Selling Guide", ["how to sell", "selling a home", "list my home", "home staging", "sell house fast"]),
            ("Mortgage & Finance", ["mortgage", "home loan", "interest rate", "down payment", "pre-approval", "refinance"]),
            ("First-Time Buyer", ["first time", "first-time", "starter home"]),
            ("Investment Property", ["investment property", "rental property", "flip", "roi", "cap rate", "cash flow"]),
            ("Market Trends", ["market trend", "housing market", "home prices", "real estate market"]),
        ]
        for cat_name, patterns in category_rules:
            if any(p in kw_lower for p in patterns):
                category = cat_name
                break

        # City extraction (common US cities)
        city = None
        cities = [
            "new york", "los angeles", "chicago", "houston", "phoenix", "philadelphia",
            "san antonio", "san diego", "dallas", "san jose", "austin", "jacksonville",
            "fort worth", "columbus", "charlotte", "indianapolis", "san francisco",
            "seattle", "denver", "washington", "nashville", "oklahoma city", "el paso",
            "boston", "portland", "las vegas", "memphis", "louisville", "baltimore",
            "milwaukee", "albuquerque", "tucson", "fresno", "sacramento", "mesa",
            "kansas city", "atlanta", "omaha", "colorado springs", "raleigh", "miami",
            "tampa", "orlando", "minneapolis", "st louis", "pittsburgh", "cincinnati",
            "greensboro", "plano", "madison", "knoxville", "greenville", "bloomington",
            "st augustine", "cambridge", "fullerton",
        ]
        for c in cities:
            if c in kw_lower:
                city = c.title()
                break

        return {
            "cpc": round(cpc, 2),
            "difficulty": difficulty,
            "category": category,
            "city": city,
            "is_long_tail": is_long_tail,
            "tier": tier,
            "word_count": word_count,
        }


dataforseo_client = DataForSEOClient()
