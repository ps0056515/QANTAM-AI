"""
RBAC Middleware - Role-based access control
"""
from functools import wraps
from typing import List

from fastapi import HTTPException, Depends

from middleware.auth import get_current_user, CurrentUser


ROLE_PERMISSIONS = {
    "admin": [
        "clarity:read", "clarity:write", "clarity:delete",
        "pulse:read", "pulse:write", "pulse:delete",
        "signal:read", "signal:write",
        "forge:read", "forge:write",
        "users:read", "users:write", "users:delete",
        "projects:read", "projects:write", "projects:delete",
        "settings:read", "settings:write"
    ],
    "release_manager": [
        "clarity:read", "clarity:write",
        "pulse:read", "pulse:write",
        "signal:read", "signal:write",
        "forge:read",
        "projects:read"
    ],
    "qa_lead": [
        "clarity:read", "clarity:write",
        "pulse:read", "pulse:write",
        "signal:read",
        "forge:read",
        "projects:read"
    ],
    "qa_engineer": [
        "clarity:read", "clarity:write",
        "pulse:read", "pulse:write",
        "forge:read",
        "projects:read"
    ]
}


def has_permission(role: str, permission: str) -> bool:
    """Check if role has specific permission."""
    permissions = ROLE_PERMISSIONS.get(role, [])
    return permission in permissions


def require_permission(permission: str):
    """Decorator to require specific permission."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user: CurrentUser = Depends(get_current_user), **kwargs):
            if not has_permission(user.role, permission):
                raise HTTPException(
                    status_code=403,
                    detail=f"Permission denied: {permission} required"
                )
            return await func(*args, user=user, **kwargs)
        return wrapper
    return decorator


def require_roles(roles: List[str]):
    """Decorator to require one of specified roles."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user: CurrentUser = Depends(get_current_user), **kwargs):
            if user.role not in roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Role required: one of {roles}"
                )
            return await func(*args, user=user, **kwargs)
        return wrapper
    return decorator


class RBACChecker:
    """Dependency for checking permissions in route handlers."""

    def __init__(self, permission: str):
        self.permission = permission

    async def __call__(self, user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not has_permission(user.role, self.permission):
            raise HTTPException(
                status_code=403,
                detail=f"Permission denied: {self.permission} required"
            )
        return user
