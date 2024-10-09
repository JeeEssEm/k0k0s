from sqlalchemy import select, or_

from config import settings
from core.security import get_password_hash
from exceptions import UserNotFound
from .base import Repository
import models

from schemas import CreateUser, ShortUser


class UsersRepository(Repository):
    async def _get_user_by_id(self, user_id: int) -> models.User:
        user = await self.session.get(models.User, user_id)
        if not user:
            raise UserNotFound
        return user

    def _convert_model_to_schema(self, user: models.User) -> ShortUser:
        return ShortUser(
            id=user.id,
            fullname=user.fullname,
            email=user.email,
            joined=user.created_at.date()
        )

    async def get_by_id(self, user_id: int) -> ShortUser:
        user = await self._get_user_by_id(user_id)
        return self._convert_model_to_schema(user)

    async def get_user_hashed_password(self, user_id: int) -> str:
        return (await self._get_user_by_id(user_id)).password

    async def get_by_username(self, data: str) -> ShortUser:
        q = select(models.User).where(
            or_(models.User.email == data, models.User.fullname == data)
        )
        res = await self.session.execute(q)
        return self._convert_model_to_schema(
            res.scalars().first()
        )

    async def check_exists(self, fullname: str, email: str) -> bool:
        q = select(models.User).where(or_(
            models.User.email == email, models.User.fullname == fullname
        ))
        res = await self.session.execute(q)
        return res.scalars().first() is not None

    async def create_user(self, user: CreateUser) -> ShortUser:
        new_user = models.User(
            email=user.email,
            fullname=user.fullname,
            password=get_password_hash(user.password1),
            phone=user.phone,
            verified=settings.VERIFIED
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return self._convert_model_to_schema(new_user)
