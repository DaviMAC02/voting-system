from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class VoteType(str, Enum):
    UP = "up"
    DOWN = "down"


class VoteCreate(BaseModel):
    feature_id: int
    vote_type: VoteType


class VoteResponse(VoteCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
