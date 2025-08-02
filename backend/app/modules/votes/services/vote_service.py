from typing import Optional
from app.modules.votes.interfaces.vote_repository import VoteRepository
from app.modules.votes.models import Vote
from app.modules.votes.schemas import VoteCreate, VoteType


class VoteService:
    def __init__(self, vote_repository: VoteRepository):
        self.vote_repository = vote_repository

    def toggle_vote(self, vote_data: VoteCreate, user_id: int) -> Vote:
        existing_vote = self.vote_repository.get_by_user_and_feature(
            user_id, vote_data.feature_id
        )

        if existing_vote:
            if existing_vote.vote_type == vote_data.vote_type:
                # Remove vote if same type
                self.vote_repository.delete(existing_vote.id)
                return None
            else:
                # Update vote type if different
                existing_vote.vote_type = vote_data.vote_type
                return self.vote_repository.update(existing_vote)
        else:
            # Create new vote
            vote = Vote(
                feature_id=vote_data.feature_id,
                user_id=user_id,
                vote_type=vote_data.vote_type,
            )
            return self.vote_repository.create(vote)

    def get_vote_count(self, feature_id: int) -> int:
        return self.vote_repository.get_vote_count_for_feature(feature_id)

    def get_user_vote(self, feature_id: int, user_id: int) -> Optional[Vote]:
        return self.vote_repository.get_by_user_and_feature(user_id, feature_id)
