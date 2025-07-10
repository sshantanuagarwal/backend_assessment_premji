import pytest
from datetime import datetime, timedelta
from assessment_app.service.analysis_service import AnalysisService
from assessment_app.models.models import Portfolio, PortfolioHolding
import uuid

@pytest.fixture
def analysis_service():
    return AnalysisService()

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
def test_holdings():
    return [
        PortfolioHolding(
            stock_symbol="RELIANCE",
            quantity=10,
            average_price=285.73,
            current_value=2857.30
        ),
        PortfolioHolding(
            stock_symbol="HDFCBANK",
            quantity=5,
            average_price=1242.60,
            current_value=6213.00
        )
    ]

def test_compute_cagr(analysis_service):
    start_price = 100.0
    end_price = 121.0
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    cagr = analysis_service.compute_cagr(start_price, end_price, start_date, end_date)
    assert abs(cagr - 0.21) < 0.01  # 21% CAGR

def test_compute_portfolio_returns(analysis_service, test_portfolio, test_holdings):
    start_ts = datetime.now() - timedelta(days=30)
    end_ts = datetime.now()
    
    returns = analysis_service.compute_portfolio_returns(
        test_portfolio,
        test_holdings,
        start_ts,
        end_ts
    )
    
    assert returns.total_investment > 0
    assert returns.current_value > 0
    assert isinstance(returns.returns, float)
    assert isinstance(returns.returns_percentage, float)
    assert len(returns.holdings) == len(test_holdings)

def test_compute_stock_returns(analysis_service):
    start_ts = datetime.now() - timedelta(days=30)
    end_ts = datetime.now()
    start_price = 100.0
    end_price = 110.0
    
    returns = analysis_service.compute_stock_returns(
        start_price,
        end_price,
        start_ts,
        end_ts
    )
    
    assert isinstance(returns, float)
    assert returns > 0

def test_compute_portfolio_net_worth(analysis_service, test_portfolio, test_holdings):
    net_worth = analysis_service.compute_portfolio_net_worth(
        test_portfolio,
        test_holdings
    )
    
    assert net_worth > 0
    assert net_worth == test_portfolio.cash_balance + sum(h.current_value for h in test_holdings)

def test_compute_holding_returns(analysis_service, test_holdings):
    start_ts = datetime.now() - timedelta(days=30)
    end_ts = datetime.now()
    
    for holding in test_holdings:
        returns = analysis_service.compute_holding_returns(
            holding,
            start_ts,
            end_ts
        )
        
        assert isinstance(returns, float)
        assert isinstance(returns.returns_percentage, float)

def test_compute_portfolio_risk_metrics(analysis_service, test_portfolio, test_holdings):
    start_ts = datetime.now() - timedelta(days=30)
    end_ts = datetime.now()
    
    risk_metrics = analysis_service.compute_portfolio_risk_metrics(
        test_portfolio,
        test_holdings,
        start_ts,
        end_ts
    )
    
    assert isinstance(risk_metrics.volatility, float)
    assert isinstance(risk_metrics.sharpe_ratio, float)
    assert isinstance(risk_metrics.max_drawdown, float)

def test_compute_stock_risk_metrics(analysis_service):
    start_ts = datetime.now() - timedelta(days=30)
    end_ts = datetime.now()
    prices = [100.0, 105.0, 110.0, 115.0, 120.0]
    
    risk_metrics = analysis_service.compute_stock_risk_metrics(
        prices,
        start_ts,
        end_ts
    )
    
    assert isinstance(risk_metrics.volatility, float)
    assert isinstance(risk_metrics.sharpe_ratio, float)
    assert isinstance(risk_metrics.max_drawdown, float) 