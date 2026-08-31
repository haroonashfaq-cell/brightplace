import json
import httpx

from app.config import get_settings


class RedisCache:
    """Upstash Redis REST API wrapper."""

    def __init__(self):
        settings = get_settings()
        self.url = settings.upstash_redis_url
        self.token = settings.upstash_redis_token
        self.enabled = bool(self.url and self.token)

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    async def get(self, key: str) -> dict | list | None:
        if not self.enabled:
            return None
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.url}/get/{key}", headers=self._headers()
                )
                data = resp.json()
                result = data.get("result")
                if result is None:
                    return None
                return json.loads(result)
        except Exception:
            return None

    async def set(self, key: str, value: dict | list, ttl: int = 604800) -> bool:
        """Set a key with optional TTL (default 7 days)."""
        if not self.enabled:
            return False
        try:
            async with httpx.AsyncClient() as client:
                payload = json.dumps(value)
                resp = await client.post(
                    f"{self.url}/set/{key}/{payload}/ex/{ttl}",
                    headers=self._headers(),
                )
                return resp.status_code == 200
        except Exception:
            return False

    async def delete(self, key: str) -> bool:
        if not self.enabled:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.url}/del/{key}", headers=self._headers()
                )
                return resp.status_code == 200
        except Exception:
            return False


cache = RedisCache()
