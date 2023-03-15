from http import HTTPStatus

import pytest

from app.core.constants import PAGINATION_DEFAULT
from app.repository.schemas import CommentDB

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "comment",
    [
        ("Really great!"),
        ("Wow"),
        ("I'll buy it!"),
    ],
)
async def test_create_comment(
    authorized_client, test_posts, test_user, comment
):
    response = await authorized_client.post(
        f"/posts/{test_posts[1].id}/comments",
        json={"comment": comment},
    )
    created_comment = CommentDB(**response.json())
    assert response.status_code == HTTPStatus.OK
    assert created_comment.comment == comment
    assert created_comment.author == test_user["id"]


async def test_create_comment_post_incorrect_id(authorized_client):
    response = await authorized_client.post(
        "/posts/9999/comments",
        json={"comment": "that's cool"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_unauthorized_user_create_comment(client, test_posts):
    response = await client.post(
        f"/posts/{test_posts[0].id}/comments",
        json={"comment": "that's cool"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_get_all_post_comments(client, test_comments):
    def validate(comment):
        return CommentDB(**comment)

    post_id = test_comments[0].post_id
    comment_list = []
    response_for_total = await client.get(f"/posts/{post_id}/comments")
    response_total = response_for_total.json()["total"]
    page = 1
    for __ in range(0, response_total + 1, PAGINATION_DEFAULT):
        chunk_response = await client.get(
            f"/posts/{post_id}/comments?page={page}&size={PAGINATION_DEFAULT}"
        )
        page += 1
        for comment in chunk_response.json()["items"]:
            comment_ready = validate(comment)
            comment_list.append(comment_ready)
    assert len(comment_list) == len(test_comments)
    assert response_for_total.status_code == HTTPStatus.OK


async def test_get_all_comments_post_incorrect_id(client):
    response = await client.get("/posts/9999/comments")
    assert response.status_code == HTTPStatus.NOT_FOUND
