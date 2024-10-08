from pydantic import BaseModel
from .users import ShortUser
from . import ItemSchema


class CreateOrder(BaseModel):
    item_id: int
    comment: str | None


class OrderSchema(CreateOrder):
    id: int
    item: ItemSchema | None
    user: ShortUser | None
