from fastapi import APIRouter
from datetime import datetime

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from assessment_app.models.models import (Task)
from assessment_app.repository.database import get_db
from assessment_app.repository.tasks import TaskRepository
from pydantic import BaseModel

from assessment_app.service.auth_service import get_current_user_from_request

router = APIRouter()


@router.get("/tasks", response_model=List[Task])
async def get_tasks(
        db: Session = Depends(get_db)
) -> List[Task]:
    """
    Get all tasks available.
    """
    task_repo = TaskRepository(db)
    return task_repo.get_all_tasks()


@router.post("/tasks", response_model=Task)
async def create_tasks(
        task: Task,
        db: Session = Depends(get_db)
) -> Task:
    """
    Create a new trading tasks.
    """
    tasks_repo = TaskRepository(db)
    return tasks_repo.creat e_task(task)


@router.get("/tasks_for_days", response_model=List[Task])
async def get_tasks(
        day: datetime,
        db: Session = Depends(get_db)
) -> List[Task]:
    """
    Get all tasks available.
    """
    task_repo = TaskRepository(db)
    return task_repo.tasks_for_day(day)
