import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from assessment_app.main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "username": "backtester",
        "email": "backtester@example.com",
        "password": "backtest123"
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
def test_backtest_params():
    end_time = datetime.now()
    start_time = end_time - timedelta(days=90)
    return {
        "strategy_id": "test_strategy_id",
        "portfolio_id": "test_portfolio_id",
        "start_date": start_time.isoformat(),
        "end_date": end_time.isoformat(),
        "initial_capital": 10000.0
    }

def test_backtest_strategy(test_backtest_params, auth_headers):
    # Create a strategy first
    strategy = {
        "name": "Test Backtest Strategy",
        "description": "A strategy for backtesting",
        "parameters": {
            "stocks": ["AAPL", "GOOGL"],
            "moving_average_period": 20,
            "profit_target": 0.05
        }
    }
    strategy_response = client.post(
        "/strategies",
        json=strategy,
        headers=auth_headers
    )
    strategy_id = strategy_response.json()["id"]

    # Create a portfolio
    portfolio = {
        "initial_capital": test_backtest_params["initial_capital"]
    }
    portfolio_response = client.post(
        "/portfolio",
        json=portfolio,
        headers=auth_headers
    )
    portfolio_id = portfolio_response.json()["id"]

    # Update backtest params with actual IDs
    test_backtest_params["strategy_id"] = strategy_id
    test_backtest_params["portfolio_id"] = portfolio_id

    # Run backtest
    response = client.post(
        "/backtest",
        json=test_backtest_params,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "start_date" in data
    assert "end_date" in data
    assert "initial_capital" in data
    assert "final_capital" in data
    assert "trades" in data
    assert "profit_loss" in data
    assert "annualized_return" in data

    # Verify trade data structure
    if data["trades"]:
        trade = data["trades"][0]
        assert "stock_symbol" in trade
        assert "quantity" in trade
        assert "price" in trade
        assert "trade_type" in trade
        assert "execution_ts" in trade 