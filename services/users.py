from fastapi import UploadFile

from .base import Service
from core.images import convert_image_to_webp
from core.security import verify_password, create_tokens, decode_token
from repositories import UsersRepository, S3Users
from schemas import CreateUser, User
from exceptions import (UserNotFound, InvalidToken, IncorrectPassword,
                        UserAlreadyExists, ImageNotFound)


class UserService(Service):
    repository: UsersRepository
    s3_repository: S3Users

    async def login_user(self, username: str, password: str) -> dict:
        user = await self.repository.get_by_username(username)
        hashed_pwd = await self.repository.get_user_hashed_password(user.id)
        if user is None:
            raise UserNotFound

        if not verify_password(password, hashed_pwd):
            raise IncorrectPassword
        return create_tokens(user.id, hashed_pwd)

    async def create_user(self, user: CreateUser) -> User:
        if await self.repository.check_exists(user.fullname, user.email):
            raise UserAlreadyExists
        return await self.repository.create_user(user)

    async def get_by_id(self, user_id) -> User:
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

    async def upload_image(self, user_id: int, image: UploadFile):
        file = await convert_image_to_webp(image)
        path = await self.s3_repository.upload_image(user_id, file)
        return await self.repository.upload_image(user_id, path)

    async def get_user_image(self, user_id: int):
        user = await self.repository.get_by_id(user_id)
        if not user.avatar:
            raise ImageNotFound
        try:
            return await self.s3_repository.get_image(user.avatar)
        except Exception:
            raise ImageNotFound
