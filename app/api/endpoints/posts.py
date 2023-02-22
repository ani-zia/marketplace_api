from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_all_posts():
    """List of all posts."""
    return {"Hello, posts are here!"}
