"""
Tasks Router - Async Job Status
"""
from uuid import UUID
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class TaskStatus(BaseModel):
    status: str
    progress: int
    result_id: Optional[UUID] = None


@router.get("/{task_id}/status", response_model=TaskStatus)
async def get_task_status(task_id: UUID):
    """Poll task status."""
    return TaskStatus(status="pending", progress=0)


@router.post("/{task_id}/cancel")
async def cancel_task(task_id: UUID):
    """Cancel a running task."""
    return {"status": "cancelled"}
