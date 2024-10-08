from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class Category(Base):
    __tablename__ = 'categories'

    title: Mapped[str]
    is_hidden: Mapped[bool]
    deleted: Mapped[bool] = mapped_column(default=False)

    items: Mapped[list['Item']] = relationship(back_populates='category')  # noqa
