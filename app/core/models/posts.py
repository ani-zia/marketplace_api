from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.db import Base


class Post(Base):
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
