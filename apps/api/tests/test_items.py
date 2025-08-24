"""Tests for items API endpoints."""

import pytest
from httpx import AsyncClient

from app.schemas.item import ItemCreate


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    """Test creating a new item."""
    item_data = {
        "title": "Test Item",
        "description": "Test description"
    }
    
    response = await client.post("/v1/items/", json=item_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_get_item(client: AsyncClient):
    """Test getting an item by ID."""
    # First create an item
    item_data = {"title": "Test Item", "description": "Test description"}
    create_response = await client.post("/v1/items/", json=item_data)
    created_item = create_response.json()
    
    # Then get the item
    response = await client.get(f"/v1/items/{created_item['id']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == created_item["id"]
    assert data["title"] == item_data["title"]


@pytest.mark.asyncio
async def test_get_item_not_found(client: AsyncClient):
    """Test getting a non-existent item."""
    response = await client.get("/v1/items/non-existent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_items(client: AsyncClient):
    """Test listing items with pagination."""
    # Create some test items
    for i in range(3):
        item_data = {"title": f"Item {i}", "description": f"Description {i}"}
        await client.post("/v1/items/", json=item_data)
    
    response = await client.get("/v1/items/")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "has_next" in data
    assert "has_prev" in data


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient):
    """Test updating an item."""
    # First create an item
    item_data = {"title": "Original Title", "description": "Original description"}
    create_response = await client.post("/v1/items/", json=item_data)
    created_item = create_response.json()
    
    # Update the item
    update_data = {"title": "Updated Title"}
    response = await client.put(f"/v1/items/{created_item['id']}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == item_data["description"]  # Should remain unchanged


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient):
    """Test deleting an item."""
    # First create an item
    item_data = {"title": "Item to Delete", "description": "Will be deleted"}
    create_response = await client.post("/v1/items/", json=item_data)
    created_item = create_response.json()
    
    # Delete the item
    response = await client.delete(f"/v1/items/{created_item['id']}")
    assert response.status_code == 204
    
    # Verify item is deleted
    get_response = await client.get(f"/v1/items/{created_item['id']}")
    assert get_response.status_code == 404
