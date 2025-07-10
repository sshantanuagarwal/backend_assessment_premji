import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

from pydantic import BaseModel, Field, EmailStr

from assessment_app.models.constants import TradeType


class RegisterUserRequest(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class PortfolioRequest(BaseModel):
    initial_capital: float


class Portfolio(BaseModel):
    id: str
    user_id: str
    cash_balance: float
    current_ts: datetime
    net_worth: float
    created_at: datetime


class Strategy(BaseModel):
    id: str
    user_id: str
    portfolio_id: str
    name: str
    description: str
    parameters: Dict[str, Any]
    created_at: datetime


class Trade(BaseModel):
    id: str
    user_id: str
    stock_symbol: str
    quantity: int
    price: float
    trade_type: str
    execution_ts: datetime
    created_at: datetime


class TickData(BaseModel):
    stock_symbol: str
    timestamp: datetime
    price: float
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int


class PortfolioHolding(BaseModel):
    stock_symbol: str
    quantity: int
    average_price: float
    current_value: float


class PortfolioAnalysis(BaseModel):
    total_investment: float
    current_value: float
    returns: float
    returns_percentage: float
    holdings: List[PortfolioHolding]


class BacktestRequest(BaseModel):
    strategy_id: str
    portfolio_id: str
    start_date: datetime
    end_date: datetime
    initial_capital: float


class BacktestResponse(BaseModel):
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float
    trades: List[Trade]
    profit_loss: float
    annualized_return: float


class StockInfo(BaseModel):
    stock_symbol: str
    name: str
    current_price: Optional[float] = None


class Group(BaseModel):
    id: str
    name: str


class Task(BaseModel):
    id: Optional[str]
    group_id: str
    name: str
    start_date: datetime
    end_date: datetime
    estimated_effort: float
    weekdays: List[int]
