"""System schemas."""

from datetime import datetime
from typing import Dict, Any, List

from pydantic import BaseModel


class SystemHealth(BaseModel):
    """System health schema."""
    status: str
    timestamp: datetime
    uptime: str
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    database_status: str
    redis_status: str
    version: str


class SystemConfig(BaseModel):
    """System configuration schema."""
    app_name: str
    app_version: str
    environment: str
    debug: bool
    database_url: str
    redis_enabled: bool
    redis_url: str
    cors_origins: List[str]
    rate_limit_enabled: bool
    max_requests_per_minute: int
    security_headers_enabled: bool
    allowed_hosts: List[str]
    file_upload_enabled: bool
    max_file_size: int
    allowed_file_types: List[str]
    opentelemetry_enabled: bool
    prometheus_enabled: bool


class SystemLogs(BaseModel):
    """System logs schema."""
    logs: List[Dict[str, Any]]
    total: int
    level: str
    limit: int


class ActivityLogs(BaseModel):
    """Activity logs schema."""
    activities: List[Dict[str, Any]]
    total: int
    limit: int
