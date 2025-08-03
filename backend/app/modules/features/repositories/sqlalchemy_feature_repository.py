from sqlalchemy import desc, func, case
from typing import List, Optional
from app.modules.features.models import Feature
from app.modules.votes.models import Vote
from app.modules.features.interfaces.feature_repository import FeatureRepository
from app.shared.database import db


class SQLAlchemyFeatureRepository(FeatureRepository):
    def get_by_id(self, id: int) -> Optional[Feature]:
        result = (
            db.session.query(Feature, func.count(Vote.id).label("vote_count"))
            .outerjoin(Vote)
            .filter(Feature.id == id)
            .group_by(Feature.id)
            .first()
        )
        if result:
            feature, vote_count = result
            feature.like_count = vote_count
            return feature
        return None

    def get_all(self) -> List[Feature]:
        return Feature.query.all()

    def get_all_sorted_by_date(self) -> List[Feature]:
        return Feature.query.order_by(desc(Feature.created_at)).all()

    def get_features_with_vote_count(self) -> List[tuple[Feature, int]]:
        return (
            db.session.query(
                Feature,
                func.count(Vote.id).label("vote_count"),
            )
            .outerjoin(Vote)
            .group_by(Feature.id)
            .order_by(desc(Feature.created_at))
            .all()
        )

    def get_by_title(self, title: str) -> Optional[Feature]:
        return Feature.query.filter(
            func.lower(Feature.title) == func.lower(title)
        ).first()

    def create(self, feature: Feature) -> Feature:
        db.session.add(feature)
        db.session.commit()
        return feature

    def update(self, feature: Feature) -> Feature:
        db.session.merge(feature)
        db.session.commit()
        return feature

    def delete(self, id: int) -> bool:
        feature = self.get_by_id(id)
        if feature:
            db.session.delete(feature)
            db.session.commit()
            return True
        return False
