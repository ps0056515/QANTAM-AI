"""
Health Router - System health checks
"""
from fastapi import APIRouter
from db.postgres import engine
from db.neo4j import neo4j_driver

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check."""
    return {"status": "healthy", "service": "qantam-api"}


@router.get("/health/detailed")
async def detailed_health():
    """Detailed health check with dependency status."""
    checks = {
        "api": "healthy",
        "postgres": "unknown",
        "neo4j": "unknown",
        "redis": "unknown"
    }
    
    # PostgreSQL
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        checks["postgres"] = "healthy"
    except Exception as e:
        checks["postgres"] = f"unhealthy: {str(e)}"
    
    # Neo4j
    try:
        with neo4j_driver.session() as session:
            session.run("RETURN 1")
        checks["neo4j"] = "healthy"
    except Exception as e:
        checks["neo4j"] = f"unhealthy: {str(e)}"
    
    all_healthy = all(v == "healthy" for v in checks.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "checks": checks
    }
