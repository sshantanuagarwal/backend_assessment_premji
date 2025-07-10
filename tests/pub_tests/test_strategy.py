import pytest
from datetime import datetime
from assessment_app.models.models import PortfolioRequest, Strategy, RegisterUserRequest
from fastapi.testclient import TestClient
from assessment_app.main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    user_data = RegisterUserRequest(
        username="test_user",
        email="test@example.com",
        password="test_password"
    ).model_dump()
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def auth_headers(test_user):
    response = client.post("/auth/login", json={
        "username": test_user["username"],
        "password": "test_password"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_portfolio():
    return {
        "initial_capital": 100000.0
    }

@pytest.fixture
def test_strategy():
    return {
        "name": "Test Strategy",
        "description": "A test trading strategy",
        "parameters": {
            "stocks": ["AAPL", "GOOGL"],
            "moving_average_period": 20,
            "profit_target": 0.05
        }
    }

def test_create_portfolio(test_portfolio, auth_headers):
    response = client.post(
        "/portfolio",
        json=test_portfolio,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "user_id" in data
    assert "cash_balance" in data
    assert "current_ts" in data
    assert "net_worth" in data
    assert "created_at" in data
    assert data["cash_balance"] == test_portfolio["initial_capital"]

def test_get_portfolio(test_portfolio, auth_headers):
    # First create a portfolio
    create_response = client.post(
        "/portfolio",
        json=test_portfolio,
        headers=auth_headers
    )
    portfolio_id = create_response.json()["id"]
    
    # Then get the portfolio
    response = client.get(
        f"/portfolio/{portfolio_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "user_id" in data
    assert "cash_balance" in data
    assert "current_ts" in data
    assert "net_worth" in data
    assert "created_at" in data

def test_create_strategy(test_portfolio, test_strategy, auth_headers):
    # First create a portfolio
    portfolio_response = client.post(
        "/portfolio",
        json=test_portfolio,
        headers=auth_headers
    )
    portfolio_id = portfolio_response.json()["id"]
    
    # Add portfolio_id to strategy data
    strategy_data = test_strategy.copy()
    strategy_data["portfolio_id"] = portfolio_id
    
    # Create strategy
    response = client.post(
        "/strategy",
        json=strategy_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data
    assert "description" in data
    assert "parameters" in data
    assert "created_at" in data

def test_get_strategies(test_portfolio, test_strategy, auth_headers):
    # First create a portfolio
    portfolio_response = client.post(
        "/portfolio",
        json=test_portfolio,
        headers=auth_headers
    )
    portfolio_id = portfolio_response.json()["id"]
    
    # Add portfolio_id to strategy data
    strategy_data = test_strategy.copy()
    strategy_data["portfolio_id"] = portfolio_id
    
    # Create strategy
    client.post(
        "/strategy",
        json=strategy_data,
        headers=auth_headers
    )
    
    # Get all strategies
    response = client.get(
        f"/strategy?portfolio_id={portfolio_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    strategy = data[0]
    assert "id" in strategy
    assert "name" in strategy
    assert "description" in strategy
    assert "parameters" in strategy
    assert "created_at" in strategy

def test_get_portfolio_net_worth(test_portfolio, auth_headers):
    # First create a portfolio
    client.post(
        "/portfolio",
        json=test_portfolio,
        headers=auth_headers
    )
    
    # Get portfolio net worth
    response = client.get(
        "/portfolio-net-worth",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "net_worth" in data
    assert "cash_balance" in data
    assert "holdings" in data 