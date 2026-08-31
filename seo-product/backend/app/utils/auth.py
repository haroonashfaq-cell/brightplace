from fastapi import HTTPException, status
from supabase import create_client

from app.config import get_settings


def verify_jwt(token: str) -> dict:
    """Verify a Supabase JWT by calling Supabase auth.getUser()."""
    settings = get_settings()

    if not settings.supabase_url or not settings.supabase_anon_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase not configured",
        )

    try:
        sb = create_client(settings.supabase_url, settings.supabase_anon_key)
        user_response = sb.auth.get_user(token)
        user = user_response.user

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        return {"sub": user.id, "email": user.email or ""}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
