"""Feature management API endpoints."""

import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.features import (
    FeatureCreate,
    FeatureResponse,
    FeatureListResponse,
    DiscoverFeaturesRequest,
)
from app.services.features import FeatureService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/features", tags=["Features"])


async def get_feature_service(db: AsyncSession = Depends(get_db)) -> FeatureService:
    """Get feature service."""
    return FeatureService(db)


@router.get("", response_model=FeatureListResponse)
async def list_features(
    skip: int = 0,
    limit: int = 100,
    feature_service: FeatureService = Depends(get_feature_service),
) -> FeatureListResponse:
    """List all features."""
    try:
        features = await feature_service.list_features(skip=skip, limit=limit)
        return FeatureListResponse(features=features, total=len(features))
    except Exception as e:
        logger.error(f"Error listing features: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("", response_model=FeatureResponse, status_code=status.HTTP_201_CREATED)
async def create_feature(
    feature_data: FeatureCreate,
    feature_service: FeatureService = Depends(get_feature_service),
) -> FeatureResponse:
    """Create a new feature."""
    try:
        feature = await feature_service.create_feature(feature_data)
        logger.info(f"Created feature: {feature.name}")
        return feature
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating feature: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{feature_id}", response_model=FeatureResponse)
async def get_feature(
    feature_id: UUID,
    feature_service: FeatureService = Depends(get_feature_service),
) -> FeatureResponse:
    """Get feature details."""
    try:
        feature = await feature_service.get_feature(feature_id)
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feature not found"
            )
        return feature
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting feature: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{feature_id}", response_model=FeatureResponse)
async def update_feature(
    feature_id: UUID,
    feature_data: FeatureCreate,
    feature_service: FeatureService = Depends(get_feature_service),
) -> FeatureResponse:
    """Update a feature."""
    try:
        feature = await feature_service.update_feature(feature_id, feature_data)
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feature not found"
            )
        logger.info(f"Updated feature: {feature.name}")
        return feature
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating feature: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feature(
    feature_id: UUID,
    feature_service: FeatureService = Depends(get_feature_service),
):
    """Delete a feature."""
    try:
        success = await feature_service.delete_feature(feature_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feature not found"
            )
        logger.info(f"Deleted feature: {feature_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting feature: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/discover", response_model=List[FeatureResponse])
async def discover_features(
    discovery_request: DiscoverFeaturesRequest,
    feature_service: FeatureService = Depends(get_feature_service),
) -> List[FeatureResponse]:
    """Discover features from external stores (HTTP_JSON, GIT, S3, GCS)."""
    try:
        features = await feature_service.discover_features(discovery_request)
        logger.info(f"Discovered {len(features)} features from {discovery_request.store_type}")
        return features
    except Exception as e:
        logger.error(f"Error discovering features: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during feature discovery"
        )
