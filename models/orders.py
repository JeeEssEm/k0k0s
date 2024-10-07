from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from datetime import date

from database import Base


class Order(Base):
    __tablename__ = 'orders'

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    date: Mapped[date]

    user: Mapped['User'] = relationship(back_populates='orders')
    item: Mapped['Item'] = relationship()
