"""Application configuration."""

import json
import os
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = Field("Agent Router API", description="Application name")
    version: str = Field("0.1.0", description="Application version")
    debug: bool = Field(False, description="Debug mode")
    log_level: str = Field("INFO", description="Log level")
    enable_docs: bool = Field(True, description="Enable API documentation")

    # Database
    database_url: str = Field(
        "sqlite+aiosqlite:///./data/app.db",
        description="Database connection URL"
    )

    # Redis
    redis_url: str = Field(
        "redis://localhost:6379/0",
        description="Redis connection URL"
    )

    # JWT Authentication
    jwt_secret_key: str = Field(
        "your-secret-key-change-in-production",
        description="JWT secret key"
    )
    jwt_algorithm: str = Field("HS256", description="JWT algorithm")
    jwt_access_token_expire_minutes: int = Field(30, description="JWT access token expiration")
    jwt_refresh_token_expire_days: int = Field(7, description="JWT refresh token expiration")

    # CORS
    cors_origins: List[str] = Field(
        ["http://localhost:3000", "http://localhost:3001"],
        description="CORS allowed origins"
    )

    # Rate Limiting
    rate_limit_requests: int = Field(100, description="Rate limit requests per minute")
    rate_limit_window: int = Field(60, description="Rate limit window in seconds")

    # Security
    security_headers: bool = Field(True, description="Enable security headers")
    security_headers_enabled: bool = Field(True, description="Enable security headers")
    trusted_hosts: List[str] = Field(["localhost", "127.0.0.1"], description="Trusted hosts")
    allowed_hosts: List[str] = Field(["localhost", "127.0.0.1", "*"], description="Allowed hosts for TrustedHostMiddleware")
    csp_default_src: str = Field("'self'", description="Content Security Policy default source")
    hsts_max_age: int = Field(31536000, description="HSTS max age in seconds (1 year)")

    # File Upload
    max_file_size: int = Field(10 * 1024 * 1024, description="Maximum file size in bytes")
    allowed_file_types: List[str] = Field(
        [".json", ".yaml", ".yml", ".txt"],
        description="Allowed file types"
    )

    # OpenTelemetry
    otel_endpoint: Optional[str] = Field(None, description="OpenTelemetry endpoint")
    otel_service_name: str = Field("agent-router-api", description="OpenTelemetry service name")

    # Monitoring
    prometheus_enabled: bool = Field(True, description="Enable Prometheus metrics")
    health_check_interval: int = Field(60, description="Health check interval in seconds")

    # Agent Discovery
    agent_discovery_timeout: int = Field(30, description="Agent discovery timeout in seconds")
    agent_health_check_interval: int = Field(300, description="Agent health check interval in seconds")

    # Feature Store
    feature_discovery_timeout: int = Field(30, description="Feature discovery timeout in seconds")
    feature_cache_ttl: int = Field(3600, description="Feature cache TTL in seconds")

    # IAM Integration
    iam_discovery_timeout: int = Field(30, description="IAM discovery timeout in seconds")
    iam_role_cache_ttl: int = Field(3600, description="IAM role cache TTL in seconds")

    # Backup & Recovery
    backup_enabled: bool = Field(True, description="Enable backup functionality")
    backup_retention_days: int = Field(30, description="Backup retention in days")
    backup_schedule: str = Field("0 2 * * *", description="Backup schedule (cron format)")

    # Litestream (for SQLite backup)
    litestream_enabled: bool = Field(False, description="Enable Litestream for SQLite backup")
    litestream_bucket: Optional[str] = Field(None, description="Litestream S3 bucket")
    litestream_path: Optional[str] = Field(None, description="Litestream S3 path")

    @field_validator("cors_origins", mode="before")
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return json.loads(v)
        return v

    @field_validator("trusted_hosts", mode="before")
    def parse_trusted_hosts(cls, v):
        """Parse trusted hosts from string or list."""
        if isinstance(v, str):
            return json.loads(v)
        return v

    @field_validator("allowed_hosts", mode="before")
    def parse_allowed_hosts(cls, v):
        """Parse allowed hosts from string or list."""
        if isinstance(v, str):
            return json.loads(v)
        return v

    @field_validator("allowed_file_types", mode="before")
    def parse_allowed_file_types(cls, v):
        """Parse allowed file types from string or list."""
        if isinstance(v, str):
            return json.loads(v)
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return not self.debug

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.debug

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables


# Global settings instance
settings = Settings()
