"""Analytics service."""

import logging
from datetime import datetime
from typing import List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Agent, Feature, Route, User
from app.schemas.analytics import (
    AnalyticsOverview,
    RouteUsageStats,
    AgentHealthStats,
    FeatureUsageStats,
)

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Analytics service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_overview(self) -> AnalyticsOverview:
        """Get overview statistics."""
        # Get counts
        agent_count = await self._get_agent_count()
        feature_count = await self._get_feature_count()
        route_count = await self._get_route_count()
        user_count = await self._get_user_count()
        
        # Get health status
        healthy_agents = await self._get_healthy_agent_count()
        active_routes = await self._get_active_route_count()
        
        return AnalyticsOverview(
            total_agents=agent_count,
            total_features=feature_count,
            total_routes=route_count,
            total_users=user_count,
            healthy_agents=healthy_agents,
            active_routes=active_routes,
            system_uptime="99.9%",
            last_updated=datetime.now()
        )

    async def get_route_usage_stats(self, start_date: datetime, end_date: datetime) -> RouteUsageStats:
        """Get route usage statistics."""
        # Mock implementation - in production, this would query actual usage logs
        total_routes = await self._get_route_count()
        active_routes = await self._get_active_route_count()
        
        # Mock usage data
        usage_data = [
            {"route_id": "route-1", "usage_count": 150, "avg_response_time": 250},
            {"route_id": "route-2", "usage_count": 89, "avg_response_time": 180},
            {"route_id": "route-3", "usage_count": 234, "avg_response_time": 320},
        ]
        
        return RouteUsageStats(
            total_routes=total_routes,
            active_routes=active_routes,
            period_start=start_date,
            period_end=end_date,
            usage_data=usage_data,
            total_requests=sum(item["usage_count"] for item in usage_data),
            avg_response_time=sum(item["avg_response_time"] for item in usage_data) / len(usage_data)
        )

    async def get_agent_health_stats(self) -> AgentHealthStats:
        """Get agent health statistics."""
        total_agents = await self._get_agent_count()
        healthy_agents = await self._get_healthy_agent_count()
        unhealthy_agents = total_agents - healthy_agents
        
        # Mock health data by source type
        health_by_source = [
            {"source_type": "MCP", "healthy": 5, "unhealthy": 1},
            {"source_type": "A2A", "healthy": 3, "unhealthy": 0},
            {"source_type": "WORKFLOW", "healthy": 2, "unhealthy": 1},
        ]
        
        return AgentHealthStats(
            total_agents=total_agents,
            healthy_agents=healthy_agents,
            unhealthy_agents=unhealthy_agents,
            health_percentage=(healthy_agents / total_agents * 100) if total_agents > 0 else 0,
            health_by_source=health_by_source,
            last_check=datetime.now()
        )

    async def get_feature_usage_stats(self, start_date: datetime, end_date: datetime) -> FeatureUsageStats:
        """Get feature usage statistics."""
        total_features = await self._get_feature_count()
        active_features = await self._get_active_feature_count()
        
        # Mock usage data by store type
        usage_by_store = [
            {"store_type": "HTTP_JSON", "usage_count": 450, "feature_count": 8},
            {"store_type": "GIT", "usage_count": 234, "feature_count": 5},
            {"store_type": "S3", "usage_count": 189, "feature_count": 3},
            {"store_type": "GCS", "usage_count": 156, "feature_count": 2},
        ]
        
        return FeatureUsageStats(
            total_features=total_features,
            active_features=active_features,
            period_start=start_date,
            period_end=end_date,
            usage_by_store=usage_by_store,
            total_requests=sum(item["usage_count"] for item in usage_by_store),
            avg_features_per_store=sum(item["feature_count"] for item in usage_by_store) / len(usage_by_store)
        )

    async def _get_agent_count(self) -> int:
        """Get total agent count."""
        result = await self.db.execute(select(func.count(Agent.id)))
        return result.scalar() or 0

    async def _get_feature_count(self) -> int:
        """Get total feature count."""
        result = await self.db.execute(select(func.count(Feature.id)))
        return result.scalar() or 0

    async def _get_route_count(self) -> int:
        """Get total route count."""
        result = await self.db.execute(select(func.count(Route.id)))
        return result.scalar() or 0

    async def _get_user_count(self) -> int:
        """Get total user count."""
        result = await self.db.execute(select(func.count(User.id)))
        return result.scalar() or 0

    async def _get_healthy_agent_count(self) -> int:
        """Get healthy agent count."""
        result = await self.db.execute(
            select(func.count(Agent.id)).where(Agent.health == "healthy")
        )
        return result.scalar() or 0

    async def _get_active_route_count(self) -> int:
        """Get active route count."""
        result = await self.db.execute(
            select(func.count(Route.id)).where(Route.status == "active")
        )
        return result.scalar() or 0

    async def _get_active_feature_count(self) -> int:
        """Get active feature count."""
        result = await self.db.execute(
            select(func.count(Feature.id)).where(Feature.status == "active")
        )
        return result.scalar() or 0
