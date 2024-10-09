from typing import Annotated

from fastapi import Depends

from .security import is_valid_token, decode_token
from services.users import UserService
from routers.auth import oauth2_scheme
from exceptions import InvalidToken, TokenExpired


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: Annotated[UserService, Depends()]
):
    if not token:
        return None
    try:
        user_id = decode_token(token).get('id')
        user = await user_service.get_by_id(user_id)
        password = await user_service.get_user_password(user_id)
        if is_valid_token(token, password):
            return user
        raise InvalidToken
    except Exception:
        raise TokenExpired
