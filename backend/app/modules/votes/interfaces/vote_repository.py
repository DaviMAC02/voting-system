from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.votes.models import Vote
from app.shared.interfaces.repository import Repository


class VoteRepository(Repository):
    @abstractmethod
    def get_by_user_and_feature(self, user_id: int, feature_id: int) -> Optional[Vote]:
        pass

    @abstractmethod
    def get_vote_count_for_feature(self, feature_id: int) -> int:
        pass
