from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .orders import Order
    from .cart import Cart
from database import Base


class User(Base):
    __tablename__ = 'users'

    phone: Mapped[str | None] = mapped_column(String(16), default='')
    email: Mapped[str]
    fullname: Mapped[str]
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    verified: Mapped[bool] = mapped_column(default=False)
    avatar: Mapped[str | None]
    birthday: Mapped[date | None]

    cart: Mapped['Cart'] = relationship()
    orders: Mapped[list['Order']] = relationship(back_populates='user')
