from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Supabase
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_key: str = ""
    supabase_jwt_secret: str = ""

    # DataForSEO
    dataforseo_login: str = ""
    dataforseo_password: str = ""

    # Upstash Redis
    upstash_redis_url: str = ""
    upstash_redis_token: str = ""

    # Anthropic
    anthropic_api_key: str = ""

    # App
    frontend_url: str = "http://localhost:3000"
    environment: str = "development"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
