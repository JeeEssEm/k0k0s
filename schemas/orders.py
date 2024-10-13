from pydantic import BaseModel, Field
from .users import MiniUser
from . import MiniItem
from models import Status


class CreateOrder(BaseModel):
    item_id: int
    comment: str | None
    amount: int = Field(default=1, ge=1)


class EditOrder(BaseModel):
    status: Status


class Order(CreateOrder):
    id: int
    item: MiniItem | None
    user: MiniUser | None
    status: Status | None = Status.pending
    is_paid: bool


class MiniOrder(CreateOrder):
    id: int
    item: str
    is_paid: bool
    status: Status
