"""Main FastAPI application."""

import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, ORJSONResponse
from fastapi_limiter import FastAPILimiter
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1 import router as v1_router
from app.config import settings
from app.core.middleware import setup_middleware
from app.core.redis import init_redis, close_redis
from app.db.session import configure_database, close_db, init_db


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting up application...")
    
    # Initialize database
    await configure_database()
    await init_db()
    
    # Initialize Redis
    await init_redis()
    # Initialize rate limiter (only if Redis is available)
    from app.core.redis import get_redis
    redis_client = await get_redis()
    if redis_client:
        try:
            await FastAPILimiter.init(redis_client)
        except Exception as e:
            logger.warning(f"Rate limiter initialization failed: {e}")
    else:
        logger.warning("Rate limiter disabled - Redis not available")
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    await close_redis()
    await close_db()
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="High-performance FastAPI backend for Agent Router",
    version="0.1.0",
    docs_url="/docs" if settings.enable_docs else None,
    redoc_url="/redoc" if settings.enable_docs else None,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

# Setup middleware
setup_middleware(app)

# Setup Prometheus metrics
Instrumentator().instrument(app).expose(app, include_in_schema=False)

# Include API routes
app.include_router(v1_router, prefix="/v1")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "correlation_id": correlation_id,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions."""
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "correlation_id": correlation_id,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "correlation_id": correlation_id,
        },
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Agent Router API",
        "version": "0.1.0",
        "docs": "/docs" if settings.enable_docs else None,
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    # This is handled by the Instrumentator
    pass
