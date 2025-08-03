from typing import Optional
from app.modules.votes.interfaces.vote_repository import VoteRepository
from app.modules.votes.models import Vote
from app.modules.votes.schemas import VoteCreate
from app.modules.features.services.feature_service import FeatureService
from app.modules.features.repositories.sqlalchemy_feature_repository import (
    SQLAlchemyFeatureRepository,
)


class VoteService:
    def __init__(self, vote_repository: VoteRepository):
        self.vote_repository = vote_repository
        self.feature_service = FeatureService(SQLAlchemyFeatureRepository())

    def toggle_vote(self, vote_data: VoteCreate, user_id: int) -> Optional[Vote]:
        # Check if feature exists
        feature = self.feature_service.get_feature_by_id(vote_data.feature_id)
        if not feature:
            raise ValueError("Feature not found")

        existing_vote = self.vote_repository.get_by_user_and_feature(
            user_id, vote_data.feature_id
        )

        if existing_vote:
            self.vote_repository.delete(existing_vote.id)
            return None

        vote = Vote(
            feature_id=vote_data.feature_id,
            user_id=user_id,
        )
        return self.vote_repository.create(vote)

    def get_vote_count(self, feature_id: int) -> int:
        return self.vote_repository.get_vote_count_for_feature(feature_id)

    def get_user_vote(self, feature_id: int, user_id: int) -> Optional[Vote]:
        return self.vote_repository.get_by_user_and_feature(user_id, feature_id)

    def get_user_votes(self, user_id: int) -> list[Vote]:
        """Get all votes for a specific user"""
        return self.vote_repository.get_votes_by_user(user_id)

    def get_all_votes(self) -> list[Vote]:
        """Get all votes"""
        return self.vote_repository.get_all()
        return self.vote_repository.get_by_user(user_id)
