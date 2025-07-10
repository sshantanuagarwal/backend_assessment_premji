from typing import List, Optional
from sqlalchemy.orm import Session
from assessment_app.models.db_models import User as DBUser
from assessment_app.models.models import UserResponse, RegisterUserRequest

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: str) -> Optional[DBUser]:
        return self.db.query(DBUser).filter(DBUser.id == user_id).first()

    def get_user_by_id(self, user_id: str) -> Optional[DBUser]:
        return self.get_user(user_id)

    def get_user_by_email(self, email: str) -> Optional[DBUser]:
        return self.db.query(DBUser).filter(DBUser.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[DBUser]:
        return self.db.query(DBUser).filter(DBUser.username == username).first()

    def get_all_users(self) -> List[DBUser]:
        return self.db.query(DBUser).all()

    def create_user(self, user: DBUser) -> DBUser:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: DBUser) -> DBUser:
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: str) -> bool:
        user = self.get_user(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False 