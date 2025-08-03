from sqlalchemy import func, case
from typing import List, Optional
from app.modules.votes.models import Vote
from app.modules.votes.interfaces.vote_repository import VoteRepository
from app.shared.database import db


class SQLAlchemyVoteRepository(VoteRepository):
    def get_by_id(self, id: int) -> Optional[Vote]:
        return Vote.query.filter(Vote.id == id).first()

    def get_all(self) -> List[Vote]:
        return Vote.query.all()

    def create(self, vote: Vote) -> Vote:
        db.session.add(vote)
        db.session.commit()
        return vote

    def update(self, vote: Vote) -> Vote:
        db.session.merge(vote)
        db.session.commit()
        return vote

    def delete(self, id: int) -> bool:
        vote = self.get_by_id(id)
        if vote:
            db.session.delete(vote)
            db.session.commit()
            return True
        return False

    def get_by_user_and_feature(self, user_id: int, feature_id: int) -> Optional[Vote]:
        return Vote.query.filter(
            Vote.user_id == user_id, Vote.feature_id == feature_id
        ).first()

    def get_vote_count_for_feature(self, feature_id: int) -> int:
        result = (
            db.session.query(func.count())
            .filter(Vote.feature_id == feature_id)
            .scalar()
        )
        return result or 0

    def get_by_user(self, user_id: int) -> List[Vote]:
        """Get all votes for a specific user"""
        return Vote.query.filter(Vote.user_id == user_id).all()
