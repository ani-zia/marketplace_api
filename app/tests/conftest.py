from http import HTTPStatus

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.db import Base, get_async_session
from app.main import main_router
from app.repository.models import Comment, Post


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


pytestmark = pytest.mark.anyio


def start_application():
    app = FastAPI()
    app.include_router(main_router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test_db.db"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionTesting = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


@pytest.fixture
async def app():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    app = start_application()
    yield app


@pytest.fixture
async def db_session(app):
    async with SessionTesting() as async_session:
        yield async_session


@pytest.fixture
async def client(app, db_session):
    async def get_test_db():
        yield db_session

    app.dependency_overrides[get_async_session] = get_test_db
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        yield ac


@pytest.fixture
async def test_user(client):
    user_data = {"email": "user@example.com", "password": "string"}
    res = await client.post("/auth/register", json=user_data)
    assert res.status_code == HTTPStatus.CREATED
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
async def test_user2(client):
    user_data = {"email": "user2@example.com", "password": "string2"}
    res = await client.post("/auth/register", json=user_data)
    assert res.status_code == HTTPStatus.CREATED
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
async def authorized_user_token(client, test_user):
    res = await client.post(
        "/auth/jwt/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    assert res.status_code == HTTPStatus.OK
    return res.json()["access_token"]


@pytest.fixture
def authorized_client(client, authorized_user_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {authorized_user_token}",
    }
    return client


@pytest.fixture
async def test_posts(db_session, test_user, test_user2):
    posts_data = [
        {
            "title": "1st title",
            "description": "first content",
            "price": 1,
            "author_id": test_user["id"],
        },
        {
            "title": "2nd title",
            "description": "2nd content",
            "price": 2,
            "author_id": test_user2["id"],
        },
        {
            "title": "3rt title",
            "description": "3rd content",
            "price": 3,
            "author_id": test_user["id"],
        },
        {
            "title": "4th title",
            "description": "4th content",
            "price": 4,
            "author_id": test_user2["id"],
        },
        {
            "title": "5th title",
            "description": "",
            "price": 5,
            "author_id": test_user["id"],
        },
        {
            "title": "6th title",
            "description": None,
            "price": 6,
            "author_id": test_user2["id"],
        },
    ]
    for post in posts_data:
        post_db = Post(**post)
        db_session.add(post_db)
    await db_session.commit()
    db_posts = await db_session.execute(select(Post))
    return db_posts.scalars().all()


@pytest.fixture
async def test_comments(db_session, test_posts, test_user, test_user2):
    post_id = test_posts[0].id
    comments_data = [
        {
            "comment": "1st comment",
            "post_id": post_id,
            "author": test_user["id"],
        },
        {
            "comment": "2nd comment",
            "post_id": post_id,
            "author": test_user2["id"],
        },
        {
            "comment": "3rd comment",
            "post_id": post_id,
            "author": test_user["id"],
        },
        {
            "comment": "4th comment",
            "post_id": post_id,
            "author": test_user2["id"],
        },
        {
            "comment": "5th comment",
            "post_id": post_id,
            "author": test_user["id"],
        },
    ]
    for comment in comments_data:
        comment_db = Comment(**comment)
        db_session.add(comment_db)
    await db_session.commit()
    db_comment = await db_session.execute(
        select(Comment).where(Comment.post_id == post_id)
    )
    return db_comment.scalars().all()
