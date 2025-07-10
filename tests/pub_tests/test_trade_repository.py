import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from assessment_app.models.db_models import Base, Trade as DBTrade
from assessment_app.repository.trade_repository import TradeRepository
from assessment_app.models.models import Trade, TradeType
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
def trade_repo(db_session):
    return TradeRepository(db_session)

@pytest.fixture
def test_user_id():
    return str(uuid.uuid4())

@pytest.fixture
def test_trade():
    return DBTrade(
        id=str(uuid.uuid4()),
        user_id=str(uuid.uuid4()),
        stock_symbol="RELIANCE",
        quantity=10,
        price=100.0,
        trade_type="BUY",
        execution_ts=datetime.now(),
        created_at=datetime.now()
    )

def test_create_trade(trade_repo, test_trade):
    created_trade = trade_repo.create_trade(test_trade)
    assert created_trade.id == test_trade.id
    assert created_trade.user_id == test_trade.user_id
    assert created_trade.stock_symbol == test_trade.stock_symbol
    assert created_trade.quantity == test_trade.quantity
    assert created_trade.price == test_trade.price
    assert created_trade.trade_type == test_trade.trade_type

def test_get_trade(trade_repo, test_trade):
    created_trade = trade_repo.create_trade(test_trade)
    retrieved_trade = trade_repo.get_trade(created_trade.id)
    assert retrieved_trade.id == test_trade.id
    assert retrieved_trade.user_id == test_trade.user_id
    assert retrieved_trade.stock_symbol == test_trade.stock_symbol

def test_get_user_trades(trade_repo, test_trade):
    created_trade = trade_repo.create_trade(test_trade)
    trades = trade_repo.get_user_trades(test_trade.user_id)
    assert len(trades) == 1
    assert trades[0].id == created_trade.id

def test_get_trades_by_stock(trade_repo, test_trade):
    created_trade = trade_repo.create_trade(test_trade)
    trades = trade_repo.get_trades_by_stock(test_trade.stock_symbol)
    assert len(trades) == 1
    assert trades[0].id == created_trade.id

def test_get_trades_by_type(trade_repo, test_trade):
    created_trade = trade_repo.create_trade(test_trade)
    trades = trade_repo.get_trades_by_type(test_trade.trade_type)
    assert len(trades) == 1
    assert trades[0].id == created_trade.id

def test_get_trades_by_time_range(trade_repo, test_trade):
    created_trade = trade_repo.create_trade(test_trade)
    start_ts = datetime.now() - timedelta(days=1)
    end_ts = datetime.now() + timedelta(days=1)
    trades = trade_repo.get_trades_by_time_range(start_ts, end_ts)
    assert len(trades) == 1
    assert trades[0].id == created_trade.id

def test_delete_trade(trade_repo, test_trade):
    created_trade = trade_repo.create_trade(test_trade)
    trade_repo.delete_trade(created_trade.id)
    assert trade_repo.get_trade(created_trade.id) is None 