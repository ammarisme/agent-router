"""Role service."""

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Role
from app.schemas.roles import (
    RoleCreate,
    RoleResponse,
    ImportIAMRolesRequest,
)

logger = logging.getLogger(__name__)


class RoleService:
    """Role service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_roles(self, skip: int = 0, limit: int = 100) -> List[RoleResponse]:
        """List all roles."""
        result = await self.db.execute(
            select(Role).offset(skip).limit(limit)
        )
        roles = result.scalars().all()
        return [RoleResponse.from_orm(role) for role in roles]

    async def get_role(self, role_id: UUID) -> Optional[RoleResponse]:
        """Get role by ID."""
        result = await self.db.execute(
            select(Role).where(Role.id == role_id)
        )
        role = result.scalar_one_or_none()
        return RoleResponse.from_orm(role) if role else None

    async def create_role(self, role_data: RoleCreate) -> RoleResponse:
        """Create a new role."""
        role = Role(
            name=role_data.name,
            description=role_data.description,
            permissions=role_data.permissions,
            config_data=role_data.config_data or {},
        )
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return RoleResponse.from_orm(role)

    async def update_role(self, role_id: UUID, role_data: RoleCreate) -> Optional[RoleResponse]:
        """Update a role."""
        result = await self.db.execute(
            select(Role).where(Role.id == role_id)
        )
        role = result.scalar_one_or_none()
        if not role:
            return None

        role.name = role_data.name
        role.description = role_data.description
        role.permissions = role_data.permissions
        role.config_data = role_data.config_data or {}

        await self.db.commit()
        await self.db.refresh(role)
        return RoleResponse.from_orm(role)

    async def delete_role(self, role_id: UUID) -> bool:
        """Delete a role."""
        result = await self.db.execute(
            select(Role).where(Role.id == role_id)
        )
        role = result.scalar_one_or_none()
        if not role:
            return False

        await self.db.delete(role)
        await self.db.commit()
        return True

    async def import_iam_roles(self, import_request: ImportIAMRolesRequest) -> List[RoleResponse]:
        """Import IAM roles from cloud providers."""
        # This is a mock implementation - in production, this would connect to
        # actual AWS IAM, Azure RBAC, or GCP IAM APIs
        logger.info(f"Importing IAM roles from {import_request.provider}")
        
        # Mock imported roles based on provider
        mock_roles = []
        if import_request.provider == "AWS":
            mock_roles = [
                Role(
                    name="AWS-AdministratorAccess",
                    description="AWS Administrator Access role",
                    permissions=["*"],
                    config_data={
                        "provider": "AWS",
                        "arn": "arn:aws:iam::123456789012:role/AdministratorAccess",
                        "trust_policy": {"Version": "2012-10-17", "Statement": []}
                    }
                ),
                Role(
                    name="AWS-ReadOnlyAccess",
                    description="AWS Read Only Access role",
                    permissions=["s3:Get*", "ec2:Describe*", "iam:Get*"],
                    config_data={
                        "provider": "AWS",
                        "arn": "arn:aws:iam::123456789012:role/ReadOnlyAccess",
                        "trust_policy": {"Version": "2012-10-17", "Statement": []}
                    }
                )
            ]
        elif import_request.provider == "AZURE":
            mock_roles = [
                Role(
                    name="Azure-Owner",
                    description="Azure Owner role",
                    permissions=["*"],
                    config_data={
                        "provider": "AZURE",
                        "role_definition_id": "8e3af657-a8ff-443c-a75c-2fe8c4bcb635",
                        "scope": "/subscriptions/12345678-1234-1234-1234-123456789012"
                    }
                )
            ]
        elif import_request.provider == "GCP":
            mock_roles = [
                Role(
                    name="GCP-Owner",
                    description="GCP Owner role",
                    permissions=["*"],
                    config_data={
                        "provider": "GCP",
                        "role_id": "roles/owner",
                        "project_id": "example-project-123"
                    }
                )
            ]

        # Save imported roles to database
        for mock_role in mock_roles:
            self.db.add(mock_role)
        
        await self.db.commit()
        
        # Refresh to get IDs
        for role in mock_roles:
            await self.db.refresh(role)
        
        return [RoleResponse.from_orm(role) for role in mock_roles]
