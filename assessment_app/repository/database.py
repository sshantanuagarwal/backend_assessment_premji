import os
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "db")  # This should match the POSTGRES_DB in docker-compose.yml

# Use SQLite for testing
if os.getenv("TESTING", "false").lower() == "true":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
else:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    logger.info(f"Connecting to database at host: {DB_HOST}, port: {DB_PORT}, database: {DB_NAME}")
    try:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_pre_ping=True,  # Enable connection health checks
            echo=True  # Enable SQL query logging
        )
        
        # Test the connection
        with engine.connect() as conn:
            logger.info("Successfully connected to the database")
            
    except Exception as e:
        logger.error(f"Failed to connect to the database: {str(e)}")
        logger.error(f"Connection URL: {SQLALCHEMY_DATABASE_URL}")
        raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
