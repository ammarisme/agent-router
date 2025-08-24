"""API v1 router."""

from fastapi import APIRouter

from app.api.v1 import auth, agents, features, routes, roles, analytics, system

router = APIRouter()

# Include all route modules
router.include_router(auth.router)
router.include_router(agents.router)
router.include_router(features.router)
router.include_router(routes.router)
router.include_router(roles.router)
router.include_router(analytics.router)
router.include_router(system.router)
