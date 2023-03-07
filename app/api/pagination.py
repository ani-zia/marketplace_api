from typing import Generic, TypeVar

from fastapi import Query
from fastapi_pagination.default import Page as BasePage
from fastapi_pagination.default import Params as BaseParams

from app.core.config import settings

T = TypeVar("T")


class Params(BaseParams):
    size: int = Query(
        settings.pagination_default, ge=1, le=1_000, description="Page size"
    )


class Page(BasePage[T], Generic[T]):
    __params_type__ = Params
