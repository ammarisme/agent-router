"""Route service."""

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Route, Condition, Agent, Feature
from app.schemas.routes import (
    RouteCreate,
    RouteResponse,
    RouteCondition,
)

logger = logging.getLogger(__name__)


class RouteService:
    """Route service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_routes(self, skip: int = 0, limit: int = 100) -> List[RouteResponse]:
        """List all routes."""
        result = await self.db.execute(
            select(Route).offset(skip).limit(limit)
        )
        routes = result.scalars().all()
        return [RouteResponse.from_orm(route) for route in routes]

    async def get_route(self, route_id: UUID) -> Optional[RouteResponse]:
        """Get route by ID."""
        result = await self.db.execute(
            select(Route).where(Route.id == route_id)
        )
        route = result.scalar_one_or_none()
        return RouteResponse.from_orm(route) if route else None

    async def create_route(self, route_data: RouteCreate) -> RouteResponse:
        """Create a new route."""
        # Verify that agent and feature exist
        agent_result = await self.db.execute(
            select(Agent).where(Agent.id == route_data.agent_id)
        )
        agent = agent_result.scalar_one_or_none()
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Agent not found"
            )

        feature_result = await self.db.execute(
            select(Feature).where(Feature.id == route_data.feature_id)
        )
        feature = feature_result.scalar_one_or_none()
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feature not found"
            )

        route = Route(
            feature_id=route_data.feature_id,
            agent_id=route_data.agent_id,
            rules=route_data.rules,
            conditional=route_data.conditional,
        )
        self.db.add(route)
        await self.db.commit()
        await self.db.refresh(route)
        return RouteResponse.from_orm(route)

    async def update_route(self, route_id: UUID, route_data: RouteCreate) -> Optional[RouteResponse]:
        """Update a route."""
        result = await self.db.execute(
            select(Route).where(Route.id == route_id)
        )
        route = result.scalar_one_or_none()
        if not route:
            return None

        # Verify that agent and feature exist
        agent_result = await self.db.execute(
            select(Agent).where(Agent.id == route_data.agent_id)
        )
        agent = agent_result.scalar_one_or_none()
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Agent not found"
            )

        feature_result = await self.db.execute(
            select(Feature).where(Feature.id == route_data.feature_id)
        )
        feature = feature_result.scalar_one_or_none()
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feature not found"
            )

        route.feature_id = route_data.feature_id
        route.agent_id = route_data.agent_id
        route.rules = route_data.rules
        route.conditional = route_data.conditional

        await self.db.commit()
        await self.db.refresh(route)
        return RouteResponse.from_orm(route)

    async def delete_route(self, route_id: UUID) -> bool:
        """Delete a route."""
        result = await self.db.execute(
            select(Route).where(Route.id == route_id)
        )
        route = result.scalar_one_or_none()
        if not route:
            return False

        await self.db.delete(route)
        await self.db.commit()
        return True

    async def add_condition_to_route(self, route_id: UUID, condition_data: RouteCondition) -> Optional[RouteResponse]:
        """Add a condition to a route."""
        # Get the route
        route_result = await self.db.execute(
            select(Route).where(Route.id == route_id)
        )
        route = route_result.scalar_one_or_none()
        if not route:
            return None

        # Create the condition
        condition = Condition(
            name=condition_data.name,
            description=condition_data.description,
            condition_type=condition_data.condition_type,
            condition_data=condition_data.condition_data,
        )
        self.db.add(condition)
        await self.db.commit()
        await self.db.refresh(condition)

        # Add condition to route
        route.conditions.append(condition)
        await self.db.commit()
        await self.db.refresh(route)

        return RouteResponse.from_orm(route)

    async def remove_condition_from_route(self, route_id: UUID, condition_id: UUID) -> Optional[RouteResponse]:
        """Remove a condition from a route."""
        # Get the route
        route_result = await self.db.execute(
            select(Route).where(Route.id == route_id)
        )
        route = route_result.scalar_one_or_none()
        if not route:
            return None

        # Get the condition
        condition_result = await self.db.execute(
            select(Condition).where(Condition.id == condition_id)
        )
        condition = condition_result.scalar_one_or_none()
        if not condition:
            return None

        # Remove condition from route
        if condition in route.conditions:
            route.conditions.remove(condition)
            await self.db.commit()
            await self.db.refresh(route)

        return RouteResponse.from_orm(route)
