"""Route management API endpoints."""

import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.routes import (
    RouteCreate,
    RouteResponse,
    RouteListResponse,
    RouteCondition,
)
from app.services.routes import RouteService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/routes", tags=["Routes"])


async def get_route_service(db: AsyncSession = Depends(get_db)) -> RouteService:
    """Get route service."""
    return RouteService(db)


@router.get("", response_model=RouteListResponse)
async def list_routes(
    skip: int = 0,
    limit: int = 100,
    page: int = None,
    size: int = None,
    route_service: RouteService = Depends(get_route_service),
) -> RouteListResponse:
    """List all routes with pagination support for both skip/limit and page/size formats."""
    # Support both pagination formats
    if page is not None and size is not None:
        skip = (page - 1) * size
        limit = size
    """List all routes."""
    try:
        routes = await route_service.list_routes(skip=skip, limit=limit)
        return RouteListResponse(routes=routes, total=len(routes))
    except Exception as e:
        logger.error(f"Error listing routes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
async def create_route(
    route_data: RouteCreate,
    route_service: RouteService = Depends(get_route_service),
) -> RouteResponse:
    """Create a new route."""
    try:
        route = await route_service.create_route(route_data)
        logger.info(f"Created route: {route.id}")
        return route
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(
    route_id: UUID,
    route_service: RouteService = Depends(get_route_service),
) -> RouteResponse:
    """Get route details."""
    try:
        route = await route_service.get_route(route_id)
        if not route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Route not found"
            )
        return route
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{route_id}", response_model=RouteResponse)
async def update_route(
    route_id: UUID,
    route_data: RouteCreate,
    route_service: RouteService = Depends(get_route_service),
) -> RouteResponse:
    """Update a route."""
    try:
        route = await route_service.update_route(route_id, route_data)
        if not route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Route not found"
            )
        logger.info(f"Updated route: {route.id}")
        return route
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(
    route_id: UUID,
    route_service: RouteService = Depends(get_route_service),
):
    """Delete a route."""
    try:
        success = await route_service.delete_route(route_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Route not found"
            )
        logger.info(f"Deleted route: {route_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/{route_id}/conditions", response_model=RouteResponse)
async def add_condition_to_route(
    route_id: UUID,
    condition_data: RouteCondition,
    route_service: RouteService = Depends(get_route_service),
) -> RouteResponse:
    """Add a condition to a route."""
    try:
        route = await route_service.add_condition_to_route(route_id, condition_data)
        if not route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Route not found"
            )
        logger.info(f"Added condition to route: {route_id}")
        return route
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding condition to route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{route_id}/conditions/{condition_id}", response_model=RouteResponse)
async def remove_condition_from_route(
    route_id: UUID,
    condition_id: UUID,
    route_service: RouteService = Depends(get_route_service),
) -> RouteResponse:
    """Remove a condition from a route."""
    try:
        route = await route_service.remove_condition_from_route(route_id, condition_id)
        if not route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Route or condition not found"
            )
        logger.info(f"Removed condition from route: {route_id}")
        return route
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing condition from route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
