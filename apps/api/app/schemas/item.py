"""Pydantic schemas for Item model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Base Item schema with common fields."""

    title: str = Field(..., min_length=1, max_length=255, description="Item title")
    description: Optional[str] = Field(None, max_length=1000, description="Item description")


class ItemCreate(ItemBase):
    """Schema for creating a new item."""

    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class ItemResponse(ItemBase):
    """Schema for item response."""

    id: str = Field(..., description="Item unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class ItemListResponse(BaseModel):
    """Schema for paginated item list response."""

    items: list[ItemResponse] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")
