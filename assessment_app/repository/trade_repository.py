from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from assessment_app.models.db_models import Trade as DBTrade

class TradeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_trade(self, trade_id: str) -> Optional[DBTrade]:
        return self.db.query(DBTrade).filter(DBTrade.id == trade_id).first()

    def create_trade(self, trade: DBTrade) -> DBTrade:
        self.db.add(trade)
        self.db.commit()
        self.db.refresh(trade)
        return trade

    def get_user_trades(self, user_id: str) -> List[DBTrade]:
        return self.db.query(DBTrade).filter(DBTrade.user_id == user_id).all()

    def get_trades_by_stock(self, stock_symbol: str) -> List[DBTrade]:
        return self.db.query(DBTrade).filter(DBTrade.stock_symbol == stock_symbol).all()

    def get_trades_by_type(self, trade_type: str) -> List[DBTrade]:
        return self.db.query(DBTrade).filter(DBTrade.trade_type == trade_type).all()

    def get_trades_by_time_range(self, start_ts: datetime, end_ts: datetime) -> List[DBTrade]:
        return self.db.query(DBTrade).filter(
            DBTrade.execution_ts >= start_ts,
            DBTrade.execution_ts <= end_ts
        ).all()

    def delete_trade(self, trade_id: str) -> bool:
        trade = self.get_trade(trade_id)
        if trade:
            self.db.delete(trade)
            self.db.commit()
            return True
        return False 