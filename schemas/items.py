from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from .categories import Category


class CreateItem(BaseModel):
    title: str
    description: str | None = Field(default=None)
    price: int | None = Field(default=0)
    amount: int | None = Field(default=0)
    is_hidden: bool | None = Field(default=False)


class Item(CreateItem):
    id: int
    category: Optional['Category'] = None
    is_deleted: bool


class MiniItem(BaseModel):
    id: int
    title: str
    price: int | None
