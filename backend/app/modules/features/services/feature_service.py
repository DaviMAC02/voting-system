from typing import List, Optional, Tuple
from app.modules.features.interfaces.feature_repository import FeatureRepository
from app.modules.features.models import Feature, FeatureCategory


class FeatureService:
    def __init__(self, feature_repository: FeatureRepository):
        self.feature_repository = feature_repository

    def create_feature(
        self,
        title: str,
        description: str,
        category: FeatureCategory,
        created_by_id: int,
    ) -> Feature:
        existing_feature = self.feature_repository.get_by_title(title)
        if existing_feature:
            raise ValueError("A feature with this title already exists")

        feature = Feature(
            title=title,
            description=description,
            category=category,
            user_id=created_by_id,
        )
        return self.feature_repository.create(feature)

    def get_feature_by_id(self, feature_id: int) -> Optional[Feature]:
        features_with_votes = self.feature_repository.get_features_with_vote_count()
        for feature, vote_count in features_with_votes:
            if feature.id == feature_id:
                feature.like_count = vote_count
                return feature
        return None

    def get_features(self) -> List[Feature]:
        features_with_votes = self.feature_repository.get_features_with_vote_count()
        # Combine vote counts with features
        for feature, vote_count in features_with_votes:
            feature.like_count = vote_count
        return [feature for feature, _ in features_with_votes]

    def update_feature(
        self,
        feature_id: int,
        title: str,
        description: str,
        category: FeatureCategory,
        user_id: int,
    ) -> Optional[Feature]:
        feature = self.get_feature_by_id(feature_id)
        if not feature:
            raise ValueError("Feature not found")

        if feature.user_id != user_id:
            raise ValueError("Not authorized to update this feature")

        feature.title = title
        feature.description = description
        feature.category = category

        return self.feature_repository.update(feature)

    def delete_feature(self, feature_id: int, user_id: int) -> bool:
        feature = self.get_feature_by_id(feature_id)
        if not feature:
            raise ValueError("Feature not found")

        if feature.user_id != user_id:
            raise ValueError("Not authorized to delete this feature")

        return self.feature_repository.delete(feature_id)
