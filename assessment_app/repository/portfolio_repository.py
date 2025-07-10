from typing import List, Optional
from sqlalchemy.orm import Session
from assessment_app.models.models import Portfolio as PydanticPortfolio
from assessment_app.models.db_models import Portfolio as DBPortfolio
from assessment_app.models.models import PortfolioHolding
from assessment_app.models.db_models import PortfolioHolding as DBPortfolioHolding

class PortfolioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_portfolio(self, user_id: str) -> PydanticPortfolio:
        db_portfolio = self.db.query(DBPortfolio).filter(DBPortfolio.user_id == user_id).first()
        if not db_portfolio:
            return None
        return PydanticPortfolio(
            id=db_portfolio.id,
            user_id=db_portfolio.user_id,
            cash_balance=db_portfolio.cash_balance,
            current_ts=db_portfolio.current_ts,
            net_worth=db_portfolio.net_worth,
            created_at=db_portfolio.created_at
        )

    def get_portfolio_by_id(self, portfolio_id: str) -> Optional[PydanticPortfolio]:
        db_portfolio = self.db.query(DBPortfolio).filter(DBPortfolio.id == portfolio_id).first()
        if not db_portfolio:
            return None
        return PydanticPortfolio(
            id=db_portfolio.id,
            user_id=db_portfolio.user_id,
            cash_balance=db_portfolio.cash_balance,
            current_ts=db_portfolio.current_ts,
            net_worth=db_portfolio.net_worth,
            created_at=db_portfolio.created_at
        )

    def create_portfolio(self, portfolio: PydanticPortfolio) -> PydanticPortfolio:
        db_portfolio = DBPortfolio(
            id=portfolio.id,
            user_id=portfolio.user_id,
            cash_balance=portfolio.cash_balance,
            current_ts=portfolio.current_ts,
            net_worth=portfolio.net_worth,
            created_at=portfolio.created_at
        )
        self.db.add(db_portfolio)
        self.db.commit()
        self.db.refresh(db_portfolio)
        return PydanticPortfolio(
            id=db_portfolio.id,
            user_id=db_portfolio.user_id,
            cash_balance=db_portfolio.cash_balance,
            current_ts=db_portfolio.current_ts,
            net_worth=db_portfolio.net_worth,
            created_at=db_portfolio.created_at
        )

    def update_portfolio(self, portfolio: PydanticPortfolio) -> PydanticPortfolio:
        db_portfolio = self.db.query(DBPortfolio).filter(DBPortfolio.user_id == portfolio.user_id).first()
        if not db_portfolio:
            return None
        db_portfolio.cash_balance = portfolio.cash_balance
        db_portfolio.current_ts = portfolio.current_ts
        db_portfolio.net_worth = portfolio.net_worth
        self.db.commit()
        self.db.refresh(db_portfolio)
        return PydanticPortfolio(
            id=db_portfolio.id,
            user_id=db_portfolio.user_id,
            cash_balance=db_portfolio.cash_balance,
            current_ts=db_portfolio.current_ts,
            net_worth=db_portfolio.net_worth,
            created_at=db_portfolio.created_at
        )

    def delete_portfolio(self, user_id: str) -> None:
        db_portfolio = self.db.query(DBPortfolio).filter(DBPortfolio.user_id == user_id).first()
        if db_portfolio:
            self.db.delete(db_portfolio)
            self.db.commit()

    def get_holdings(self, user_id: str, stock_symbol: str) -> Optional[PortfolioHolding]:
        portfolio = self.get_portfolio(user_id)
        if not portfolio:
            return None
        
        db_holding = self.db.query(DBPortfolioHolding).join(DBPortfolio).filter(
            DBPortfolio.user_id == user_id,
            DBPortfolioHolding.stock_symbol == stock_symbol
        ).first()
        
        if not db_holding:
            return None
        
        return PortfolioHolding(
            stock_symbol=db_holding.stock_symbol,
            quantity=db_holding.quantity,
            average_price=db_holding.average_price,
            current_value=db_holding.current_value
        )

    def get_all_holdings(self, user_id: str) -> List[PortfolioHolding]:
        portfolio = self.get_portfolio(user_id)
        if not portfolio:
            return []
        
        db_holdings = self.db.query(DBPortfolioHolding).join(DBPortfolio).filter(
            DBPortfolio.user_id == user_id
        ).all()
        
        return [
            PortfolioHolding(
                stock_symbol=holding.stock_symbol,
                quantity=holding.quantity,
                average_price=holding.average_price,
                current_value=holding.current_value
            )
            for holding in db_holdings
        ]

    def get_all_portfolios(self) -> List[PydanticPortfolio]:
        """Get all portfolios"""
        db_portfolios = self.db.query(DBPortfolio).all()
        return [
            PydanticPortfolio(
                id=portfolio.id,
                user_id=portfolio.user_id,
                cash_balance=portfolio.cash_balance,
                current_ts=portfolio.current_ts,
                net_worth=portfolio.net_worth,
                created_at=portfolio.created_at
            )
            for portfolio in db_portfolios
        ] 