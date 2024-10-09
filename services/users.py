from .base import Service
from core.security import verify_password, create_tokens, decode_token
from repositories import UsersRepository
from schemas import CreateUser, ShortUser
from exceptions import (UserNotFound, InvalidToken, IncorrectPassword,
                        UserAlreadyExists)


class UserService(Service):
    repository: UsersRepository

    async def login_user(self, username: str, password: str) -> dict:
        user = await self.repository.get_by_username(username)
        hashed_pwd = await self.repository.get_user_hashed_password(user.id)
        if user is None:
            raise UserNotFound

        if not verify_password(password, hashed_pwd):
            raise IncorrectPassword
        return create_tokens(user.id, hashed_pwd)

    async def create_user(self, user: CreateUser) -> ShortUser:
        if await self.repository.check_exists(user.fullname, user.email):
            raise UserAlreadyExists
        return await self.repository.create_user(user)

    async def get_by_id(self, user_id) -> ShortUser:
        return await self.repository.get_by_id(user_id)

    async def get_user_password(self, user_id: int) -> str:
        return await self.repository.get_user_hashed_password(user_id)

    async def update_token(self, token) -> str:
        try:
            data = decode_token(token)
            if data.get('type') != 'refresh':
                raise InvalidToken
            current_user = await self.repository.get_by_id(data.get('id'))
            tokens = create_tokens(current_user.id, current_user.password)
            return tokens['access_token']

        except Exception:
            raise InvalidToken
