from datetime import datetime
from typing import List
import pandas as pd
import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from assessment_app.models.models import TickData, Trade, TradeType, Portfolio, PortfolioHolding, StockInfo
from assessment_app.models.db_models import Trade as DBTrade, Portfolio as DBPortfolio, \
    PortfolioHolding as DBPortfolioHolding
from assessment_app.service.auth_service import get_current_user_from_request
from assessment_app.repository.database import get_db
from assessment_app.repository.trade_repository import TradeRepository
from assessment_app.repository.portfolio_repository import PortfolioRepository
from assessment_app.models.constants import StockSymbols

router = APIRouter()


class MarketDataRequest(BaseModel):
    stock_symbol: str
    current_ts: datetime


class MarketDataRangeRequest(BaseModel):
    stock_symbol: str
    from_ts: datetime
    to_ts: datetime


class TradeRequest(BaseModel):
    stock_symbol: str
    quantity: int
    price: float
    trade_type: TradeType
    execution_ts: datetime


def get_stock_data(stock_symbol: str, timestamp: datetime) -> pd.DataFrame:
    """Load and filter stock data from CSV file"""
    file_path = f"assessment_app/data/{stock_symbol}.csv"
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock data not found for {stock_symbol}"
        )

    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    # Filter by date component only
    target_date = timestamp.date()
    df = df[df['Date'].dt.date == target_date]
    return df


def get_stock_data_range(stock_symbol: str, from_ts: datetime, to_ts: datetime) -> pd.DataFrame:
    """Load and filter stock data for a date range"""
    file_path = f"assessment_app/data/{stock_symbol}.csv"
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock data not found for {stock_symbol}"
        )

    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    # Filter by date component only
    from_date = from_ts.date()
    to_date = to_ts.date()
    return df[(df['Date'].dt.date >= from_date) & (df['Date'].dt.date <= to_date)]


@router.post("/market/data/tick", response_model=TickData)
async def get_market_data_tick(
        request: MarketDataRequest,
        db: Session = Depends(get_db)
) -> TickData:
    """
    Get data for stocks for a given datetime from `data` folder.
    """
    if request.stock_symbol not in [s.value for s in StockSymbols]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stock symbol. Valid symbols are: {[s.value for s in StockSymbols]}"
        )

    df = get_stock_data(request.stock_symbol, request.current_ts)
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for {request.stock_symbol} at {request.current_ts}"
        )

    row = df.iloc[0]
    return TickData(
        stock_symbol=request.stock_symbol,
        timestamp=request.current_ts,
        price=(row['Open'] + row['Close']) / 2,
        open_price=row['Open'],
        high_price=row['High'],
        low_price=row['Low'],
        close_price=row['Close'],
        volume=row['Volume']
    )


@router.post("/market/data/range", response_model=List[TickData])
async def get_market_data_range(
        request: MarketDataRangeRequest,
        db: Session = Depends(get_db)
) -> List[TickData]:
    """
    Get data for stocks for a given datetime range from `data` folder.
    """
    if request.stock_symbol not in [s.value for s in StockSymbols]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stock symbol. Valid symbols are: {[s.value for s in StockSymbols]}"
        )

    df = get_stock_data_range(request.stock_symbol, request.from_ts, request.to_ts)
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for {request.stock_symbol} between {request.from_ts} and {request.to_ts}"
        )

    return [
        TickData(
            stock_symbol=request.stock_symbol,
            timestamp=row['Date'],
            price=(row['Open'] + row['Close']) / 2,
            open_price=row['Open'],
            high_price=row['High'],
            low_price=row['Low'],
            close_price=row['Close'],
            volume=row['Volume']
        )
        for _, row in df.iterrows()
    ]


@router.post("/market/trade", response_model=Trade)
async def trade_stock(
        trade_request: TradeRequest,
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> Trade:
    """
    Execute a trade if price is within valid range and update portfolio.
    """
    # Validate stock symbol
    if trade_request.stock_symbol not in [s.value for s in StockSymbols]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stock symbol. Valid symbols are: {[s.value for s in StockSymbols]}"
        )

    # Get market data for trade timestamp
    df = get_stock_data(trade_request.stock_symbol, trade_request.execution_ts)
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No market data found for {trade_request.stock_symbol} at {trade_request.execution_ts}"
        )

    row = df.iloc[0]
    avg_price = (row['Open'] + row['Close']) / 2

    # Validate trade price
    if trade_request.price != avg_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Trade price must be equal to average price: {avg_price}"
        )

    # Get user's portfolio
    portfolio_repo = PortfolioRepository(db)
    portfolio = portfolio_repo.get_portfolio(current_user_id)

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    # Validate trade timestamp
    if trade_request.execution_ts < portfolio.current_ts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot execute trade in the past"
        )

    # Calculate trade value
    trade_value = trade_request.price * trade_request.quantity

    # Validate trade based on type
    if trade_request.trade_type == "BUY":
        if portfolio.cash_balance < trade_value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient funds"
            )
        portfolio.cash_balance -= trade_value
    else:  # SELL
        # Check if user has enough shares
        holdings = portfolio_repo.get_holdings(current_user_id, trade_request.stock_symbol)
        if not holdings or holdings.quantity < trade_request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient shares"
            )
        portfolio.cash_balance += trade_value

    # Update portfolio
    portfolio.current_ts = trade_request.execution_ts
    portfolio_repo.update_portfolio(portfolio)

    # Get or create portfolio holding
    holding = portfolio_repo.get_holdings(current_user_id, trade_request.stock_symbol)
    if trade_request.trade_type == "BUY":
        if holding:
            # Update existing holding
            total_value = holding.quantity * holding.average_price + trade_value
            total_quantity = holding.quantity + trade_request.quantity
            new_average_price = total_value / total_quantity
            holding.quantity = total_quantity
            holding.average_price = new_average_price
            holding.current_value = total_quantity * trade_request.price
        else:
            # Create new holding
            holding = DBPortfolioHolding(
                id=str(uuid.uuid4()),
                portfolio_id=portfolio.id,
                stock_symbol=trade_request.stock_symbol,
                quantity=trade_request.quantity,
                average_price=trade_request.price,
                current_value=trade_value
            )
            db.add(holding)
    else:  # SELL
        # Update existing holding
        holding.quantity -= trade_request.quantity
        if holding.quantity == 0:
            # Remove holding if no shares left
            db.delete(holding)
        else:
            # Update current value
            holding.current_value = holding.quantity * trade_request.price

    # Create trade object
    db_trade = DBTrade(
        id=str(uuid.uuid4()),
        user_id=current_user_id,
        stock_symbol=trade_request.stock_symbol,
        quantity=trade_request.quantity,
        price=trade_request.price,
        trade_type=trade_request.trade_type,
        execution_ts=trade_request.execution_ts,
        created_at=datetime.now()
    )

    # Save trade and commit all changes
    trade_repo = TradeRepository(db)
    saved_trade = trade_repo.create_trade(db_trade)

    # Convert to Pydantic model for response
    return Trade(
        id=saved_trade.id,
        user_id=saved_trade.user_id,
        stock_symbol=saved_trade.stock_symbol,
        quantity=saved_trade.quantity,
        price=saved_trade.price,
        trade_type=saved_trade.trade_type,
        execution_ts=saved_trade.execution_ts,
        created_at=saved_trade.created_at
    )


@router.get("/stocks")
async def get_stocks():
    """
    Lists all registered stocks with their current prices.
    """
    stocks = []
    for stock_symbol in [s.value for s in StockSymbols]:
        file_path = f"assessment_app/data/{stock_symbol}.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['Date'] = pd.to_datetime(df['Date'])
            latest_data = df.iloc[-1]
            current_price = (latest_data['Open'] + latest_data['Close']) / 2
            stocks.append(StockInfo(
                stock_symbol=stock_symbol,
                name=stock_symbol,  # Using symbol as name for simplicity
                current_price=current_price
            ))
        else:
            stocks.append(StockInfo(
                stock_symbol=stock_symbol,
                name=stock_symbol,
                current_price=None
            ))
    return stocks


@router.get("/market-data/{stock_symbol}", response_model=dict)
async def get_market_data(
        stock_symbol: str,
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> dict:
    # Implementation of the new endpoint
    pass


@router.get("/stocks", response_model=List[StockInfo])
async def get_all_stocks(
        current_user_id: str = Depends(get_current_user_from_request),
        db: Session = Depends(get_db)
) -> List[StockInfo]:
    # Implementation of the new endpoint
    pass
