"""Analytics schemas."""

from datetime import datetime
from typing import Dict, Any, List

from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    """Analytics overview schema."""
    total_agents: int
    total_features: int
    total_routes: int
    total_users: int
    healthy_agents: int
    active_routes: int
    system_uptime: str
    last_updated: datetime


class RouteUsageStats(BaseModel):
    """Route usage statistics schema."""
    total_routes: int
    active_routes: int
    period_start: datetime
    period_end: datetime
    usage_data: List[Dict[str, Any]]
    total_requests: int
    avg_response_time: float


class AgentHealthStats(BaseModel):
    """Agent health statistics schema."""
    total_agents: int
    healthy_agents: int
    unhealthy_agents: int
    health_percentage: float
    health_by_source: List[Dict[str, Any]]
    last_check: datetime


class FeatureUsageStats(BaseModel):
    """Feature usage statistics schema."""
    total_features: int
    active_features: int
    period_start: datetime
    period_end: datetime
    usage_by_store: List[Dict[str, Any]]
    total_requests: int
    avg_features_per_store: float
