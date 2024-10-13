from typing import Annotated
from datetime import datetime

from fastapi import Depends

from .security import is_valid_token, decode_token
from services.users import UserService
from routers.auth import oauth2_scheme
from exceptions import InvalidToken, TokenExpired
from schemas import ShortUser


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: Annotated[UserService, Depends()]
):
    if not token:
        return ShortUser(
            id=-1,
            fullname='Anonym',
            email='anonym@email.org',
            joined=datetime.now().date(),
            is_admin=False,
        )
    try:
        user_id = decode_token(token).get('id')
        user = await user_service.get_by_id(user_id)
        password = await user_service.get_user_password(user_id)
        if is_valid_token(token, password):
            return user
        raise InvalidToken
    except Exception:
        raise TokenExpired


async def get_current_authenticated_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: Annotated[UserService, Depends()]
):
    user = await get_current_user(token, user_service)
    if not user:
        raise InvalidToken
    return user
