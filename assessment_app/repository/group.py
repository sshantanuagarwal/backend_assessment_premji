from typing import List
from sqlalchemy.orm import Session
from assessment_app.models.models import Group as PydanticGroup
from assessment_app.models.db_models import Group as DBGroup


class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_group(self, group_id: str) -> PydanticGroup:
        db_group = self.db.query(DBGroup).filter(DBGroup.id == group_id).first()
        return PydanticGroup(
            id=db_group.id,
            name=db_group.name
        )

    def get_all_groups(self) -> List[PydanticGroup]:
        db_strategies = self.db.query(DBGroup).all()
        return [
            PydanticGroup(
                id=group.id,
                name=group.name
            )
            for group in db_strategies
        ]

    def create_group(self, group: PydanticGroup) -> PydanticGroup:
        db_group = DBGroup(
            id=group.id,
            name=group.name
        )
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)
        return PydanticGroup(
            id=db_group.id,
            name=db_group.name,
        )
