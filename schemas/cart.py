from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .items import MiniItem


class Cart(BaseModel):
    id: int
    items: list['MiniItem']


class EditItem(BaseModel):
    amount: int
