from datetime import datetime
import uuid

from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from assessment_app.models.base import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    portfolio = relationship("Portfolio", back_populates="user", uselist=False)
    trades = relationship("Trade", back_populates="user")


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    cash_balance = Column(Float, nullable=False)
    current_ts = Column(DateTime, nullable=False)
    net_worth = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="portfolio")
    holdings = relationship("PortfolioHolding", back_populates="portfolio")


class PortfolioHolding(Base):
    __tablename__ = "portfolio_holdings"

    id = Column(String, primary_key=True, default=generate_uuid)
    portfolio_id = Column(String, ForeignKey("portfolios.id"), nullable=False)
    stock_symbol = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    average_price = Column(Float, nullable=False)
    current_value = Column(Float, nullable=False)

    portfolio = relationship("Portfolio", back_populates="holdings")


class Trade(Base):
    __tablename__ = "trades"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    stock_symbol = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    trade_type = Column(String, nullable=False)
    execution_ts = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="trades")


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    parameters = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class Group(Base):
    __tablename__ = "group"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)


class Task(Base):
    __tablename__ = "task"

    id = Column(String, primary_key=True, default=generate_uuid)
    group_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    estimated_effort = Column(Float, nullable=False)
    weekdays = Column(JSON, nullable=False)
