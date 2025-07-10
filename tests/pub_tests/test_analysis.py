import pytest
from datetime import datetime, timedelta
from assessment_app.models.models import PortfolioRequest, RegisterUserRequest
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
def test_analysis_params():
    return {
        "start_timestamp": (datetime.now() - timedelta(days=30)).isoformat(),
        "end_timestamp": datetime.now().isoformat()
    }

def test_estimate_portfolio_returns(test_portfolio, test_analysis_params, auth_headers):
    # Create a portfolio first
    portfolio_response = client.post(
        "/portfolio",
        json=test_portfolio,
        headers=auth_headers
    )
    portfolio_id = portfolio_response.json()["id"]
    
    # Get portfolio returns
    response = client.get(
        f"/analysis/estimate_returns/portfolio/{portfolio_id}",
        params={
            "start_timestamp": test_analysis_params["start_timestamp"],
            "end_timestamp": test_analysis_params["end_timestamp"]
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "returns" in data
    assert "returns_percentage" in data

def test_get_portfolio_analysis(test_portfolio, auth_headers):
    # Create a portfolio first
    portfolio_response = client.post(
        "/portfolio",
        json=test_portfolio,
        headers=auth_headers
    )
    portfolio_id = portfolio_response.json()["id"]
    
    # Get portfolio analysis
    response = client.get(
        f"/analysis/portfolio/{portfolio_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_investment" in data
    assert "current_value" in data
    assert "returns" in data
    assert "returns_percentage" in data
    assert "holdings" in data
    assert "portfolio_id" in data
    assert "user_id" in data
    assert "initial_capital" in data
    assert "current_capital" in data
    
    # Verify holdings structure
    assert isinstance(data["holdings"], list)
    if data["holdings"]:
        holding = data["holdings"][0]
        assert "stock_symbol" in holding
        assert "quantity" in holding
        assert "average_price" in holding
        assert "current_price" in holding
        assert "total_value" in holding
        assert "profit_loss" in holding

def test_get_stock_analysis(test_analysis_params, auth_headers):
    response = client.get(
        "/analysis/estimate_returns/stock",
        params=test_analysis_params,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "returns" in data
    assert "returns_percentage" in data
    assert "start_price" in data
    assert "end_price" in data 