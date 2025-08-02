from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.shared.models import Base
from app.modules.features.schemas import FeatureCategory, FeatureStatus


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    category = Column(Enum(FeatureCategory), nullable=False)
    status = Column(Enum(FeatureStatus), nullable=False, default=FeatureStatus.OPEN)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", backref="features")
    votes = relationship("Vote", backref="feature", cascade="all, delete-orphan")
