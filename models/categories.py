from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class Category(Base):
    __tablename__ = 'categories'

    title: Mapped[int]
    is_hidden: Mapped[bool]

    items: Mapped[list['Item']] = relationship(back_populates='category', cascade='all, delete-orphan')
