from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.shared.models import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    name = Column(String(80), nullable=False)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
