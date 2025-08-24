"""System service."""

import logging
import os
import psutil
from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.schemas.system import (
    SystemHealth,
    SystemConfig,
    SystemLogs,
    ActivityLogs,
)

logger = logging.getLogger(__name__)


class SystemService:
    """System service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_system_health(self) -> SystemHealth:
        """Get system health check."""
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Check database connectivity
        try:
            await self.db.execute("SELECT 1")
            db_status = "healthy"
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            db_status = "unhealthy"
        
        # Check Redis connectivity (if enabled)
        redis_status = "healthy"
        if settings.redis_enabled:
            try:
                # This would be an actual Redis check in production
                redis_status = "healthy"
            except Exception as e:
                logger.error(f"Redis health check failed: {e}")
                redis_status = "unhealthy"
        
        return SystemHealth(
            status="healthy" if all(s == "healthy" for s in [db_status, redis_status]) else "unhealthy",
            timestamp=datetime.now(),
            uptime=self._get_uptime(),
            cpu_usage=cpu_percent,
            memory_usage=memory.percent,
            disk_usage=disk.percent,
            database_status=db_status,
            redis_status=redis_status,
            version="1.0.0"
        )

    async def get_system_config(self) -> SystemConfig:
        """Get system configuration."""
        return SystemConfig(
            app_name=settings.app_name,
            app_version="1.0.0",
            environment=settings.app_env,
            debug=settings.debug,
            database_url=settings.database_url.split('@')[0] + '@***' if '@' in settings.database_url else '***',
            redis_enabled=settings.redis_enabled,
            redis_url=settings.redis_url.split('@')[0] + '@***' if '@' in settings.redis_url else '***',
            cors_origins=settings.cors_origins,
            rate_limit_enabled=settings.rate_limit_enabled,
            max_requests_per_minute=settings.max_requests_per_minute,
            security_headers_enabled=settings.security_headers_enabled,
            allowed_hosts=settings.allowed_hosts,
            file_upload_enabled=settings.file_upload_enabled,
            max_file_size=settings.max_file_size,
            allowed_file_types=settings.allowed_file_types,
            opentelemetry_enabled=settings.opentelemetry_enabled,
            prometheus_enabled=settings.prometheus_enabled
        )

    async def get_system_logs(self, level: str = "INFO", limit: int = 100) -> SystemLogs:
        """Get system logs."""
        # Mock implementation - in production, this would read from actual log files
        mock_logs = [
            {
                "timestamp": "2024-01-01T12:00:00Z",
                "level": "INFO",
                "message": "Application started successfully",
                "module": "app.main"
            },
            {
                "timestamp": "2024-01-01T12:01:00Z",
                "level": "INFO",
                "message": "Database connection established",
                "module": "app.db.session"
            },
            {
                "timestamp": "2024-01-01T12:02:00Z",
                "level": "WARNING",
                "message": "Redis connection failed, continuing without cache",
                "module": "app.core.redis"
            },
            {
                "timestamp": "2024-01-01T12:03:00Z",
                "level": "INFO",
                "message": "API server listening on port 8000",
                "module": "app.main"
            }
        ]
        
        # Filter by level
        filtered_logs = [log for log in mock_logs if log["level"] == level]
        
        return SystemLogs(
            logs=filtered_logs[:limit],
            total=len(filtered_logs),
            level=level,
            limit=limit
        )

    async def get_activity_logs(self, limit: int = 100) -> ActivityLogs:
        """Get activity logs."""
        # Mock implementation - in production, this would query actual activity logs
        mock_activities = [
            {
                "timestamp": "2024-01-01T12:00:00Z",
                "user_id": "user-1",
                "action": "LOGIN",
                "resource": "auth",
                "details": "User logged in successfully"
            },
            {
                "timestamp": "2024-01-01T12:01:00Z",
                "user_id": "user-1",
                "action": "CREATE",
                "resource": "agent",
                "details": "Created new agent: MCP Agent 1"
            },
            {
                "timestamp": "2024-01-01T12:02:00Z",
                "user_id": "user-1",
                "action": "CREATE",
                "resource": "feature",
                "details": "Created new feature: API Feature 1"
            },
            {
                "timestamp": "2024-01-01T12:03:00Z",
                "user_id": "user-1",
                "action": "CREATE",
                "resource": "route",
                "details": "Created route between feature and agent"
            }
        ]
        
        return ActivityLogs(
            activities=mock_activities[:limit],
            total=len(mock_activities),
            limit=limit
        )

    def _get_uptime(self) -> str:
        """Get system uptime."""
        try:
            uptime_seconds = psutil.boot_time()
            uptime = datetime.now() - datetime.fromtimestamp(uptime_seconds)
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{days}d {hours}h {minutes}m {seconds}s"
        except Exception:
            return "Unknown"
