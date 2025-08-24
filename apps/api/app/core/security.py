"""Security utilities for authentication and authorization."""

from datetime import datetime, timedelta
from typing import Optional

from argon2 import PasswordHasher
from jose import JWTError, jwt

from app.config import settings

# Password hasher
ph = PasswordHasher()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_min)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_alg)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
        return payload
    except JWTError:
        return None


def hash_password(password: str) -> str:
    """Hash password using Argon2."""
    return ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    try:
        ph.verify(hashed, password)
        return True
    except Exception:
        return False
