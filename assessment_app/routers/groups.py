from fastapi import APIRouter

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from assessment_app.models.models import (Group)
from assessment_app.repository.database import get_db
from assessment_app.repository.group import GroupRepository
from pydantic import BaseModel

from assessment_app.service.auth_service import get_current_user_from_request

router = APIRouter()


@router.get("/groups", response_model=List[Group])
async def get_groups(
        db: Session = Depends(get_db)
) -> List[Group]:
    """
    Get all groups available.
    """
    group_repo = GroupRepository(db)
    return group_repo.get_all_groups()


@router.post("/groups", response_model=Group)
async def create_groups(
        group: Group,
        db: Session = Depends(get_db)
) -> Group:
    """
    Create a new trading groups.
    """
    groups_repo = GroupRepository(db)
    return groups_repo.create_group(group)
