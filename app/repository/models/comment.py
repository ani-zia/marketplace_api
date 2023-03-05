from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, Text, func

from app.core.db import Base


class Comment(Base):
    comment = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )
    post_id = Column(Integer, ForeignKey("post.id"))
    author = Column(Integer, ForeignKey("user.id"))
