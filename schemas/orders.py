from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from .users import MiniUser
if TYPE_CHECKING:
    from . import Cart
from models import Status


class CreateOrder(BaseModel):
    comment: str | None
    amount: int = Field(default=1, ge=1)


class EditOrder(BaseModel):
    status: Status


class Order(CreateOrder):
    id: int
    cart: 'Cart'
    user: MiniUser | None
    status: Status | None = Status.pending
    is_paid: bool


class MiniOrder(CreateOrder):
    id: int
    is_paid: bool
    status: Status
