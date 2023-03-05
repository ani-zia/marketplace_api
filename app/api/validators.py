from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.repository.crud.post import post_crud
from app.repository.models import Post, User


async def check_post_exist(
    post_id: int, session: AsyncSession = Depends(get_async_session)
) -> Post:
    post_db = await post_crud.get_post_by_id(post_id, session)
    if not post_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="There is no such post"
        )
    return post_db


async def check_post_before_edit(
    post_id: int, session: AsyncSession, author: User
) -> Post:
    post_db = await post_crud.get_post_by_id(post_id, session)
    if not post_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="There is no such post"
        )
    if post_db.author_id != author.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Someone else's post cannot be edited or deleted",
        )
    return post_db
