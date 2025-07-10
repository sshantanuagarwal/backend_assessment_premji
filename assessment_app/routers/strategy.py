from datetime import datetime
from typing import List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from assessment_app.models.models import Portfolio, PortfolioRequest, Strategy, UserResponse, StockInfo
from assessment_app.models.db_models import User as DBUser
from assessment_app.service.auth_service import get_current_user_from_request
from assessment_app.repository.database import get_db
from assessment_app.repository.portfolio_repository import PortfolioRepository
from assessment_app.repository.strategy_repository import StrategyRepository
from assessment_app.repository.user_repository import UserRepository
import pandas as pd
import os
from pydantic import BaseModel

router = APIRouter()


def get_stock_price_at_timestamp(stock_symbol: str, timestamp: datetime) -> float:
    """Get stock price at a specific timestamp"""
    file_path = f"assessment_app/data/{stock_symbol}.csv"
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock data not found for {stock_symbol}"
        )

    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Date'] == timestamp.date()]

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for {stock_symbol} at {timestamp}"
        )

    # Return the average of Open and Close prices
    return (df.iloc[0]['Open'] + df.iloc[0]['Close']) / 2


@router.get("/strategies", response_model=List[Strategy])
async def get_strategies(
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> List[Strategy]:
    """
    Get all strategies available.
    """
    strategy_repo = StrategyRepository(db)
    return strategy_repo.get_all_strategies()


@router.post("/strategies", response_model=Strategy)
async def create_strategy(
        strategy: Strategy,
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> Strategy:
    """
    Create a new trading strategy.
    """
    strategy_repo = StrategyRepository(db)
    return strategy_repo.create_strategy(strategy)


@router.post("/portfolio", response_model=Portfolio)
async def create_portfolio(
        portfolio_data: PortfolioRequest,
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> Portfolio:
    """
    Create a new portfolio for the current user.
    """
    try:
        user_repo = UserRepository(db)
        user = user_repo.get_user_by_id(current_user_id)

        if not user:
            # Create test user if it doesn't exist
            new_user = DBUser(
                id=current_user_id,
                username=f"test_user_{current_user_id[:8]}",  # Use a unique username based on user ID
                email=f"test_{current_user_id[:8]}@example.com",
                hashed_password="test_password"
            )
            try:
                user = user_repo.create_user(new_user)
            except Exception as e:
                # If user creation fails (e.g., user already exists), try to get it again
                db.rollback()  # Rollback the session
                user = user_repo.get_user_by_id(current_user_id)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to create or retrieve user"
                    )

        portfolio_repo = PortfolioRepository(db)
        existing_portfolio = portfolio_repo.get_portfolio(current_user_id)

        if existing_portfolio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has a portfolio"
            )

        # Create new portfolio
        new_portfolio = Portfolio(
            id=str(uuid.uuid4()),
            user_id=current_user_id,
            cash_balance=portfolio_data.initial_capital,
            current_ts=datetime.now(),
            net_worth=portfolio_data.initial_capital,
            created_at=datetime.now()
        )

        saved_portfolio = portfolio_repo.create_portfolio(new_portfolio)
        return saved_portfolio
    except Exception as e:
        db.rollback()  # Rollback the session on any error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/portfolio/{portfolio_id}", response_model=Portfolio)
async def get_portfolio_by_id(
        portfolio_id: str,
        current_ts: datetime,
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> Portfolio:
    """
    Get specified portfolio for the current user.
    """
    portfolio_repo = PortfolioRepository(db)
    portfolio = portfolio_repo.get_portfolio_by_id(portfolio_id)

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

    # Update portfolio to current timestamp
    portfolio.current_ts = current_ts
    portfolio_repo.update_portfolio(portfolio)

    return portfolio


@router.delete("/portfolio/{portfolio_id}", response_model=Portfolio)
async def delete_portfolio(
        portfolio_id: str,
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> Portfolio:
    """
    Delete the specified portfolio for the current user.
    """
    portfolio_repo = PortfolioRepository(db)
    portfolio = portfolio_repo.get_portfolio_by_id(portfolio_id)

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    if portfolio.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this portfolio"
        )

    return portfolio_repo.delete_portfolio(portfolio_id)


@router.get("/portfolio-net-worth", response_model=dict)
async def get_net_worth(
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> dict:
    """
    Get net-worth from portfolio (holdings value and cash) at current_ts field in portfolio.
    """
    portfolio_repo = PortfolioRepository(db)
    portfolio = portfolio_repo.get_portfolio(current_user_id)

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    # Get all holdings
    holdings = portfolio_repo.get_all_holdings(current_user_id)

    # Calculate total holdings value
    total_holdings_value = 0.0
    for holding in holdings:
        try:
            current_price = get_stock_price_at_timestamp(holding.stock_symbol, portfolio.current_ts)
            total_holdings_value += holding.quantity * current_price
        except HTTPException:
            # If price data is not available, use the last known value
            total_holdings_value += holding.quantity * holding.average_price

    # Update portfolio net worth
    portfolio.net_worth = portfolio.cash_balance + total_holdings_value
    portfolio_repo.update_portfolio(portfolio)

    return {
        "net_worth": portfolio.net_worth,
        "cash_balance": portfolio.cash_balance,
        "holdings": holdings
    }


@router.get("/stocks", response_model=List[StockInfo])
async def get_all_stocks() -> List[StockInfo]:
    """
    Get list of all registered stocks with their latest prices.
    """
    stocks = []
    available_stocks = [f.replace('.csv', '') for f in os.listdir('assessment_app/data') if f.endswith('.csv')]

    for stock in available_stocks:
        try:
            # Read the CSV file and get the latest data
            file_path = f"assessment_app/data/{stock}.csv"
            df = pd.read_csv(file_path)
            df['Date'] = pd.to_datetime(df['Date'])
            latest_data = df.iloc[-1]  # Get the last row (most recent data)

            # Calculate average price
            current_price = (latest_data['Open'] + latest_data['Close']) / 2

            stock_info = StockInfo(
                stock_symbol=stock,
                name=stock,  # Using symbol as name for simplicity
                current_price=current_price
            )
            stocks.append(stock_info)
        except Exception as e:
            # Add stock even if current price is not available
            stock_info = StockInfo(
                stock_symbol=stock,
                name=stock,
                current_price=None
            )
            stocks.append(stock_info)

    return stocks


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
        db: Session = Depends(get_db)
) -> List[UserResponse]:
    """
    Get all users.
    """
    user_repo = UserRepository(db)
    users = user_repo.get_all_users()
    return [UserResponse.from_orm(user) for user in users]


@router.get("/portfolios", response_model=List[Portfolio])
async def get_all_portfolios(
        db: Session = Depends(get_db)
) -> List[Portfolio]:
    """
    Get list of all portfolios.
    """
    portfolio_repo = PortfolioRepository(db)
    return portfolio_repo.get_all_portfolios()


class TimestampUpdateRequest(BaseModel):
    new_ts: datetime


@router.put("/portfolio/{portfolio_id}/timestamp", response_model=Portfolio)
async def update_portfolio_timestamp(
        portfolio_id: str,
        request: TimestampUpdateRequest,
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> Portfolio:
    """
    Update portfolio timestamp.
    """
    portfolio_repo = PortfolioRepository(db)
    portfolio = portfolio_repo.get_portfolio_by_id(portfolio_id)

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    if portfolio.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this portfolio"
        )

    # Update portfolio timestamp
    portfolio.current_ts = request.new_ts
    updated_portfolio = portfolio_repo.update_portfolio(portfolio)

    return updated_portfolio
