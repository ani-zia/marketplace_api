from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.crud.base import CRUDBase
from app.repository.models import Comment


class CommentCRUD(CRUDBase):
    async def get_comments_by_post(
        self, post_id: int, session: AsyncSession
    ) -> list[Comment]:
        comments = await session.execute(
            select(Comment).where(Comment.post_id == post_id)
        )
        return comments.scalars().all()


comment_crud = CommentCRUD(Comment)
