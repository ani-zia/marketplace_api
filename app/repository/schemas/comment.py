from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    comment: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    post_id: Optional[int]


class CommentDB(CommentBase):
    created_at: datetime

    class Config:
        orm_mode = True
