"""
Neo4j Connection - QKG database connection management
"""
import os
from contextlib import asynccontextmanager
from neo4j import AsyncGraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "qantam123")

_driver = None


def get_driver():
    """Get or create Neo4j driver."""
    global _driver
    if _driver is None:
        _driver = AsyncGraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )
    return _driver


def close_driver():
    """Close Neo4j driver."""
    global _driver
    if _driver:
        _driver.close()
        _driver = None


@asynccontextmanager
async def get_neo4j_session():
    """Get Neo4j session as async context manager."""
    driver = get_driver()
    session = driver.session()
    try:
        yield session
    finally:
        await session.close()


neo4j_driver = get_driver()
