from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from database import Base


class Item(Base):
    __tablename__ = 'items'

    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    amount: Mapped[int] = mapped_column(default=0)
    is_hidden: Mapped[bool] = mapped_column(default=True)
    deleted: Mapped[bool] = mapped_column(default=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    category: Mapped['Category'] = relationship(back_populates='items')  # noqa
