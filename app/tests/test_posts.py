from http import HTTPStatus

import pytest

from app.core.constants import PAGINATION_DEFAULT
from app.repository.models import Post
from app.repository.schemas import PostDB

pytestmark = pytest.mark.anyio


async def test_root(client):
    response = await client.get("/")
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_get_all_posts(client, test_posts):
    def validate(post):
        return PostDB(**post)

    posts_list = []
    response_for_total = await client.get("/posts/")
    response_total = response_for_total.json()["total"]
    page = 1
    for __ in range(0, response_total + 1, PAGINATION_DEFAULT):
        chunk_response = await client.get(
            f"/posts/?page={page}&size={PAGINATION_DEFAULT}"
        )
        page += 1
        for post in chunk_response.json()["items"]:
            post_ready = validate(post)
            posts_list.append(post_ready)
    assert len(posts_list) == len(test_posts)
    assert response_for_total.status_code == HTTPStatus.OK


async def test_get_one_post(authorized_client, test_posts):
    response = await authorized_client.get(f"/posts/{test_posts[0].id}")
    post = PostDB(**response.json())
    assert response.status_code == HTTPStatus.OK
    assert post.title == test_posts[0].title
    assert post.description == test_posts[0].description
    assert post.price == test_posts[0].price


async def test_get_post_incorrect_id(client):
    response = await client.get("/posts/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "There is no such post"


@pytest.mark.parametrize(
    "title, description, price",
    [
        ("smth good", "very good for free", 0),
        ("google pixel", "", 100500),
        ("irobot", None, 12),
    ],
)
async def test_create_post(
    authorized_client, test_user, title, description, price
):
    response = await authorized_client.post(
        "/posts/",
        json={"title": title, "description": description, "price": price},
    )

    created_post = PostDB(**response.json())
    assert response.status_code == HTTPStatus.OK
    assert created_post.title == title
    assert created_post.description == description
    assert created_post.price == price
    assert created_post.author.id == test_user["id"]


async def test_unauthorized_user_create_post(client):
    response = await client.post(
        "/posts/",
        json={"title": "The title", "description": "no", "price": 10},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title": "new title",
        "description": "new description",
        "price": 22,
    }
    response = await authorized_client.patch(
        f"/posts/{test_posts[0].id}", json=data
    )
    updated_post = PostDB(**response.json())
    assert response.status_code == HTTPStatus.OK
    assert updated_post.author.id == test_user["id"]
    assert updated_post.title == data["title"]
    assert updated_post.description == data["description"]
    assert updated_post.price == data["price"]


async def test_unauthorized_user_update_post(client, test_posts):
    data = {"title": "The title", "description": "no", "price": 10}
    response = await client.patch(f"/posts/{test_posts[0].id}", json=data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_update_smbds_else_post(authorized_client, test_posts):
    data = {"title": "The title", "description": "no", "price": 10}
    response = await authorized_client.patch(
        f"/posts/{test_posts[1].id}", json=data
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


async def test_update_post_incorrect_id(authorized_client):
    data = {"title": "The title", "description": "no", "price": 10}
    response = await authorized_client.patch("/posts/999", json=data)
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_delete_post_success(authorized_client, test_posts):
    response = await authorized_client.delete(f"/posts/{test_posts[0].id}")
    deleted_post = Post(**response.json())
    assert deleted_post.id == test_posts[0].id
    assert response.status_code == HTTPStatus.OK


async def test_unauthorized_user_delete_post(client, test_posts):
    response = await client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_delete_smbds_else_post(authorized_client, test_posts):
    response = await authorized_client.delete(f"/posts/{test_posts[1].id}")
    assert response.status_code == HTTPStatus.FORBIDDEN


async def test_delete_post_incorrect_id(authorized_client):
    response = await authorized_client.delete("/posts/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
