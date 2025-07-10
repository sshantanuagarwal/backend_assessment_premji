import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from assessment_app.main import app
from assessment_app.models.constants import TradeType

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "username": "trader",
        "email": "trader@example.com",
        "password": "tradepassword"
    }

@pytest.fixture
def auth_headers(test_user):
    # Register and login the user
    client.post("/register", json=test_user)
    response = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_stock_data():
    return {
        "stock_symbol": "AAPL",
        "timestamp": datetime.now().isoformat(),
        "price": 150.0,
        "open_price": 148.0,
        "high_price": 152.0,
        "low_price": 147.0,
        "close_price": 151.0,
        "volume": 1000000
    }

@pytest.fixture
def test_trade():
    return {
        "stock_symbol": "AAPL",
        "quantity": 10,
        "price": 150.0,
        "trade_type": TradeType.BUY,
        "execution_ts": datetime.now().isoformat()
    }

def test_get_market_data_tick(test_stock_data, auth_headers):
    response = client.post(
        "/market/data/tick",
        json={
            "stock_symbol": test_stock_data["stock_symbol"],
            "timestamp": test_stock_data["timestamp"]
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["stock_symbol"] == test_stock_data["stock_symbol"]
    assert "price" in data
    assert "open_price" in data
    assert "high_price" in data
    assert "low_price" in data
    assert "close_price" in data
    assert "volume" in data

def test_get_market_data_range(test_stock_data, auth_headers):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    response = client.post(
        "/market/data/range",
        json={
            "stock_symbol": test_stock_data["stock_symbol"],
            "start_timestamp": start_time.isoformat(),
            "end_timestamp": end_time.isoformat()
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "stock_symbol" in data[0]
        assert "timestamp" in data[0]
        assert "price" in data[0]

def test_trade_stock(test_trade, auth_headers):
    response = client.post(
        "/market/trade",
        json=test_trade,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["stock_symbol"] == test_trade["stock_symbol"]
    assert data["quantity"] == test_trade["quantity"]
    assert data["price"] == test_trade["price"]
    assert data["trade_type"] == test_trade["trade_type"] 