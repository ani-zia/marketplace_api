from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.repository.crud.post import post_crud
from app.repository.schemas.post import PostCreate, PostDB, PostUpdate

router = APIRouter()


@router.get("/", response_model=list[PostDB])
async def get_all_posts(session: AsyncSession = Depends(get_async_session)):
    all_posts = await post_crud.get_multi(session)
    return all_posts


@router.get("/{post_id}", response_model=PostDB)
async def get_post(
    post_id: int, session: AsyncSession = Depends(get_async_session)
):
    print(post_id)
    db_post = await check_post_exist(post_id, session)
    return db_post


@router.post("/", response_model=PostDB)
async def create_new_posts(
    post: PostCreate, session: AsyncSession = Depends(get_async_session)
):
    new_post = await post_crud.create(post, session)
    return new_post


@router.patch("/{post_id}", response_model=PostDB)
async def partially_update_posts(
    post_id: int,
    req_post: PostUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    post_db = await check_post_exist(post_id, session)
    updated_post = await post_crud.update_post(req_post, post_db, session)
    return updated_post


@router.delete("/{post_id}", response_model=PostDB)
async def remove_post(
    post_id: int, session: AsyncSession = Depends(get_async_session)
):
    post_db = await check_post_exist(post_id, session)
    deleted_post = await post_crud.delete_post(post_db, session)
    return deleted_post


async def check_post_exist(
    post_id: int, session: AsyncSession = Depends(get_async_session)
):
    post_db = await post_crud.get_post_by_id(post_id, session)
    if not post_db:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Такой записи нет")
    return post_db
