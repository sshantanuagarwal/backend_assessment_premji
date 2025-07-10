from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from assessment_app.models.db_models import Strategy as DBStrategy, Portfolio as DBPortfolio
from assessment_app.models.models import Strategy, Portfolio, PortfolioRequest, BacktestResponse
from assessment_app.repository.portfolio_repository import PortfolioRepository
from assessment_app.repository.strategy_repository import StrategyRepository


class StrategyService:
    def __init__(self, db: Session):
        self.db = db
        self.strategy_repo = StrategyRepository(db)
        self.portfolio_repo = PortfolioRepository(db)

    def create_strategy(self, strategy: Strategy) -> Strategy:
        """Create a new strategy"""
        db_strategy = DBStrategy(
            id=strategy.id,
            user_id=strategy.user_id,
            name=strategy.name,
            description=strategy.description,
            parameters=strategy.parameters,
            created_at=strategy.created_at
        )
        return self.strategy_repo.create_strategy(db_strategy)

    def get_strategy(self, strategy_id: str) -> Optional[Strategy]:
        """Get a strategy by ID"""
        return self.strategy_repo.get_strategy(strategy_id)

    def get_user_strategies(self, user_id: str) -> List[Strategy]:
        """Get all strategies for a user"""
        return self.strategy_repo.get_user_strategies(user_id)

    def update_strategy(self, strategy: Strategy) -> Strategy:
        """Update a strategy"""
        db_strategy = DBStrategy(
            id=strategy.id,
            user_id=strategy.user_id,
            name=strategy.name,
            description=strategy.description,
            parameters=strategy.parameters,
            created_at=strategy.created_at
        )
        return self.strategy_repo.update_strategy(db_strategy)

    def delete_strategy(self, strategy_id: str) -> None:
        """Delete a strategy"""
        self.strategy_repo.delete_strategy(strategy_id)

    def create_portfolio(self, user_id: str, portfolio_request: PortfolioRequest) -> Portfolio:
        """Create a new portfolio"""
        db_portfolio = DBPortfolio(
            user_id=user_id,
            initial_capital=portfolio_request.initial_capital,
            current_capital=portfolio_request.initial_capital,
            created_at=datetime.now()
        )
        return self.portfolio_repo.create_portfolio(db_portfolio)

    def get_portfolio(self, portfolio_id: str) -> Optional[Portfolio]:
        """Get a portfolio by ID"""
        return self.portfolio_repo.get_portfolio(portfolio_id)

    def get_user_portfolio(self, user_id: str) -> Optional[Portfolio]:
        """Get a user's portfolio"""
        return self.portfolio_repo.get_user_portfolio(user_id)

    def update_portfolio(self, portfolio: Portfolio) -> Portfolio:
        """Update a portfolio"""
        db_portfolio = DBPortfolio(
            id=portfolio.id,
            user_id=portfolio.user_id,
            initial_capital=portfolio.initial_capital,
            current_capital=portfolio.current_capital,
            created_at=portfolio.created_at
        )
        return self.portfolio_repo.update_portfolio(db_portfolio)

    def delete_portfolio(self, portfolio_id: str) -> None:
        """Delete a portfolio"""
        self.portfolio_repo.delete_portfolio(portfolio_id)

    def execute_strategy(self, strategy_id: str, portfolio_id: str, start_ts: datetime, end_ts: datetime) -> BacktestResponse:
        """Execute a strategy on a portfolio"""
        strategy = self.get_strategy(strategy_id)
        portfolio = self.get_portfolio(portfolio_id)
        
        if not strategy or not portfolio:
            return None
        
        # Placeholder for strategy execution logic
        # In a real implementation, this would:
        # 1. Load historical data for the date range
        # 2. Apply the strategy's rules to generate trade signals
        # 3. Execute trades based on the signals
        # 4. Calculate returns and risk metrics
        
        return BacktestResponse(
            trades=[],  # List of trades executed
            returns=0.0,  # Portfolio returns
            risk_metrics={  # Risk metrics
                "volatility": 0.0,
                "sharpe_ratio": 0.0,
                "max_drawdown": 0.0
            }
        ) 