"""Role management API endpoints."""

import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.roles import (
    RoleCreate,
    RoleResponse,
    RoleListResponse,
    ImportIAMRolesRequest,
)
from app.services.roles import RoleService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/roles", tags=["Roles"])


async def get_role_service(db: AsyncSession = Depends(get_db)) -> RoleService:
    """Get role service."""
    return RoleService(db)


@router.get("", response_model=RoleListResponse)
async def list_roles(
    skip: int = 0,
    limit: int = 100,
    role_service: RoleService = Depends(get_role_service),
) -> RoleListResponse:
    """List all roles."""
    try:
        roles = await role_service.list_roles(skip=skip, limit=limit)
        return RoleListResponse(roles=roles, total=len(roles))
    except Exception as e:
        logger.error(f"Error listing roles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    role_service: RoleService = Depends(get_role_service),
) -> RoleResponse:
    """Create a new role."""
    try:
        role = await role_service.create_role(role_data)
        logger.info(f"Created role: {role.name}")
        return role
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
) -> RoleResponse:
    """Get role details."""
    try:
        role = await role_service.get_role(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        return role
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: UUID,
    role_data: RoleCreate,
    role_service: RoleService = Depends(get_role_service),
) -> RoleResponse:
    """Update a role."""
    try:
        role = await role_service.update_role(role_id, role_data)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        logger.info(f"Updated role: {role.name}")
        return role
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
):
    """Delete a role."""
    try:
        success = await role_service.delete_role(role_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        logger.info(f"Deleted role: {role_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/import-iam", response_model=List[RoleResponse])
async def import_iam_roles(
    import_request: ImportIAMRolesRequest,
    role_service: RoleService = Depends(get_role_service),
) -> List[RoleResponse]:
    """Import IAM roles from cloud providers (AWS/Azure/GCP)."""
    try:
        roles = await role_service.import_iam_roles(import_request)
        logger.info(f"Imported {len(roles)} IAM roles from {import_request.provider}")
        return roles
    except Exception as e:
        logger.error(f"Error importing IAM roles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during IAM role import"
        )
