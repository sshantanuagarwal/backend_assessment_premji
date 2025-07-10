import os

class Config:
    # Feature flags
    SKIP_AUTH = os.getenv("SKIP_AUTH", "false").lower() == "true"
    
    # Database configuration
    DB_USER = os.getenv("POSTGRES_USER", "user")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    DB_HOST = os.getenv("POSTGRES_HOST", "db")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME = os.getenv("POSTGRES_DB", "db")
    
    # Security configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # Test user configuration
    TEST_USER_ID = "test-user-id"
    TEST_USER_EMAIL = "test@example.com" 