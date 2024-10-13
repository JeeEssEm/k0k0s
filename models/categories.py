from sqlalchemy.orm import mapped_column, Mapped, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .items import Item
from database import Base


class Category(Base):
    __tablename__ = 'categories'

    title: Mapped[str] = mapped_column(unique=True)
    is_hidden: Mapped[bool]
    is_deleted: Mapped[bool] = mapped_column(default=False)

    items: Mapped[list['Item']] = relationship(back_populates='category')
