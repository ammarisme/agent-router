"""Feature service."""

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Feature
from app.schemas.features import (
    FeatureCreate,
    FeatureResponse,
    DiscoverFeaturesRequest,
)

logger = logging.getLogger(__name__)


class FeatureService:
    """Feature service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_features(self, skip: int = 0, limit: int = 100) -> List[FeatureResponse]:
        """List all features."""
        result = await self.db.execute(
            select(Feature).offset(skip).limit(limit)
        )
        features = result.scalars().all()
        return [FeatureResponse.from_orm(feature) for feature in features]

    async def get_feature(self, feature_id: UUID) -> Optional[FeatureResponse]:
        """Get feature by ID."""
        result = await self.db.execute(
            select(Feature).where(Feature.id == feature_id)
        )
        feature = result.scalar_one_or_none()
        return FeatureResponse.from_orm(feature) if feature else None

    async def create_feature(self, feature_data: FeatureCreate) -> FeatureResponse:
        """Create a new feature."""
        feature = Feature(
            name=feature_data.name,
            description=feature_data.description,
            store_type=feature_data.store_type,
            url=feature_data.url,
            token=feature_data.token,
            config_data=feature_data.config_data or {},
        )
        self.db.add(feature)
        await self.db.commit()
        await self.db.refresh(feature)
        return FeatureResponse.from_orm(feature)

    async def update_feature(self, feature_id: UUID, feature_data: FeatureCreate) -> Optional[FeatureResponse]:
        """Update a feature."""
        result = await self.db.execute(
            select(Feature).where(Feature.id == feature_id)
        )
        feature = result.scalar_one_or_none()
        if not feature:
            return None

        feature.name = feature_data.name
        feature.description = feature_data.description
        feature.store_type = feature_data.store_type
        feature.url = feature_data.url
        feature.token = feature_data.token
        feature.config_data = feature_data.config_data or {}

        await self.db.commit()
        await self.db.refresh(feature)
        return FeatureResponse.from_orm(feature)

    async def delete_feature(self, feature_id: UUID) -> bool:
        """Delete a feature."""
        result = await self.db.execute(
            select(Feature).where(Feature.id == feature_id)
        )
        feature = result.scalar_one_or_none()
        if not feature:
            return False

        await self.db.delete(feature)
        await self.db.commit()
        return True

    async def discover_features(self, discovery_request: DiscoverFeaturesRequest) -> List[FeatureResponse]:
        """Discover features from external stores."""
        # This is a mock implementation - in production, this would connect to
        # actual HTTP_JSON endpoints, Git repositories, S3 buckets, or GCS buckets
        logger.info(f"Discovering features from {discovery_request.store_type}")
        
        # Mock discovered features based on store type
        mock_features = []
        if discovery_request.store_type == "HTTP_JSON":
            mock_features = [
                Feature(
                    name="API Feature 1",
                    description="Mock HTTP JSON feature",
                    store_type="HTTP_JSON",
                    url="https://api.example.com/features/1",
                    token="mock-api-token",
                    config_data={"endpoint": "/api/v1/features", "method": "GET"}
                ),
                Feature(
                    name="API Feature 2",
                    description="Another mock HTTP JSON feature",
                    store_type="HTTP_JSON",
                    url="https://api.example.com/features/2",
                    token="mock-api-token-2",
                    config_data={"endpoint": "/api/v1/features", "method": "POST"}
                )
            ]
        elif discovery_request.store_type == "GIT":
            mock_features = [
                Feature(
                    name="Git Feature 1",
                    description="Mock Git repository feature",
                    store_type="GIT",
                    url="https://github.com/example/feature-repo",
                    token="mock-git-token",
                    config_data={"branch": "main", "path": "features/"}
                )
            ]
        elif discovery_request.store_type == "S3":
            mock_features = [
                Feature(
                    name="S3 Feature 1",
                    description="Mock S3 bucket feature",
                    store_type="S3",
                    url="s3://example-bucket/features/",
                    token="mock-s3-token",
                    config_data={"bucket": "example-bucket", "prefix": "features/"}
                )
            ]
        elif discovery_request.store_type == "GCS":
            mock_features = [
                Feature(
                    name="GCS Feature 1",
                    description="Mock GCS bucket feature",
                    store_type="GCS",
                    url="gs://example-bucket/features/",
                    token="mock-gcs-token",
                    config_data={"bucket": "example-bucket", "prefix": "features/"}
                )
            ]

        # Save discovered features to database
        for mock_feature in mock_features:
            self.db.add(mock_feature)
        
        await self.db.commit()
        
        # Refresh to get IDs
        for feature in mock_features:
            await self.db.refresh(feature)
        
        return [FeatureResponse.from_orm(feature) for feature in mock_features]
