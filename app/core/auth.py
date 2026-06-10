from fastapi import Request, HTTPException, status
from app.config import get_settings


async def verify_api_key(request: Request) -> None:
    settings = get_settings()
    if settings.app_env == "development":
        return
    key = request.headers.get("X-API-Key")
    if not key or key != settings.api_secret_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API invalide ou manquante.",
        )
