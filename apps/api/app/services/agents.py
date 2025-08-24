"""Agent service."""

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Agent
from app.schemas.agents import (
    AgentCreate,
    AgentResponse,
    DiscoverAgentsRequest,
    AgentHealthResponse,
)

logger = logging.getLogger(__name__)


class AgentService:
    """Agent service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_agents(self, skip: int = 0, limit: int = 100) -> List[AgentResponse]:
        """List all agents."""
        result = await self.db.execute(
            select(Agent).offset(skip).limit(limit)
        )
        agents = result.scalars().all()
        return [AgentResponse.from_orm(agent) for agent in agents]

    async def get_agent(self, agent_id: UUID) -> Optional[AgentResponse]:
        """Get agent by ID."""
        result = await self.db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        return AgentResponse.from_orm(agent) if agent else None

    async def create_agent(self, agent_data: AgentCreate) -> AgentResponse:
        """Create a new agent."""
        agent = Agent(
            name=agent_data.name,
            description=agent_data.description,
            source_type=agent_data.source_type,
            endpoint=agent_data.endpoint,
            api_key=agent_data.api_key,
            config_data=agent_data.config_data or {},
        )
        self.db.add(agent)
        await self.db.commit()
        await self.db.refresh(agent)
        return AgentResponse.from_orm(agent)

    async def update_agent(self, agent_id: UUID, agent_data: AgentCreate) -> Optional[AgentResponse]:
        """Update an agent."""
        result = await self.db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        if not agent:
            return None

        agent.name = agent_data.name
        agent.description = agent_data.description
        agent.source_type = agent_data.source_type
        agent.endpoint = agent_data.endpoint
        agent.api_key = agent_data.api_key
        agent.config_data = agent_data.config_data or {}

        await self.db.commit()
        await self.db.refresh(agent)
        return AgentResponse.from_orm(agent)

    async def delete_agent(self, agent_id: UUID) -> bool:
        """Delete an agent."""
        result = await self.db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        if not agent:
            return False

        await self.db.delete(agent)
        await self.db.commit()
        return True

    async def discover_agents(self, discovery_request: DiscoverAgentsRequest) -> List[AgentResponse]:
        """Discover agents from external sources."""
        # This is a mock implementation - in production, this would connect to
        # actual MCP servers, A2A registries, or workflow engines
        logger.info(f"Discovering agents from {discovery_request.source_type}")
        
        # Mock discovered agents based on source type
        mock_agents = []
        if discovery_request.source_type == "MCP":
            mock_agents = [
                Agent(
                    name="MCP Agent 1",
                    description="Mock MCP agent",
                    source_type="MCP",
                    endpoint="https://mcp-server-1.example.com",
                    api_key="mock-api-key",
                    config_data={"capabilities": ["text-generation", "file-access"]}
                ),
                Agent(
                    name="MCP Agent 2",
                    description="Another mock MCP agent",
                    source_type="MCP",
                    endpoint="https://mcp-server-2.example.com",
                    api_key="mock-api-key-2",
                    config_data={"capabilities": ["web-search", "image-generation"]}
                )
            ]
        elif discovery_request.source_type == "A2A":
            mock_agents = [
                Agent(
                    name="A2A Agent 1",
                    description="Mock A2A agent",
                    source_type="A2A",
                    endpoint="https://a2a-registry.example.com/agent1",
                    api_key="mock-a2a-key",
                    config_data={"registry": "example-registry"}
                )
            ]
        elif discovery_request.source_type == "WORKFLOW":
            mock_agents = [
                Agent(
                    name="Workflow Engine 1",
                    description="Mock workflow engine",
                    source_type="WORKFLOW",
                    endpoint="https://workflow-engine.example.com",
                    api_key="mock-workflow-key",
                    config_data={"engine_type": "temporal"}
                )
            ]

        # Save discovered agents to database
        for mock_agent in mock_agents:
            self.db.add(mock_agent)
        
        await self.db.commit()
        
        # Refresh to get IDs
        for agent in mock_agents:
            await self.db.refresh(agent)
        
        return [AgentResponse.from_orm(agent) for agent in mock_agents]

    async def check_agent_health(self, agent_id: UUID) -> Optional[AgentHealthResponse]:
        """Check agent health status."""
        result = await self.db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        if not agent:
            return None

        # Mock health check - in production, this would actually ping the agent
        import random
        is_healthy = random.choice([True, True, True, False])  # 75% healthy
        
        # Update agent health status
        agent.health = "healthy" if is_healthy else "unhealthy"
        await self.db.commit()

        return AgentHealthResponse(
            agent_id=agent.id,
            agent_name=agent.name,
            status="healthy" if is_healthy else "unhealthy",
            details={
                "endpoint": agent.endpoint,
                "last_check": "2024-01-01T00:00:00Z",
                "response_time": random.randint(10, 500) if is_healthy else None,
                "error": None if is_healthy else "Connection timeout"
            }
        )
