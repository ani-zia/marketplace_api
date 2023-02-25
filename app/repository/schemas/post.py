from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt, validator


class PostBase(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=128)
    description: Optional[str] = Field(None, min_length=1)
    price: Optional[NonNegativeInt]


class PostCreate(PostBase):
    title: str = Field(..., min_length=2, max_length=128)
    price: NonNegativeInt


class PostUpdate(PostBase):
    is_active: Optional[bool]

    @validator("title", "price", "is_active")
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError("Field cannot be empty")
        return value


class PostDB(PostCreate):
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
