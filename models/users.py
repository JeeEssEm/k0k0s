from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    phone: Mapped[str | None] = mapped_column(String(16), default=None)
    email: Mapped[str | None]
    fullname: Mapped[str | None]
    password: Mapped[str]

    verified: Mapped[bool] = mapped_column(default=False)
    avatar: Mapped[str | None]
    birthday = Mapped[date | None]

    orders: Mapped[list['Order']] = relationship(back_populates='user')  # noqa
