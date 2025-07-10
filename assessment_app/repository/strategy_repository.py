from typing import List
from sqlalchemy.orm import Session
from assessment_app.models.models import Strategy as PydanticStrategy
from assessment_app.models.db_models import Strategy as DBStrategy

class StrategyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_strategy(self, strategy_id: str) -> PydanticStrategy:
        db_strategy = self.db.query(DBStrategy).filter(DBStrategy.id == strategy_id).first()
        if not db_strategy:
            return None
        return PydanticStrategy(
            id=db_strategy.id,
            name=db_strategy.name,
            description=db_strategy.description,
            parameters=db_strategy.parameters,
            created_at=db_strategy.created_at
        )

    def get_all_strategies(self) -> List[PydanticStrategy]:
        db_strategies = self.db.query(DBStrategy).all()
        return [
            PydanticStrategy(
                id=strategy.id,
                name=strategy.name,
                description=strategy.description,
                parameters=strategy.parameters,
                created_at=strategy.created_at
            )
            for strategy in db_strategies
        ]

    def create_strategy(self, strategy: PydanticStrategy) -> PydanticStrategy:
        db_strategy = DBStrategy(
            id=strategy.id,
            name=strategy.name,
            description=strategy.description,
            parameters=strategy.parameters,
            created_at=strategy.created_at
        )
        self.db.add(db_strategy)
        self.db.commit()
        self.db.refresh(db_strategy)
        return PydanticStrategy(
            id=db_strategy.id,
            name=db_strategy.name,
            description=db_strategy.description,
            parameters=db_strategy.parameters,
            created_at=db_strategy.created_at
        )

    def update_strategy(self, strategy: PydanticStrategy) -> PydanticStrategy:
        db_strategy = self.db.query(DBStrategy).filter(DBStrategy.id == strategy.id).first()
        if not db_strategy:
            return None
        db_strategy.name = strategy.name
        db_strategy.description = strategy.description
        db_strategy.parameters = strategy.parameters
        self.db.commit()
        self.db.refresh(db_strategy)
        return PydanticStrategy(
            id=db_strategy.id,
            name=db_strategy.name,
            description=db_strategy.description,
            parameters=db_strategy.parameters,
            created_at=db_strategy.created_at
        )

    def delete_strategy(self, strategy: PydanticStrategy) -> None:
        db_strategy = self.db.query(DBStrategy).filter(DBStrategy.id == strategy.id).first()
        if db_strategy:
            self.db.delete(db_strategy)
            self.db.commit()

    def get_strategy_stocks(self, strategy_id: str) -> List[str]:
        strategy = self.get_strategy(strategy_id)
        if not strategy:
            return []
        return strategy.parameters.get("stocks", []) 