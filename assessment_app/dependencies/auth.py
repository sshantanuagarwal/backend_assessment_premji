from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from assessment_app.dependencies.database import get_db
from assessment_app.repository.user_repository import UserRepository

async def get_current_user(x_user_id: str = Header(..., alias="X-User-ID")) -> str:
    """
    Get the current user ID from the X-User-ID header.
    """
    if not x_user_id:
        raise HTTPException(status_code=401, detail="X-User-ID header is required")
    return x_user_id 