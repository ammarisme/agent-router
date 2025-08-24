"""System management API endpoints."""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.system import (
    SystemHealth,
    SystemConfig,
    SystemLogs,
    ActivityLogs,
)
from app.services.system import SystemService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/system", tags=["System"])


async def get_system_service(db: AsyncSession = Depends(get_db)) -> SystemService:
    """Get system service."""
    return SystemService(db)


@router.get("/health", response_model=SystemHealth)
async def get_system_health(
    system_service: SystemService = Depends(get_system_service),
) -> SystemHealth:
    """Get system health check."""
    try:
        health = await system_service.get_system_health()
        return health
    except Exception as e:
        logger.error(f"Error getting system health: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/config", response_model=SystemConfig)
async def get_system_config(
    system_service: SystemService = Depends(get_system_service),
) -> SystemConfig:
    """Get system configuration."""
    try:
        config = await system_service.get_system_config()
        return config
    except Exception as e:
        logger.error(f"Error getting system config: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/logs", response_model=SystemLogs)
async def get_system_logs(
    level: str = "INFO",
    limit: int = 100,
    system_service: SystemService = Depends(get_system_service),
) -> SystemLogs:
    """Get system logs."""
    try:
        logs = await system_service.get_system_logs(level=level, limit=limit)
        return logs
    except Exception as e:
        logger.error(f"Error getting system logs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/activity", response_model=ActivityLogs)
async def get_activity_logs(
    limit: int = 100,
    system_service: SystemService = Depends(get_system_service),
) -> ActivityLogs:
    """Get activity logs."""
    try:
        logs = await system_service.get_activity_logs(limit=limit)
        return logs
    except Exception as e:
        logger.error(f"Error getting activity logs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
