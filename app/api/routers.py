from fastapi import APIRouter

from app.api.endpoints import posts_router

main_router = APIRouter()

main_router.include_router(posts_router, prefix="/posts", tags=["posts"])
