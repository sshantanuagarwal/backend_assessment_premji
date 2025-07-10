import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from assessment_app.models.db_models import Base, User as DBUser
from assessment_app.service.auth_service import AuthService
from assessment_app.models.models import User, RegisterUserRequest
import uuid
from jose import jwt
from passlib.context import CryptContext

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_service(db_session):
    return AuthService(db_session)

@pytest.fixture
def test_user():
    return RegisterUserRequest(
        username="test_user",
        email="test@example.com",
        password="testpassword123"
    )

def test_register_user(auth_service, test_user):
    user = auth_service.register_user(test_user)
    assert user.username == test_user.username
    assert user.email == test_user.email
    assert user.id is not None

def test_authenticate_user(auth_service, test_user):
    # Register user first
    auth_service.register_user(test_user)
    
    # Test authentication
    token = auth_service.authenticate_user(test_user.email, test_user.password)
    assert token is not None
    
    # Verify token
    payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
    assert payload["sub"] == test_user.email

def test_get_current_user(auth_service, test_user):
    # Register user first
    user = auth_service.register_user(test_user)
    
    # Create token
    token = auth_service.authenticate_user(test_user.email, test_user.password)
    
    # Get current user
    current_user = auth_service.get_current_user(token)
    assert current_user.id == user.id
    assert current_user.email == user.email

def test_verify_password(auth_service):
    password = "testpassword123"
    hashed_password = auth_service.get_password_hash(password)
    assert auth_service.verify_password(password, hashed_password)

def test_get_password_hash(auth_service):
    password = "testpassword123"
    hashed_password = auth_service.get_password_hash(password)
    assert hashed_password != password
    assert len(hashed_password) > 0

def test_create_access_token(auth_service, test_user):
    token = auth_service.create_access_token({"sub": test_user.email})
    assert token is not None
    
    # Verify token
    payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
    assert payload["sub"] == test_user.email

def test_get_user_by_email(auth_service, test_user):
    # Register user first
    auth_service.register_user(test_user)
    
    # Get user by email
    user = auth_service.get_user_by_email(test_user.email)
    assert user is not None
    assert user.email == test_user.email

def test_get_user_by_username(auth_service, test_user):
    # Register user first
    auth_service.register_user(test_user)
    
    # Get user by username
    user = auth_service.get_user_by_username(test_user.username)
    assert user is not None
    assert user.username == test_user.username

def test_update_user(auth_service, test_user):
    # Register user first
    user = auth_service.register_user(test_user)
    
    # Update user
    updated_user = User(
        id=user.id,
        username="updated_username",
        email=user.email,
        hashed_password=user.hashed_password
    )
    result = auth_service.update_user(updated_user)
    assert result.username == "updated_username"

def test_delete_user(auth_service, test_user):
    # Register user first
    user = auth_service.register_user(test_user)
    
    # Delete user
    auth_service.delete_user(user.id)
    
    # Verify user is deleted
    deleted_user = auth_service.get_user_by_email(test_user.email)
    assert deleted_user is None 