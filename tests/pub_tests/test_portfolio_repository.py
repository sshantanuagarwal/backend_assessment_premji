import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from assessment_app.models.db_models import Base, Portfolio as DBPortfolio, PortfolioHolding as DBPortfolioHolding
from assessment_app.repository.portfolio_repository import PortfolioRepository
from assessment_app.models.models import Portfolio, PortfolioHolding
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
def portfolio_repo(db_session):
    return PortfolioRepository(db_session)

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
def test_holding(test_portfolio):
    return PortfolioHolding(
        stock_symbol="RELIANCE",
        quantity=10,
        average_price=285.73,
        current_value=2857.30
    )

def test_create_portfolio(portfolio_repo, test_portfolio):
    created_portfolio = portfolio_repo.create_portfolio(test_portfolio)
    assert created_portfolio.id == test_portfolio.id
    assert created_portfolio.user_id == test_portfolio.user_id
    assert created_portfolio.cash_balance == test_portfolio.cash_balance
    assert created_portfolio.net_worth == test_portfolio.net_worth

def test_get_portfolio(portfolio_repo, test_portfolio):
    portfolio_repo.create_portfolio(test_portfolio)
    retrieved_portfolio = portfolio_repo.get_portfolio(test_portfolio.user_id)
    assert retrieved_portfolio.id == test_portfolio.id
    assert retrieved_portfolio.user_id == test_portfolio.user_id

def test_get_portfolio_by_id(portfolio_repo, test_portfolio):
    created_portfolio = portfolio_repo.create_portfolio(test_portfolio)
    retrieved_portfolio = portfolio_repo.get_portfolio_by_id(created_portfolio.id)
    assert retrieved_portfolio.id == test_portfolio.id
    assert retrieved_portfolio.user_id == test_portfolio.user_id

def test_update_portfolio(portfolio_repo, test_portfolio):
    created_portfolio = portfolio_repo.create_portfolio(test_portfolio)
    created_portfolio.cash_balance = 90000.0
    updated_portfolio = portfolio_repo.update_portfolio(created_portfolio)
    assert updated_portfolio.cash_balance == 90000.0

def test_delete_portfolio(portfolio_repo, test_portfolio):
    created_portfolio = portfolio_repo.create_portfolio(test_portfolio)
    portfolio_repo.delete_portfolio(created_portfolio.user_id)
    retrieved_portfolio = portfolio_repo.get_portfolio(created_portfolio.user_id)
    assert retrieved_portfolio is None

def test_get_holdings(portfolio_repo, test_portfolio, test_holding):
    created_portfolio = portfolio_repo.create_portfolio(test_portfolio)
    holding = portfolio_repo.get_holdings(created_portfolio.user_id, test_holding.stock_symbol)
    assert holding is None  # No holdings initially

def test_get_all_holdings(portfolio_repo, test_portfolio):
    created_portfolio = portfolio_repo.create_portfolio(test_portfolio)
    holdings = portfolio_repo.get_all_holdings(created_portfolio.user_id)
    assert len(holdings) == 0  # No holdings initially

def test_get_all_portfolios(portfolio_repo, test_portfolio):
    created_portfolio = portfolio_repo.create_portfolio(test_portfolio)
    portfolios = portfolio_repo.get_all_portfolios()
    assert len(portfolios) == 1
    assert portfolios[0].id == created_portfolio.id 