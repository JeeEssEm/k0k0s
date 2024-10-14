from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .items import Item

from database import Base, DeclarativeBase


class CartItem(DeclarativeBase):
    __tablename__ = 'cart_items'
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'), primary_key=True)
    amount: Mapped[int]

    item: Mapped['Item'] = relationship(lazy='joined')


class Cart(Base):
    __tablename__ = 'cart'
    items: Mapped[list[CartItem]] = relationship(lazy='selectin')
