from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .items import MiniItem


class CreateCategory(BaseModel):
    title: str
    is_hidden: bool


class Category(CreateCategory):
    id: int
    is_deleted: bool


class CategoryItems(Category):
    items: list['MiniItem']
