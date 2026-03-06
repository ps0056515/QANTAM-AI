"""
Tenant Middleware - Multi-tenant isolation
"""
from uuid import UUID
from fastapi import Request


class TenantMiddleware:
    """Middleware for tenant isolation."""

    async def __call__(self, request: Request, call_next):
        request.state.tenant_id = None
        response = await call_next(request)
        return response


def get_tenant_id(request: Request) -> UUID:
    """Get tenant ID from request state."""
    tenant_id = getattr(request.state, 'tenant_id', None)
    if not tenant_id:
        raise ValueError("Tenant ID not found in request")
    return tenant_id
