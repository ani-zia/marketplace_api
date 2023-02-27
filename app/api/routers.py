from fastapi import APIRouter

from app.api.endpoints import post_router

main_router = APIRouter()

main_router.include_router(post_router, prefix="/posts", tags=["Posts"])
