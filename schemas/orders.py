from typing import TYPE_CHECKING

from pydantic import BaseModel

from .users import MiniUser
if TYPE_CHECKING:
    from . import Cart
from models import Status


class CreateOrder(BaseModel):
    comment: str | None


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
