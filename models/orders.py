from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

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
    comment: Mapped[str] = mapped_column(default=None)
    status: Mapped[Status] = mapped_column(default=Status.pending)

    user: Mapped['User'] = relationship(back_populates='orders')
    item: Mapped['Item'] = relationship()
