from datetime import datetime
from typing import Dict, Any, List

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from assessment_app.models.constants import StockSymbols
from assessment_app.service.auth_service import get_current_user_from_request
from assessment_app.utils.utils import compute_cagr
from assessment_app.repository.database import get_db
from assessment_app.repository.portfolio_repository import PortfolioRepository
from assessment_app.repository.trade_repository import TradeRepository
from assessment_app.models.models import PortfolioAnalysis, PortfolioHolding
from assessment_app.service.analysis_service import AnalysisService
import pandas as pd
import os

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

    # Find the closest date to the requested timestamp
    target_date = timestamp.date()
    available_dates = df['Date'].dt.date.unique()

    if len(available_dates) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data available for {stock_symbol}"
        )

    # Find the closest date
    closest_date = min(available_dates, key=lambda x: abs((x - target_date).days))

    # Get data for the closest date
    df = df[df['Date'].dt.date == closest_date]

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for {stock_symbol} near {timestamp}"
        )

    # Return the average of Open and Close prices
    return (df.iloc[0]['Open'] + df.iloc[0]['Close']) / 2


@router.get("/analysis/estimate_returns/stock", response_model=dict)
async def get_stock_analysis(
        stock_symbol: str,
        start_ts: datetime,
        end_ts: datetime,
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> dict:
    """
    Estimate returns for given stock based on stock prices between the given timestamps.
    """
    if stock_symbol not in [s.value for s in StockSymbols]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stock symbol. Valid symbols are: {[s.value for s in StockSymbols]}"
        )

    try:
        start_price = get_stock_price_at_timestamp(stock_symbol, start_ts)
        end_price = get_stock_price_at_timestamp(stock_symbol, end_ts)

        if start_price <= 0 or end_price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid stock prices found"
            )

        cagr = compute_cagr(start_price, end_price, start_ts, end_ts)
        if cagr is None:
            cagr = 0.0  # Return 0% if CAGR calculation fails

        return {
            "returns": end_price - start_price,
            "returns_percentage": cagr * 100,  # Convert to percentage
            "start_price": start_price,
            "end_price": end_price
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/analysis/estimate_returns/portfolio", response_model=PortfolioAnalysis)
async def estimate_portfolio_returns(
        portfolio_id: str,
        start_ts: datetime,
        end_ts: datetime,
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> PortfolioAnalysis:
    """
    Estimate returns for a portfolio between start_ts and end_ts.
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

    # Get all holdings
    holdings = portfolio_repo.get_all_holdings(portfolio.user_id)

    # Calculate total investment and current value
    total_investment = 0.0
    current_value = 0.0
    holdings_list = []

    for holding in holdings:
        try:
            # Get start price
            start_price = get_stock_price_at_timestamp(holding.stock_symbol, start_ts)
            # Get end price
            end_price = get_stock_price_at_timestamp(holding.stock_symbol, end_ts)

            # Calculate values
            investment = holding.quantity * holding.average_price
            current_holding_value = holding.quantity * end_price

            total_investment += investment
            current_value += current_holding_value

            holdings_list.append(
                PortfolioHolding(
                    stock_symbol=holding.stock_symbol,
                    quantity=holding.quantity,
                    average_price=holding.average_price,
                    current_value=current_holding_value
                )
            )
        except HTTPException:
            # Skip stocks without data
            continue

    # Calculate returns
    returns = current_value - total_investment
    returns_percentage = (returns / total_investment) * 100 if total_investment > 0 else 0

    return PortfolioAnalysis(
        total_investment=total_investment,
        current_value=current_value,
        returns=returns,
        returns_percentage=returns_percentage,
        holdings=holdings_list
    )


@router.get("/portfolio-analysis", response_model=PortfolioAnalysis)
async def analyze_portfolio(
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> PortfolioAnalysis:
    """
    Analyze the current user's portfolio performance.
    """
    try:
        portfolio_repo = PortfolioRepository(db)
        portfolio = portfolio_repo.get_portfolio(current_user_id)

        if not portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found"
            )

        # Get all holdings
        holdings = portfolio_repo.get_all_holdings(current_user_id)

        # Initialize analysis service
        analysis_service = AnalysisService()

        # Perform analysis
        analysis = analysis_service.analyze_portfolio(portfolio, holdings)

        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/portfolio-returns", response_model=dict)
async def estimate_portfolio_returns(
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> dict:
    """
    Estimate potential returns for the current user's portfolio.
    """
    try:
        portfolio_repo = PortfolioRepository(db)
        portfolio = portfolio_repo.get_portfolio(current_user_id)

        if not portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found"
            )

        # Get all holdings
        holdings = portfolio_repo.get_all_holdings(portfolio.user_id)

        # Initialize analysis service
        analysis_service = AnalysisService()

        # Estimate returns
        estimated_returns = analysis_service.estimate_returns(portfolio, holdings)

        return {
            "portfolio_id": portfolio.id,
            "estimated_returns": estimated_returns
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
