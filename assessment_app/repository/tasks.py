import uuid
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from assessment_app.models.models import Task as PydanticTask
from assessment_app.models.db_models import Task as DBTask


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, task_id: str) -> PydanticTask:
        db_task = self.db.query(DBTask).filter(DBTask.id == task_id).first()
        return PydanticTask(
            id=db_task.id,
        )

    def get_all_tasks(self) -> List[PydanticTask]:
        db_task = self.db.query(DBTask).all()
        return [
            PydanticTask(
                id=task.id,
                name=task.name,
                group_id=task.group_id,
                start_date=task.start_date,
                end_date=task.end_date,
                estimated_effort=task.estimated_effort,
                weekdays=task.weekdays
            )
            for task in db_task
        ]

    def create_task(self, task: PydanticTask) -> PydanticTask:
        if task.start_date > task.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date can't be more than end date"
            )
        task_id = task.id
        if task.id is None:
            task_id = str(uuid.uuid4())
        db_task = DBTask(
            id=task_id,
            group_id=task.group_id,
            name=task.name,
            start_date=task.start_date,
            end_date=task.end_date,
            estimated_effort=task.estimated_effort,
            weekdays=task.weekdays
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return PydanticTask(
            id=db_task.id,
            name=db_task.name,
            group_id=db_task.group_id,
            start_date=db_task.start_date,
            end_date=db_task.end_date,
            estimated_effort=db_task.estimated_effort,
            weekdays=db_task.weekdays
        )

    def tasks_for_day(self, day) -> List[PydanticTask]:
        db_task = self.db.query(DBTask).filter(DBTask.start_date<= day,
                                               DBTask.end_date >= day).all()
        return [
            PydanticTask(
                id=task.id,
                name=task.name,
                group_id=task.group_id,
                start_date=task.start_date,
                end_date=task.end_date,
                estimated_effort=task.estimated_effort/len(task.weekdays),
                weekdays=task.weekdays
            )
            for task in db_task
        ]
