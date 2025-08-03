from pydantic import BaseModel
from datetime import datetime


class VoteCreate(BaseModel):
    feature_id: int


class VoteResponse(VoteCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
