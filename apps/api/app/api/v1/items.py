"""Items API routes with CRUD operations."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import check_idempotency_key, set_idempotency_key
from app.db.models import Item
from app.db.session import get_db
from app.schemas.item import (
    ItemCreate,
    ItemResponse,
    ItemUpdate,
    ItemListResponse,
)

router = APIRouter()


@router.get("/", response_model=ItemListResponse)
async def list_items(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    db: AsyncSession = Depends(get_db),
) -> ItemListResponse:
    """List items with pagination."""
    # Count total items
    count_result = await db.execute(select(func.count(Item.id)))
    total = count_result.scalar() or 0
    
    # Get items for current page
    offset = (page - 1) * size
    result = await db.execute(
        select(Item).offset(offset).limit(size).order_by(Item.created_at.desc())
    )
    items = result.scalars().all()
    
    return ItemListResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        has_next=offset + size < total,
        has_prev=page > 1,
    )


@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(
    item: ItemCreate,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    db: AsyncSession = Depends(get_db),
) -> ItemResponse:
    """Create a new item with idempotency support."""
    # Check idempotency key if provided
    if idempotency_key:
        if await check_idempotency_key(idempotency_key):
            raise HTTPException(
                status_code=409,
                detail="Item with this idempotency key already exists"
            )
        await set_idempotency_key(idempotency_key)
    
    # Create new item
    db_item = Item(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    
    return db_item


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: str,
    db: AsyncSession = Depends(get_db),
) -> ItemResponse:
    """Get item by ID."""
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: str,
    item_update: ItemUpdate,
    db: AsyncSession = Depends(get_db),
) -> ItemResponse:
    """Update item by ID."""
    result = await db.execute(select(Item).where(Item.id == item_id))
    db_item = result.scalar_one_or_none()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update only provided fields
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    await db.commit()
    await db.refresh(db_item)
    
    return db_item


@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: str,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete item by ID."""
    result = await db.execute(select(Item).where(Item.id == item_id))
    db_item = result.scalar_one_or_none()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    await db.delete(db_item)
    await db.commit()
