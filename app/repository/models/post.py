from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.core.db import Base


class Post(Base):
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
        onupdate=func.current_timestamp(),
    )
    comments = relationship("Comment", cascade="delete")
    author_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    author = relationship("User", lazy="joined")
