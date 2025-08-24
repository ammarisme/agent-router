"""Agent schemas."""

from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class AgentBase(BaseModel):
    """Base agent schema."""
    name: str = Field(..., min_length=1, max_length=255, description="Agent name")
    description: Optional[str] = Field(None, description="Agent description")
    source_type: str = Field(..., description="Agent source type (MCP, A2A, WORKFLOW)")
    endpoint: HttpUrl = Field(..., description="Agent endpoint URL")
    api_key: Optional[str] = Field(None, description="API key for authentication")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AgentCreate(BaseModel):
    """Agent creation schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    source_type: str = Field(..., pattern="^(MCP|A2A|WORKFLOW)$")
    endpoint: str = Field(..., min_length=1, max_length=500)
    api_key: str = Field(..., min_length=1, max_length=500)
    config_data: Optional[Dict[str, Any]] = Field(default_factory=dict)


class AgentUpdate(BaseModel):
    """Update agent request schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Agent name")
    description: Optional[str] = Field(None, description="Agent description")
    source_type: Optional[str] = Field(None, description="Agent source type (MCP, A2A, WORKFLOW)")
    endpoint: Optional[HttpUrl] = Field(None, description="Agent endpoint URL")
    api_key: Optional[str] = Field(None, description="API key for authentication")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class AgentResponse(BaseModel):
    """Agent response schema."""
    id: UUID
    name: str
    description: str
    source_type: str
    endpoint: str
    api_key: str
    status: str
    health: str
    config_data: Dict[str, Any]

    class Config:
        from_attributes = True


class AgentListResponse(BaseModel):
    """Agent list response schema."""
    agents: List[AgentResponse] = Field(..., description="List of agents")
    total: int = Field(..., description="Total number of agents")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")


class DiscoverAgentsRequest(BaseModel):
    """Agent discovery request schema."""
    source_type: str = Field(..., pattern="^(MCP|A2A|WORKFLOW)$")
    endpoint: Optional[str] = None
    credentials: Optional[Dict[str, Any]] = None


class DiscoveredAgent(BaseModel):
    """Discovered agent schema."""
    name: str = Field(..., description="Agent name")
    description: Optional[str] = Field(None, description="Agent description")
    capabilities: List[str] = Field(default_factory=list, description="Agent capabilities")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class DiscoverAgentsResponse(BaseModel):
    """Discover agents response schema."""
    agents: List[DiscoveredAgent] = Field(..., description="List of discovered agents")
    total: int = Field(..., description="Total number of discovered agents")


class AgentHealthCheck(BaseModel):
    """Agent health check response schema."""
    agent_id: UUID = Field(..., description="Agent unique identifier")
    status: str = Field(..., description="Health status (healthy, unhealthy)")
    response_time: Optional[float] = Field(None, description="Response time in milliseconds")
    last_check: datetime = Field(..., description="Last health check timestamp")
    details: Dict[str, Any] = Field(default_factory=dict, description="Health check details")


class TestConnectionRequest(BaseModel):
    """Test agent connection request schema."""
    endpoint: HttpUrl = Field(..., description="Agent endpoint URL")
    api_key: Optional[str] = Field(None, description="API key for authentication")


class TestConnectionResponse(BaseModel):
    """Test agent connection response schema."""
    success: bool = Field(..., description="Connection test result")
    message: str = Field(..., description="Connection test message")
    response_time: Optional[float] = Field(None, description="Response time in milliseconds")
    details: Dict[str, Any] = Field(default_factory=dict, description="Connection test details")


class AgentHealthResponse(BaseModel):
    """Agent health response schema."""
    agent_id: UUID
    agent_name: str
    status: str
    details: Dict[str, Any]
