import logging

from fastapi import FastAPI
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routers import main_router
from app.core.config import settings
from app.core.logger import configure_logging

app = FastAPI(title=settings.app_title)

app.include_router(main_router)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    logging.error(f"{repr(exc)}")
    return await http_exception_handler(request, exc)


@app.on_event("startup")
async def startup():
    configure_logging()
    logging.info("Application start")


@app.on_event("shutdown")
def shutdown_event():
    logging.info("Application shutdown")
