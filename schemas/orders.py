from pydantic import BaseModel
from .users import ShortUser
from . import Item


class CreateOrder(BaseModel):
    item_id: int
    comment: str | None


class Order(CreateOrder):
    id: int
    item: Item | None
    user: ShortUser | None
