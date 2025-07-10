import pytest
from fastapi.testclient import TestClient
from assessment_app.main import app
from assessment_app.repository.database import Base, get_db
from assessment_app.tests.test_config import engine, get_test_db

@pytest.fixture(autouse=True)
def setup_database():
    # Drop all tables to ensure clean state
    Base.metadata.drop_all(bind=engine)
    # Create tables before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_client():
    # Override the database dependency
    app.dependency_overrides[get_db] = get_test_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear() 