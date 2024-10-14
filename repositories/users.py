from sqlalchemy import select, or_

from config import settings
from core.security import get_password_hash
from exceptions import UserNotFound
from .base import Repository
import models

from schemas import CreateUser, User


class UsersRepository(Repository):
    async def _get_user_by_id(self, user_id: int) -> models.User:
        user = await self.session.get(models.User, user_id)
        if not user:
            raise UserNotFound
        return user

    def _convert_model_to_schema(self, user: models.User) -> User:
        return User(
            id=user.id,
            fullname=user.fullname,
            email=user.email,
            joined=user.created_at.date(),
            is_admin=user.is_admin,
            cart_id=user.cart_id
        )

    async def get_by_id(self, user_id: int) -> User:
        user = await self._get_user_by_id(user_id)
        return self._convert_model_to_schema(user)

    async def get_user_hashed_password(self, user_id: int) -> str:
        return (await self._get_user_by_id(user_id)).password

    async def get_by_username(self, data: str) -> User:
        q = select(models.User).where(
            or_(models.User.email == data, models.User.fullname == data)
        )
        user = (await self.session.scalars(q)).first()
        if not user:
            raise UserNotFound
        return self._convert_model_to_schema(
            user
        )

    async def check_exists(self, fullname: str, email: str) -> bool:
        q = select(models.User).where(or_(
            models.User.email == email, models.User.fullname == fullname
        ))
        res = await self.session.execute(q)
        return res.scalars().first() is not None

    async def create_user(self, user: CreateUser) -> User:
        new_user = models.User(
            email=user.email,
            fullname=user.fullname,
            password=get_password_hash(user.password1),
            phone=user.phone,
            verified=settings.VERIFIED
        )
        new_cart = models.Cart()
        new_user.cart = new_cart
        self.session.add(new_user)
        self.session.add(new_cart)
        await self.session.commit()
        await self.session.refresh(new_user)
        return self._convert_model_to_schema(new_user)
