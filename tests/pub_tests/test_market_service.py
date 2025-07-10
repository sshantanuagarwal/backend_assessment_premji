import pytest
from datetime import datetime, timedelta
from assessment_app.service.market_service import MarketService
from assessment_app.models.models import Trade, TradeType, TickData
import pandas as pd
import os
import uuid

@pytest.fixture
def market_service():
    return MarketService()

@pytest.fixture
def test_user_id():
    return str(uuid.uuid4())

@pytest.fixture
def test_trade(test_user_id):
    return Trade(
        id=str(uuid.uuid4()),
        user_id=test_user_id,
        stock_symbol="RELIANCE",
        quantity=10,
        price=285.73,
        trade_type=TradeType.BUY,
        execution_ts=datetime.now(),
        created_at=datetime.now()
    )

@pytest.fixture
def test_tick_data():
    return TickData(
        stock_symbol="RELIANCE",
        timestamp=datetime.now(),
        price=285.73,
        open_price=284.50,
        high_price=286.20,
        low_price=283.80,
        close_price=285.50,
        volume=1000000
    )

def test_get_stock_data(market_service):
    stock_symbol = "RELIANCE"
    timestamp = datetime.now()
    
    # Create test data file
    test_data = pd.DataFrame({
        'Date': [timestamp.date()],
        'Open': [284.50],
        'High': [286.20],
        'Low': [283.80],
        'Close': [285.50],
        'Volume': [1000000]
    })
    test_data.to_csv(f"assessment_app/data/{stock_symbol}.csv", index=False)
    
    try:
        df = market_service.get_stock_data(stock_symbol, timestamp)
        assert not df.empty
        assert df.iloc[0]['Open'] == 284.50
        assert df.iloc[0]['Close'] == 285.50
    finally:
        # Clean up test file
        os.remove(f"assessment_app/data/{stock_symbol}.csv")

def test_get_stock_data_range(market_service):
    stock_symbol = "RELIANCE"
    start_ts = datetime.now() - timedelta(days=2)
    end_ts = datetime.now()
    
    # Create test data file
    test_data = pd.DataFrame({
        'Date': [start_ts.date(), end_ts.date()],
        'Open': [284.50, 285.50],
        'High': [286.20, 286.50],
        'Low': [283.80, 284.20],
        'Close': [285.50, 286.00],
        'Volume': [1000000, 1200000]
    })
    test_data.to_csv(f"assessment_app/data/{stock_symbol}.csv", index=False)
    
    try:
        df = market_service.get_stock_data_range(stock_symbol, start_ts, end_ts)
        assert len(df) == 2
        assert df.iloc[0]['Open'] == 284.50
        assert df.iloc[1]['Close'] == 286.00
    finally:
        # Clean up test file
        os.remove(f"assessment_app/data/{stock_symbol}.csv")

def test_validate_trade(market_service, test_trade):
    # Create test data file
    stock_symbol = test_trade.stock_symbol
    test_data = pd.DataFrame({
        'Date': [test_trade.execution_ts.date()],
        'Open': [test_trade.price - 1],
        'High': [test_trade.price + 1],
        'Low': [test_trade.price - 2],
        'Close': [test_trade.price],
        'Volume': [1000000]
    })
    test_data.to_csv(f"assessment_app/data/{stock_symbol}.csv", index=False)
    
    try:
        is_valid = market_service.validate_trade(test_trade)
        assert is_valid
    finally:
        # Clean up test file
        os.remove(f"assessment_app/data/{stock_symbol}.csv")

def test_get_current_price(market_service):
    stock_symbol = "RELIANCE"
    timestamp = datetime.now()
    
    # Create test data file
    test_data = pd.DataFrame({
        'Date': [timestamp.date()],
        'Open': [284.50],
        'High': [286.20],
        'Low': [283.80],
        'Close': [285.50],
        'Volume': [1000000]
    })
    test_data.to_csv(f"assessment_app/data/{stock_symbol}.csv", index=False)
    
    try:
        price = market_service.get_current_price(stock_symbol, timestamp)
        assert price == (284.50 + 285.50) / 2
    finally:
        # Clean up test file
        os.remove(f"assessment_app/data/{stock_symbol}.csv")

def test_get_tick_data(market_service):
    stock_symbol = "RELIANCE"
    timestamp = datetime.now()
    
    # Create test data file
    test_data = pd.DataFrame({
        'Date': [timestamp.date()],
        'Open': [284.50],
        'High': [286.20],
        'Low': [283.80],
        'Close': [285.50],
        'Volume': [1000000]
    })
    test_data.to_csv(f"assessment_app/data/{stock_symbol}.csv", index=False)
    
    try:
        tick_data = market_service.get_tick_data(stock_symbol, timestamp)
        assert isinstance(tick_data, TickData)
        assert tick_data.stock_symbol == stock_symbol
        assert tick_data.price == (284.50 + 285.50) / 2
    finally:
        # Clean up test file
        os.remove(f"assessment_app/data/{stock_symbol}.csv")

def test_get_available_stocks(market_service):
    # Create test data files
    stocks = ["RELIANCE", "HDFCBANK", "ICICIBANK"]
    for stock in stocks:
        test_data = pd.DataFrame({
            'Date': [datetime.now().date()],
            'Open': [100.0],
            'High': [101.0],
            'Low': [99.0],
            'Close': [100.5],
            'Volume': [1000000]
        })
        test_data.to_csv(f"assessment_app/data/{stock}.csv", index=False)
    
    try:
        available_stocks = market_service.get_available_stocks()
        assert len(available_stocks) == len(stocks)
        for stock in stocks:
            assert any(s.stock_symbol == stock for s in available_stocks)
    finally:
        # Clean up test files
        for stock in stocks:
            os.remove(f"assessment_app/data/{stock}.csv") 