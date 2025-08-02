from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from app.modules.features.models import Feature
from app.modules.votes.models import Vote
from app.modules.features.interfaces.feature_repository import FeatureRepository
from app.shared.database import db_session


class SQLAlchemyFeatureRepository(FeatureRepository):
    def __init__(self, session: Session = db_session):
        self.session = session

    def get_by_id(self, id: int) -> Optional[Feature]:
        return self.session.query(Feature).filter(Feature.id == id).first()

    def get_all(self) -> List[Feature]:
        return self.session.query(Feature).all()

    def get_all_sorted_by_date(self) -> List[Feature]:
        return self.session.query(Feature).order_by(desc(Feature.created_at)).all()

    def get_features_with_vote_count(self) -> List[tuple[Feature, int]]:
        return (
            self.session.query(Feature, func.count(Vote.id).label("vote_count"))
            .outerjoin(Vote)
            .group_by(Feature.id)
            .order_by(desc(Feature.created_at))
            .all()
        )

    def create(self, feature: Feature) -> Feature:
        self.session.add(feature)
        self.session.commit()
        return feature

    def update(self, feature: Feature) -> Feature:
        self.session.merge(feature)
        self.session.commit()
        return feature

    def delete(self, id: int) -> bool:
        feature = self.get_by_id(id)
        if feature:
            self.session.delete(feature)
            self.session.commit()
            return True
        return False
