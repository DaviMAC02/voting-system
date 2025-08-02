from typing import List, Optional, Tuple
from app.modules.features.interfaces.feature_repository import FeatureRepository
from app.modules.features.models import Feature
from app.modules.features.schemas import FeatureCreate, FeatureUpdate


class FeatureService:
    def __init__(self, feature_repository: FeatureRepository):
        self.feature_repository = feature_repository

    def create_feature(self, feature_data: FeatureCreate, user_id: int) -> Feature:
        feature = Feature(
            title=feature_data.title,
            description=feature_data.description,
            category=feature_data.category,
            user_id=user_id,
        )
        return self.feature_repository.create(feature)

    def get_feature(self, feature_id: int) -> Optional[Feature]:
        return self.feature_repository.get_by_id(feature_id)

    def get_all_features(self) -> List[Tuple[Feature, int]]:
        return self.feature_repository.get_features_with_vote_count()

    def update_feature_status(
        self, feature_id: int, update_data: FeatureUpdate
    ) -> Optional[Feature]:
        feature = self.get_feature(feature_id)
        if feature:
            feature.status = update_data.status
            return self.feature_repository.update(feature)
        return None
