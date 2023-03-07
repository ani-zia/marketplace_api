import logging

from fastapi import APIRouter, Depends
from fastapi_pagination import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.pagination import Page, Params
from app.api.validators import check_post_before_edit, check_post_exist
from app.core.db import get_async_session
from app.core.user import current_user
from app.repository.crud.comment import comment_crud
from app.repository.crud.post import post_crud
from app.repository.models import User
from app.repository.schemas import (
    CommentCreate,
    CommentDB,
    PostCreate,
    PostDB,
    PostUpdate,
)

router = APIRouter()


@router.get("/", response_model=Page[PostDB])
async def get_all_posts(
    session: AsyncSession = Depends(get_async_session),
    params: Params = Depends(),
):
    all_posts = await post_crud.get_posts(session)
    logging.info("Extract posts from DB")
    return paginate(all_posts, params)


@router.get("/{post_id}", response_model=PostDB)
async def get_post(
    post_id: int, session: AsyncSession = Depends(get_async_session)
):
    db_post = await check_post_exist(post_id, session)
    logging.info(f"Get post with id {db_post.id} from DB")
    return db_post


@router.post("/", response_model=PostDB)
async def create_new_posts(
    post: PostCreate,
    session: AsyncSession = Depends(get_async_session),
    author: User = Depends(current_user),
):
    new_post = await post_crud.create_post(post, session, author)
    logging.info(f"Create new post with id {new_post.id}")
    return new_post


@router.patch("/{post_id}", response_model=PostDB)
async def partially_update_posts(
    post_id: int,
    req_post: PostUpdate,
    session: AsyncSession = Depends(get_async_session),
    author: User = Depends(current_user),
):
    post_db = await check_post_before_edit(post_id, session, author)
    updated_post = await post_crud.update_post(req_post, post_db, session)
    logging.info(f"Update post with id {updated_post.id}")
    return updated_post


@router.delete("/{post_id}")
async def remove_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    author: User = Depends(current_user),
):
    post_db = await check_post_before_edit(post_id, session, author)
    deleted_post = await post_crud.delete_post(post_db, session)
    logging.info(f"Delete post with id {deleted_post.id}")
    return deleted_post


@router.post("/{post_id}/comments", response_model=Page[CommentDB])
async def create_new_comment(
    post_id: int,
    comment: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
    author: User = Depends(current_user),
):
    await check_post_exist(post_id, session)
    comment.post_id = post_id
    new_comment = await comment_crud.create_comment(comment, session, author)
    logging.info(f"Create comment with id {new_comment.id}")
    return new_comment


@router.get("/{post_id}/comments", response_model=Page[CommentDB])
async def get_all_comments(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    params: Params = Depends(),
):
    await check_post_exist(post_id, session)
    all_comments = await comment_crud.get_comments_by_post(post_id, session)
    logging.info("Extract comments from DB")
    return paginate(all_comments, params)
