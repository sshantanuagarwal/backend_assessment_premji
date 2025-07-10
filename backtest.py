from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from assessment_app.models.models import BacktestRequest, BacktestResponse
from assessment_app.service.auth_service import get_current_user_from_request
from assessment_app.repository.database import get_db
from assessment_app.repository.portfolio_repository import PortfolioRepository
from assessment_app.repository.strategy_repository import StrategyRepository
from assessment_app.service.strategy_service import StrategyService

router = APIRouter()

@router.post("/backtest", response_model=BacktestResponse)
async def run_backtest(
    backtest_request: BacktestRequest,
    current_user_id: str = Depends(get_current_user_from_request),
    db: Session = Depends(get_db)
) -> BacktestResponse:
    """
    Run a backtest for a given strategy and portfolio.
    """
    try:
        # Validate portfolio ownership
        portfolio_repo = PortfolioRepository(db)
        portfolio = portfolio_repo.get_portfolio_by_id(backtest_request.portfolio_id)
        
        if not portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found"
            )
        
        if portfolio.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this portfolio"
            )
        
        # Get strategy
        strategy_repo = StrategyRepository(db)
        strategy = strategy_repo.get_strategy_by_id(backtest_request.strategy_id)
        
        if not strategy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Strategy not found"
            )
        
        # Initialize strategy service
        strategy_service = StrategyService()
        
        # Run backtest
        backtest_result = strategy_service.run_backtest(
            strategy=strategy,
            portfolio=portfolio,
            start_ts=backtest_request.start_ts,
            end_ts=backtest_request.end_ts,
            initial_capital=backtest_request.initial_capital
        )
        
        return backtest_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )