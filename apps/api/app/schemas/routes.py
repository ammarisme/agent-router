"""Route schemas."""

from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field


class RouteRules(BaseModel):
    """Route rules schema."""
    allowAll: bool = Field(default=False)
    allowed: List[str] = Field(default_factory=list)
    disallowed: List[str] = Field(default_factory=list)


class RouteCondition(BaseModel):
    """Route condition schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    condition_type: str = Field(..., pattern="^(role_based|time_based)$")
    condition_data: Dict[str, Any] = Field(default_factory=dict)


class RouteBase(BaseModel):
    """Base route schema."""
    feature_id: UUID = Field(..., description="Feature unique identifier")
    agent_id: UUID = Field(..., description="Agent unique identifier")
    rules: RouteRules = Field(..., description="Route access control rules")
    conditional: bool = Field(False, description="Whether this is a conditional route")
    conditions: List[RouteCondition] = Field(default_factory=list, description="Route conditions")


class RouteCreate(BaseModel):
    """Route creation schema."""
    feature_id: UUID
    agent_id: UUID
    rules: RouteRules
    conditional: bool = Field(default=False)


class RouteUpdate(BaseModel):
    """Update route request schema."""
    rules: Optional[RouteRules] = Field(None, description="Route access control rules")
    conditional: Optional[bool] = Field(None, description="Whether this is a conditional route")
    conditions: Optional[List[RouteCondition]] = Field(None, description="Route conditions")
    status: Optional[str] = Field(None, description="Route status (active, inactive)")


class RouteResponse(BaseModel):
    """Route response schema."""
    id: UUID
    feature_id: UUID
    agent_id: UUID
    rules: RouteRules
    conditional: bool
    status: str
    conditions: List[Dict[str, Any]] = Field(default_factory=list)

    class Config:
        from_attributes = True


class RouteListResponse(BaseModel):
    """Route list response schema."""
    routes: list[RouteResponse]
    total: int


class RouteTestRequest(BaseModel):
    """Test route request schema."""
    route_id: UUID = Field(..., description="Route unique identifier")
    user_roles: List[str] = Field(..., description="User roles to test")
    test_data: Optional[Dict[str, Any]] = Field(None, description="Test data")


class RouteTestResponse(BaseModel):
    """Test route response schema."""
    route_id: UUID = Field(..., description="Route unique identifier")
    allowed: bool = Field(..., description="Whether access is allowed")
    reason: str = Field(..., description="Reason for access decision")
    response_time: Optional[float] = Field(None, description="Response time in milliseconds")
    details: Dict[str, Any] = Field(default_factory=dict, description="Test details")


class RouteAnalytics(BaseModel):
    """Route analytics schema."""
    route_id: UUID = Field(..., description="Route unique identifier")
    total_requests: int = Field(..., description="Total number of requests")
    successful_requests: int = Field(..., description="Number of successful requests")
    failed_requests: int = Field(..., description="Number of failed requests")
    average_response_time: float = Field(..., description="Average response time in milliseconds")
    last_used: Optional[datetime] = Field(None, description="Last usage timestamp")
    usage_by_role: Dict[str, int] = Field(default_factory=dict, description="Usage by role")


class BulkRouteCreate(BaseModel):
    """Bulk create routes request schema."""
    routes: List[RouteCreate] = Field(..., description="List of routes to create")


class BulkRouteResponse(BaseModel):
    """Bulk route response schema."""
    created: List[RouteResponse] = Field(..., description="Successfully created routes")
    failed: List[Dict[str, Any]] = Field(..., description="Failed route creations")
    total_created: int = Field(..., description="Total number of created routes")
    total_failed: int = Field(..., description="Total number of failed creations")
