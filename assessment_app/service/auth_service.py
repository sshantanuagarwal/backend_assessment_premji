from datetime import datetime, timedelta
from typing import Optional, Dict
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from assessment_app.models.models import UserResponse, RegisterUserRequest
from assessment_app.models.db_models import User as DBUser
from assessment_app.repository.user_repository import UserRepository
from assessment_app.config import Config
from fastapi import Request, HTTPException, status, Depends, Header
from fastapi.security import OAuth2PasswordBearer

from assessment_app.models.constants import JWT_TOKEN
from assessment_app.repository.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register_user(self, user_request: RegisterUserRequest) -> UserResponse:
        """Register a new user"""
        # Check if user already exists
        if self.get_user_by_email(user_request.email):
            raise ValueError("Email already registered")
        if self.get_user_by_username(user_request.username):
            raise ValueError("Username already taken")
        
        # Create new user
        hashed_password = self.get_password_hash(user_request.password)
        db_user = DBUser(
            username=user_request.username,
            email=user_request.email,
            hashed_password=hashed_password,
            created_at=datetime.now()
        )
        created_user = self.user_repo.create_user(db_user)
        return UserResponse.from_orm(created_user)

    def authenticate_user(self, email: str, password: str) -> Optional[str]:
        """Authenticate user and return access token"""
        user = self.get_user_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        
        access_token = self.create_access_token({"sub": email})
        return access_token

    def get_current_user(self, token: str) -> Optional[UserResponse]:
        """Get current user from token"""
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
            email = payload.get("sub")
            if email is None:
                return None
            user = self.get_user_by_email(email)
            return UserResponse.from_orm(user) if user else None
        except JWTError:
            return None

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Get password hash"""
        return pwd_context.hash(password)

    def create_access_token(self, data: Dict) -> str:
        """Create access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
        return encoded_jwt

    def get_user_by_email(self, email: str) -> Optional[DBUser]:
        """Get user by email"""
        return self.user_repo.get_user_by_email(email)

    def get_user_by_username(self, username: str) -> Optional[DBUser]:
        """Get user by username"""
        return self.user_repo.get_user_by_username(username)

    def update_user(self, user: UserResponse) -> UserResponse:
        """Update user"""
        db_user = DBUser(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            created_at=datetime.now()
        )
        updated_user = self.user_repo.update_user(db_user)
        return UserResponse.from_orm(updated_user)

    def delete_user(self, user_id: str) -> None:
        """Delete user"""
        self.user_repo.delete_user(user_id)

async def get_current_user_from_request(
    request: Request,
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: Session = Depends(get_db)
) -> str:
    """
    Get user ID from X-User-ID header.
    If SKIP_AUTH is enabled, return the provided user ID.
    """
    # If SKIP_AUTH is enabled, return the provided user ID
    if Config.SKIP_AUTH:
        return x_user_id
    
    # Try to get token from cookies first
    token = request.cookies.get(JWT_TOKEN)
    
    # If not in cookies, try Authorization header
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user.id
