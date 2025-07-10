import logging
from assessment_app.models.base import Base
from assessment_app.repository.database import engine

# Configure logging
logger = logging.getLogger(__name__)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Successfully created database tables")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise 