from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class FeatureCategory(str, Enum):
    BUG = "Bug"
    FEATURE = "Feature"
    ENHANCEMENT = "Enhancement"


class FeatureStatus(str, Enum):
    OPEN = "Open"
    CLOSED = "Closed"


class FeatureBase(BaseModel):
    title: str
    description: str
    category: FeatureCategory


class FeatureCreate(FeatureBase):
    pass


class FeatureUpdate(BaseModel):
    status: FeatureStatus


class FeatureResponse(FeatureBase):
    id: int
    status: FeatureStatus
    created_at: datetime
    user_id: int
    vote_count: int = 0

    class Config:
        orm_mode = True
