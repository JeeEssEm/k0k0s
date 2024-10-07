from .security import is_valid_token, decode_token
from services.users import UserService
from routers.auth import oauth2_scheme

from fastapi import Depends
from fastapi.exceptions import HTTPException
from typing import Annotated
from fastapi import status


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: UserService = Depends()
):
    if not token:
        return None
    try:
        data = decode_token(token)
        user = await user_service.get_by_id(data.get('id'))
        if is_valid_token(token):
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is not valid anymore'
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Token expired! {exc}'
        )
