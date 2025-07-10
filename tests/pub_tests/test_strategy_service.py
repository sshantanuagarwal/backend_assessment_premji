import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from assessment_app.models.db_models import Base, Strategy as DBStrategy
from assessment_app.service.strategy_service import StrategyService
from assessment_app.models.models import Strategy, Portfolio, PortfolioRequest
import uuid

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
def strategy_service(db_session):
    return StrategyService(db_session)

@pytest.fixture
def test_user_id():
    return str(uuid.uuid4())

@pytest.fixture
def test_portfolio(test_user_id):
    return Portfolio(
        id=str(uuid.uuid4()),
        user_id=test_user_id,
        cash_balance=100000.0,
        current_ts=datetime.now(),
        net_worth=100000.0,
        created_at=datetime.now()
    )

@pytest.fixture
def test_strategy(test_user_id):
    return Strategy(
        id=str(uuid.uuid4()),
        user_id=test_user_id,
        name="Test Strategy",
        description="A test strategy",
        parameters={"param1": "value1"},
        created_at=datetime.now()
    )

def test_create_strategy(strategy_service, test_strategy):
    created_strategy = strategy_service.create_strategy(test_strategy)
    assert created_strategy.id == test_strategy.id
    assert created_strategy.user_id == test_strategy.user_id
    assert created_strategy.name == test_strategy.name
    assert created_strategy.description == test_strategy.description

def test_get_strategy(strategy_service, test_strategy):
    created_strategy = strategy_service.create_strategy(test_strategy)
    retrieved_strategy = strategy_service.get_strategy(created_strategy.id)
    assert retrieved_strategy.id == test_strategy.id
    assert retrieved_strategy.user_id == test_strategy.user_id

def test_get_user_strategies(strategy_service, test_strategy):
    created_strategy = strategy_service.create_strategy(test_strategy)
    strategies = strategy_service.get_user_strategies(created_strategy.user_id)
    assert len(strategies) == 1
    assert strategies[0].id == created_strategy.id

def test_update_strategy(strategy_service, test_strategy):
    created_strategy = strategy_service.create_strategy(test_strategy)
    created_strategy.name = "Updated Strategy"
    updated_strategy = strategy_service.update_strategy(created_strategy)
    assert updated_strategy.name == "Updated Strategy"

def test_delete_strategy(strategy_service, test_strategy):
    created_strategy = strategy_service.create_strategy(test_strategy)
    strategy_service.delete_strategy(created_strategy.id)
    retrieved_strategy = strategy_service.get_strategy(created_strategy.id)
    assert retrieved_strategy is None

def test_create_portfolio(strategy_service, test_user_id):
    portfolio_request = PortfolioRequest(
        initial_capital=100000.0
    )
    portfolio = strategy_service.create_portfolio(test_user_id, portfolio_request)
    assert portfolio.user_id == test_user_id
    assert portfolio.cash_balance == 100000.0
    assert portfolio.net_worth == 100000.0

def test_get_portfolio(strategy_service, test_portfolio):
    created_portfolio = strategy_service.create_portfolio(
        test_portfolio.user_id,
        PortfolioRequest(initial_capital=test_portfolio.cash_balance)
    )
    retrieved_portfolio = strategy_service.get_portfolio(created_portfolio.id)
    assert retrieved_portfolio.id == created_portfolio.id
    assert retrieved_portfolio.user_id == created_portfolio.user_id

def test_get_user_portfolio(strategy_service, test_portfolio):
    created_portfolio = strategy_service.create_portfolio(
        test_portfolio.user_id,
        PortfolioRequest(initial_capital=test_portfolio.cash_balance)
    )
    portfolio = strategy_service.get_user_portfolio(created_portfolio.user_id)
    assert portfolio.id == created_portfolio.id
    assert portfolio.user_id == created_portfolio.user_id

def test_update_portfolio(strategy_service, test_portfolio):
    created_portfolio = strategy_service.create_portfolio(
        test_portfolio.user_id,
        PortfolioRequest(initial_capital=test_portfolio.cash_balance)
    )
    created_portfolio.cash_balance = 90000.0
    updated_portfolio = strategy_service.update_portfolio(created_portfolio)
    assert updated_portfolio.cash_balance == 90000.0

def test_delete_portfolio(strategy_service, test_portfolio):
    created_portfolio = strategy_service.create_portfolio(
        test_portfolio.user_id,
        PortfolioRequest(initial_capital=test_portfolio.cash_balance)
    )
    strategy_service.delete_portfolio(created_portfolio.id)
    retrieved_portfolio = strategy_service.get_portfolio(created_portfolio.id)
    assert retrieved_portfolio is None

def test_execute_strategy(strategy_service, test_strategy, test_portfolio):
    created_strategy = strategy_service.create_strategy(test_strategy)
    created_portfolio = strategy_service.create_portfolio(
        test_portfolio.user_id,
        PortfolioRequest(initial_capital=test_portfolio.cash_balance)
    )
    
    result = strategy_service.execute_strategy(
        created_strategy.id,
        created_portfolio.id,
        datetime.now(),
        datetime.now() + timedelta(days=1)
    )
    
    assert result is not None
    assert "trades" in result
    assert "returns" in result
    assert "risk_metrics" in result 