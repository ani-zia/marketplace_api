from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.crud.base import CRUDBase
from app.repository.models import Comment, User
from app.repository.schemas.comment import CommentCreate


class CommentCRUD(CRUDBase):
    async def get_comments_by_post(
        self, post_id: int, session: AsyncSession
    ) -> list[Comment]:
        comments = await session.execute(
            select(Comment).where(Comment.post_id == post_id)
        )
        return comments.scalars().all()

    async def create_comment(
        self, comment_in: CommentCreate, session: AsyncSession, author: User
    ) -> Comment:
        comment_in_data = comment_in.dict()
        db_comment = self.model(**comment_in_data, author=author.id)
        session.add(db_comment)
        await session.commit()
        await session.refresh(db_comment)
        return db_comment


comment_crud = CommentCRUD(Comment)
