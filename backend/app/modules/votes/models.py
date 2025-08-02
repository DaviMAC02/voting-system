from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.shared.models import Base
from app.modules.votes.schemas import VoteType


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True)
    feature_id = Column(Integer, ForeignKey("features.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vote_type = Column(Enum(VoteType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="votes")

    __table_args__ = (
        # Ensure one vote per user per feature
        UniqueConstraint("user_id", "feature_id", name="uix_user_feature"),
    )
