from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Integer

if TYPE_CHECKING:
    from .items import Item
    from .users import User
from database import Base


class Status(Enum):
    completed = 'completed'
    in_progress = 'in_progress'
    cancelled = 'cancelled'
    pending = 'pending'


class Order(Base):
    __tablename__ = 'orders'

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    amount: Mapped[int] = mapped_column(default=1)
    comment: Mapped[str] = mapped_column(default=None)
    status: Mapped[Status] = mapped_column(default=Status.pending)
    is_paid: Mapped[bool] = mapped_column(default=False)

    user: Mapped['User'] = relationship(back_populates='orders', lazy='joined')
    item: Mapped['Item'] = relationship(lazy='joined')
