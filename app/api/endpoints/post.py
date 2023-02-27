from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_post_exist
from app.core.db import get_async_session
from app.repository.crud.comment import comment_crud
from app.repository.crud.post import post_crud
from app.repository.schemas.comment import CommentCreate, CommentDB
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


@router.post("/{post_id}/comments", response_model=CommentDB)
async def create_new_comment(
    post_id: int,
    comment: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_post_exist(post_id, session)
    comment.post_id = post_id
    new_comment = await comment_crud.create(comment, session)
    return new_comment


@router.get("/{post_id}/comments", response_model=list[CommentDB])
async def get_all_comments(
    post_id: int, session: AsyncSession = Depends(get_async_session)
):
    await check_post_exist(post_id, session)
    all_comments = await comment_crud.get_comments_by_post(post_id, session)
    return all_comments
