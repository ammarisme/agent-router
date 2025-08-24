"""Pydantic schemas for API requests and responses."""

from .auth import (
    SignInRequest,
    SignInResponse,
    SignUpRequest,
    SignUpResponse,
    UserResponse,
)
from .agents import (
    AgentCreate,
    AgentResponse,
    AgentListResponse,
    DiscoverAgentsRequest,
    AgentHealthResponse,
)
from .features import (
    FeatureCreate,
    FeatureResponse,
    FeatureListResponse,
    DiscoverFeaturesRequest,
)
from .routes import (
    RouteCreate,
    RouteResponse,
    RouteListResponse,
    RouteCondition,
)
from .roles import (
    RoleCreate,
    RoleResponse,
    RoleListResponse,
    ImportIAMRolesRequest,
)
from .analytics import (
    AnalyticsOverview,
    RouteUsageStats,
    AgentHealthStats,
    FeatureUsageStats,
)
from .system import (
    SystemHealth,
    SystemConfig,
    SystemLogs,
    ActivityLogs,
)

__all__ = [
    # Auth
    "SignInRequest",
    "SignInResponse", 
    "SignUpRequest",
    "SignUpResponse",
    "UserResponse",
    # Agents
    "AgentCreate",
    "AgentResponse",
    "AgentListResponse",
    "DiscoverAgentsRequest",
    "AgentHealthResponse",
    # Features
    "FeatureCreate",
    "FeatureResponse",
    "FeatureListResponse",
    "DiscoverFeaturesRequest",
    # Routes
    "RouteCreate",
    "RouteResponse",
    "RouteListResponse",
    "RouteCondition",
    # Roles
    "RoleCreate",
    "RoleResponse",
    "RoleListResponse",
    "ImportIAMRolesRequest",
    # Analytics
    "AnalyticsOverview",
    "RouteUsageStats",
    "AgentHealthStats",
    "FeatureUsageStats",
    # System
    "SystemHealth",
    "SystemConfig",
    "SystemLogs",
    "ActivityLogs",
]
