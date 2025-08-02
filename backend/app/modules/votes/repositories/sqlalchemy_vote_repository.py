from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.modules.votes.models import Vote
from app.modules.votes.interfaces.vote_repository import VoteRepository
from app.shared.database import db_session


class SQLAlchemyVoteRepository(VoteRepository):
    def __init__(self, session: Session = db_session):
        self.session = session

    def get_by_id(self, id: int) -> Optional[Vote]:
        return self.session.query(Vote).filter(Vote.id == id).first()

    def get_all(self) -> List[Vote]:
        return self.session.query(Vote).all()

    def create(self, vote: Vote) -> Vote:
        self.session.add(vote)
        self.session.commit()
        return vote

    def update(self, vote: Vote) -> Vote:
        self.session.merge(vote)
        self.session.commit()
        return vote

    def delete(self, id: int) -> bool:
        vote = self.get_by_id(id)
        if vote:
            self.session.delete(vote)
            self.session.commit()
            return True
        return False

    def get_by_user_and_feature(self, user_id: int, feature_id: int) -> Optional[Vote]:
        return (
            self.session.query(Vote)
            .filter(Vote.user_id == user_id, Vote.feature_id == feature_id)
            .first()
        )

    def get_vote_count_for_feature(self, feature_id: int) -> int:
        result = (
            self.session.query(
                func.sum(func.case([(Vote.vote_type == "up", 1)], else_=-1))
            )
            .filter(Vote.feature_id == feature_id)
            .scalar()
        )
        return result or 0
