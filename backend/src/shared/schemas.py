from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PageParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Número da página (mínimo 1)")
    size: int = Field(default=10, ge=1, le=100, description="Itens por página (máximo 100)")


class PageResponse(BaseModel, Generic[T]):
    items: list[T]
    page: int
    size: int
    total_items: int
    total_pages: int