"""
Authentication Middleware - JWT verification and user extraction
"""
import os
from uuid import UUID
from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "24"))

security = HTTPBearer(auto_error=False)


@dataclass
class CurrentUser:
    id: UUID
    tenant_id: UUID
    email: str
    name: str
    role: str


class AuthMiddleware:
    """Middleware for JWT authentication."""

    async def __call__(self, request: Request, call_next):
        # Skip auth for health checks and public endpoints
        if request.url.path in ["/health", "/health/detailed", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        # Webhooks use different auth (signature verification)
        if "/webhook/" in request.url.path:
            return await call_next(request)
        
        return await call_next(request)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=JWT_EXPIRY_HOURS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """Extract current user from JWT token."""
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        return CurrentUser(
            id=UUID(payload["sub"]),
            tenant_id=UUID(payload["tenant_id"]),
            email=payload["email"],
            name=payload.get("name", ""),
            role=payload["role"]
        )
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=401, detail="Invalid token payload")


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[CurrentUser]:
    """Extract current user if token present, otherwise None."""
    if not credentials:
        return None
    
    payload = verify_token(credentials.credentials)
    if not payload:
        return None
    
    try:
        return CurrentUser(
            id=UUID(payload["sub"]),
            tenant_id=UUID(payload["tenant_id"]),
            email=payload["email"],
            name=payload.get("name", ""),
            role=payload["role"]
        )
    except (KeyError, ValueError):
        return None
