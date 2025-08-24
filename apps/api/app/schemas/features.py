"""Feature schemas."""

from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class FeatureBase(BaseModel):
    """Base feature schema."""
    name: str = Field(..., min_length=1, max_length=255, description="Feature name")
    description: Optional[str] = Field(None, description="Feature description")
    store_type: str = Field(..., description="Feature store type (HTTP_JSON, GIT, S3, GCS)")
    url: HttpUrl = Field(..., description="Feature store URL")
    token: Optional[str] = Field(None, description="Authentication token")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class FeatureCreate(BaseModel):
    """Feature creation schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    store_type: str = Field(..., pattern="^(HTTP_JSON|GIT|S3|GCS)$")
    url: str = Field(..., min_length=1, max_length=500)
    token: str = Field(..., min_length=1, max_length=500)
    config_data: Optional[Dict[str, Any]] = Field(default_factory=dict)


class FeatureUpdate(BaseModel):
    """Update feature request schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Feature name")
    description: Optional[str] = Field(None, description="Feature description")
    store_type: Optional[str] = Field(None, description="Feature store type (HTTP_JSON, GIT, S3, GCS)")
    url: Optional[HttpUrl] = Field(None, description="Feature store URL")
    token: Optional[str] = Field(None, description="Authentication token")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class FeatureResponse(BaseModel):
    """Feature response schema."""
    id: UUID
    name: str
    description: str
    store_type: str
    url: str
    token: str
    status: str
    config_data: Dict[str, Any]

    class Config:
        from_attributes = True


class FeatureListResponse(BaseModel):
    """Feature list response schema."""
    features: List[FeatureResponse] = Field(..., description="List of features")
    total: int = Field(..., description="Total number of features")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")


class DiscoverFeaturesRequest(BaseModel):
    """Feature discovery request schema."""
    store_type: str = Field(..., pattern="^(HTTP_JSON|GIT|S3|GCS)$")
    url: Optional[str] = None
    credentials: Optional[Dict[str, Any]] = None


class DiscoveredFeature(BaseModel):
    """Discovered feature schema."""
    name: str = Field(..., description="Feature name")
    description: Optional[str] = Field(None, description="Feature description")
    version: Optional[str] = Field(None, description="Feature version")
    dependencies: List[str] = Field(default_factory=list, description="Feature dependencies")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class DiscoverFeaturesResponse(BaseModel):
    """Discover features response schema."""
    features: List[DiscoveredFeature] = Field(..., description="List of discovered features")
    total: int = Field(..., description="Total number of discovered features")


class TestFeatureConnectionRequest(BaseModel):
    """Test feature connection request schema."""
    store_type: str = Field(..., description="Feature store type (HTTP_JSON, GIT, S3, GCS)")
    url: HttpUrl = Field(..., description="Feature store URL")
    token: Optional[str] = Field(None, description="Authentication token")


class TestFeatureConnectionResponse(BaseModel):
    """Test feature connection response schema."""
    success: bool = Field(..., description="Connection test result")
    message: str = Field(..., description="Connection test message")
    response_time: Optional[float] = Field(None, description="Response time in milliseconds")
    details: Dict[str, Any] = Field(default_factory=dict, description="Connection test details")
