"""Analytics API endpoints."""

import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.analytics import (
    AnalyticsOverview,
    RouteUsageStats,
    AgentHealthStats,
    FeatureUsageStats,
)
from app.services.analytics import AnalyticsService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


async def get_analytics_service(db: AsyncSession = Depends(get_db)) -> AnalyticsService:
    """Get analytics service."""
    return AnalyticsService(db)


@router.get("/overview", response_model=AnalyticsOverview)
async def get_analytics_overview(
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> AnalyticsOverview:
    """Get overview statistics."""
    try:
        overview = await analytics_service.get_overview()
        return overview
    except Exception as e:
        logger.error(f"Error getting analytics overview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/routes/usage", response_model=RouteUsageStats)
async def get_route_usage_stats(
    start_date: datetime = None,
    end_date: datetime = None,
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> RouteUsageStats:
    """Get route usage statistics."""
    try:
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        stats = await analytics_service.get_route_usage_stats(start_date, end_date)
        return stats
    except Exception as e:
        logger.error(f"Error getting route usage stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/agents/health", response_model=AgentHealthStats)
async def get_agent_health_stats(
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> AgentHealthStats:
    """Get agent health statistics."""
    try:
        stats = await analytics_service.get_agent_health_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting agent health stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/features/usage", response_model=FeatureUsageStats)
async def get_feature_usage_stats(
    start_date: datetime = None,
    end_date: datetime = None,
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> FeatureUsageStats:
    """Get feature usage statistics."""
    try:
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        stats = await analytics_service.get_feature_usage_stats(start_date, end_date)
        return stats
    except Exception as e:
        logger.error(f"Error getting feature usage stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
