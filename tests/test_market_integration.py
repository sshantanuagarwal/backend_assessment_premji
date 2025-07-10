import pytest
from datetime import datetime
from assessment_app.models.models import Portfolio, Trade
from assessment_app.repository.portfolio_repository import PortfolioRepository
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid

def test_trade_stock(client: TestClient, test_db: Session):
    # Create a test portfolio
    portfolio_repo = PortfolioRepository(test_db)
    portfolio = DBPortfolio(
        id=str(uuid.uuid4()),
        user_id=str(uuid.uuid4()),
        cash_balance=100000.0,
        current_ts=datetime.now(),
        net_worth=100000.0,
        created_at=datetime.now()
    )
    portfolio_repo.create_portfolio(portfolio)

    # Test creating a trade
    trade_data = {
        "stock_symbol": "RELIANCE",
        "quantity": 10,
        "price": 100.0,
        "trade_type": TradeType.BUY,
        "execution_ts": datetime.now().isoformat()
    }

    response = client.post("/market/trade", json=trade_data)
    assert response.status_code == 200
    assert response.json()["stock_symbol"] == trade_data["stock_symbol"]
    assert response.json()["quantity"] == trade_data["quantity"]

def test_get_market_data(client: TestClient):
    # Test getting market data
    response = client.get("/market/data/RELIANCE")
    assert response.status_code == 200
    assert "stock_symbol" in response.json()
    assert "price" in response.json()
    assert "timestamp" in response.json()

def test_get_available_stocks(client: TestClient):
    # Test getting available stocks
    response = client.get("/market/stocks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert "symbol" in response.json()[0]
    assert "current_price" in response.json()[0] 