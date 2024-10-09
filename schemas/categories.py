from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .items import Item


class CreateCategory(BaseModel):
    title: str
    is_hidden: bool


class Category(CreateCategory):
    id: int


class CategoryItems(Category):
    items: list['Item']
