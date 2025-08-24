"""Agent management API endpoints."""

import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.agents import (
    AgentCreate,
    AgentResponse,
    AgentListResponse,
    DiscoverAgentsRequest,
    AgentHealthResponse,
)
from app.services.agents import AgentService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agents", tags=["Agents"])


async def get_agent_service(db: AsyncSession = Depends(get_db)) -> AgentService:
    """Get agent service."""
    return AgentService(db)


@router.get("", response_model=AgentListResponse)
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    page: int = None,
    size: int = None,
    agent_service: AgentService = Depends(get_agent_service),
) -> AgentListResponse:
    """List all agents with pagination support for both skip/limit and page/size formats."""
    # Support both pagination formats
    if page is not None and size is not None:
        skip = (page - 1) * size
        limit = size
    """List all agents."""
    try:
        agents = await agent_service.list_agents(skip=skip, limit=limit)
        total = len(agents)  # In a real app, you'd get total count from DB
        
        # Calculate pagination info
        current_page = (skip // limit) + 1 if limit > 0 else 1
        total_pages = (total + limit - 1) // limit if limit > 0 else 1
        
        return AgentListResponse(
            agents=agents, 
            total=total,
            page=current_page,
            size=limit,
            pages=total_pages
        )
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    agent_service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    """Create a new agent."""
    try:
        agent = await agent_service.create_agent(agent_data)
        logger.info(f"Created agent: {agent.name}")
        return agent
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    agent_service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    """Get agent details."""
    try:
        agent = await agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        return agent
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: UUID,
    agent_data: AgentCreate,
    agent_service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    """Update an agent."""
    try:
        agent = await agent_service.update_agent(agent_id, agent_data)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        logger.info(f"Updated agent: {agent.name}")
        return agent
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: UUID,
    agent_service: AgentService = Depends(get_agent_service),
):
    """Delete an agent."""
    try:
        success = await agent_service.delete_agent(agent_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        logger.info(f"Deleted agent: {agent_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/discover", response_model=List[AgentResponse])
async def discover_agents(
    discovery_request: DiscoverAgentsRequest,
    agent_service: AgentService = Depends(get_agent_service),
) -> List[AgentResponse]:
    """Discover agents from external sources (MCP, A2A, Workflow)."""
    try:
        agents = await agent_service.discover_agents(discovery_request)
        logger.info(f"Discovered {len(agents)} agents from {discovery_request.source_type}")
        return agents
    except Exception as e:
        logger.error(f"Error discovering agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during agent discovery"
        )


@router.get("/{agent_id}/health", response_model=AgentHealthResponse)
async def get_agent_health(
    agent_id: UUID,
    agent_service: AgentService = Depends(get_agent_service),
) -> AgentHealthResponse:
    """Check agent health status."""
    try:
        health = await agent_service.check_agent_health(agent_id)
        if not health:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        return health
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking agent health: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
