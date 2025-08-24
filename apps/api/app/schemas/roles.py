"""Role schemas."""

from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    """Base role schema."""
    name: str = Field(..., min_length=1, max_length=255, description="Role name")
    description: Optional[str] = Field(None, description="Role description")
    permissions: List[str] = Field(default_factory=list, description="Role permissions")
    is_custom: bool = Field(True, description="Whether this is a custom role")
    source: Optional[str] = Field(None, description="Role source (AWS, AZURE, GCP, CUSTOM)")


class RoleCreate(BaseModel):
    """Role creation schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    permissions: List[str] = Field(default_factory=list)
    config_data: Optional[Dict[str, Any]] = Field(default_factory=dict)


class RoleUpdate(BaseModel):
    """Update role request schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Role name")
    description: Optional[str] = Field(None, description="Role description")
    permissions: Optional[List[str]] = Field(None, description="Role permissions")
    is_custom: Optional[bool] = Field(None, description="Whether this is a custom role")
    source: Optional[str] = Field(None, description="Role source (AWS, AZURE, GCP, CUSTOM)")


class RoleResponse(BaseModel):
    """Role response schema."""
    id: UUID
    name: str
    description: str
    permissions: List[str]
    config_data: Dict[str, Any]

    class Config:
        from_attributes = True


class RoleListResponse(BaseModel):
    """Role list response schema."""
    roles: list[RoleResponse]
    total: int


class ImportIAMRolesRequest(BaseModel):
    """Import IAM roles request schema."""
    provider: str = Field(..., pattern="^(AWS|AZURE|GCP)$")
    credentials: Optional[Dict[str, Any]] = None
    filters: Optional[Dict[str, Any]] = None


class IAMRole(BaseModel):
    """IAM role schema."""
    arn: str = Field(..., description="IAM role ARN")
    name: str = Field(..., description="IAM role name")
    description: Optional[str] = Field(None, description="IAM role description")
    permissions: List[str] = Field(default_factory=list, description="IAM role permissions")
    tags: Dict[str, str] = Field(default_factory=dict, description="IAM role tags")


class ImportIAMRolesResponse(BaseModel):
    """Import IAM roles response schema."""
    imported_roles: List[RoleResponse] = Field(..., description="Successfully imported roles")
    failed_roles: List[Dict[str, Any]] = Field(..., description="Failed role imports")
    total_imported: int = Field(..., description="Total number of imported roles")
    total_failed: int = Field(..., description="Total number of failed imports")


class DiscoverIAMRolesRequest(BaseModel):
    """Discover IAM roles request schema."""
    provider: str = Field(..., description="Cloud provider (AWS, AZURE, GCP)")
    region: str = Field(..., description="Cloud region")
    access_key: str = Field(..., description="Access key ID")
    secret_key: str = Field(..., description="Secret access key")


class DiscoverIAMRolesResponse(BaseModel):
    """Discover IAM roles response schema."""
    roles: List[IAMRole] = Field(..., description="List of discovered IAM roles")
    total: int = Field(..., description="Total number of discovered roles")


class AssignUsersToRoleRequest(BaseModel):
    """Assign users to role request schema."""
    user_ids: List[UUID] = Field(..., description="List of user IDs to assign")


class AssignUsersToRoleResponse(BaseModel):
    """Assign users to role response schema."""
    assigned_users: List[UUID] = Field(..., description="Successfully assigned user IDs")
    failed_users: List[Dict[str, Any]] = Field(..., description="Failed user assignments")
    total_assigned: int = Field(..., description="Total number of assigned users")
    total_failed: int = Field(..., description="Total number of failed assignments")


class Permission(BaseModel):
    """Permission schema."""
    name: str = Field(..., description="Permission name")
    description: Optional[str] = Field(None, description="Permission description")
    category: str = Field(..., description="Permission category")
    resource: str = Field(..., description="Permission resource")


class PermissionListResponse(BaseModel):
    """Permission list response schema."""
    permissions: List[Permission] = Field(..., description="List of permissions")
    categories: List[str] = Field(..., description="Available permission categories")
    total: int = Field(..., description="Total number of permissions")
