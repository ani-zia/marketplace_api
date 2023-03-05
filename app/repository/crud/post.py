from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.crud.base import CRUDBase
from app.repository.models import Post, User
from app.repository.schemas.post import PostCreate, PostUpdate


class CRUDPost(CRUDBase):
    async def get_post_by_id(
        self, post_id: int, session: AsyncSession
    ) -> Optional[Post]:
        db_post = await session.get(Post, post_id)
        return db_post

    async def create_post(
        self, post_in: PostCreate, session: AsyncSession, author: User
    ):
        post_in_data = post_in.dict()
        db_post = self.model(**post_in_data, author_id=author.id)
        session.add(db_post)
        await session.commit()
        await session.refresh(db_post)
        return db_post

    async def update_post(
        self, req_post: PostUpdate, db_post: Post, session: AsyncSession
    ) -> Post:
        obj_data = jsonable_encoder(db_post)
        update_data = req_post.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_post, field, update_data[field])
        session.add(db_post)
        await session.commit()
        await session.refresh(db_post)
        return db_post

    async def delete_post(self, db_post: Post, session: AsyncSession) -> Post:
        await session.delete(db_post)
        await session.commit()
        return db_post


post_crud = CRUDPost(Post)
