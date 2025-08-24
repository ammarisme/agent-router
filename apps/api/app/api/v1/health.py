"""Health check endpoints."""

import os
from typing import Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import get_redis
from app.db.session import get_db

router = APIRouter()


@router.get("/live")
async def health_live() -> Dict[str, str]:
    """Liveness probe - check if process is running."""
    return {"status": "alive"}


@router.get("/ready")
async def health_ready(
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Readiness probe - check if service is ready to serve requests."""
    checks = {
        "database": False,
        "redis": False,
    }
    
    # Check database
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        checks["database"] = True
    except Exception:
        pass
    
    # Check Redis
    try:
        redis_client = await get_redis()
        await redis_client.ping()
        checks["redis"] = True
    except Exception:
        pass
    
    # Check if all services are healthy
    all_healthy = all(checks.values())
    
    return {
        "status": "ready" if all_healthy else "not_ready",
        "checks": checks,
    }
