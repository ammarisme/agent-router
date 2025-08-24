"""Redis client configuration."""

import json
from typing import Any, Optional

import redis.asyncio as redis
from fastapi import HTTPException

from app.config import settings

# Global Redis client
redis_client: Optional[redis.Redis] = None


async def init_redis() -> None:
    """Initialize Redis connection."""
    global redis_client
    try:
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        await redis_client.ping()
        print("✅ Redis connected successfully")
    except Exception as e:
        print(f"⚠️  Redis connection failed: {e}")
        print("⚠️  Running without Redis (caching and rate limiting disabled)")
        redis_client = None


async def close_redis() -> None:
    """Close Redis connection."""
    global redis_client
    if redis_client:
        await redis_client.close()


async def get_redis() -> Optional[redis.Redis]:
    """Get Redis client instance."""
    return redis_client


async def cache_get(key: str) -> Optional[Any]:
    """Get value from cache."""
    client = await get_redis()
    if not client:
        return None
    value = await client.get(key)
    if value:
        return json.loads(value)
    return None


async def cache_set(key: str, value: Any, expire: int = 3600) -> None:
    """Set value in cache with expiration."""
    client = await get_redis()
    if client:
        await client.setex(key, expire, json.dumps(value))


async def cache_delete(key: str) -> None:
    """Delete value from cache."""
    client = await get_redis()
    if client:
        await client.delete(key)


async def check_idempotency_key(key: str) -> bool:
    """Check if idempotency key exists."""
    client = await get_redis()
    if not client:
        return False
    return await client.exists(f"idempotency:{key}") > 0


async def set_idempotency_key(key: str, expire: int = 3600) -> None:
    """Set idempotency key."""
    client = await get_redis()
    if client:
        await client.setex(f"idempotency:{key}", expire, "1")
