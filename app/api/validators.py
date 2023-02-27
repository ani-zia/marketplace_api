from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.repository.crud.post import post_crud


async def check_post_exist(
    post_id: int, session: AsyncSession = Depends(get_async_session)
):
    post_db = await post_crud.get_post_by_id(post_id, session)
    if not post_db:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Такой записи нет")
    return post_db
