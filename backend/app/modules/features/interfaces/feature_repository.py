from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.features.models import Feature
from app.shared.interfaces.repository import Repository


class FeatureRepository(Repository):
    @abstractmethod
    def get_all_sorted_by_date(self) -> List[Feature]:
        pass

    @abstractmethod
    def get_features_with_vote_count(self) -> List[tuple[Feature, int]]:
        pass
