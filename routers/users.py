from typing import Annotated

from fastapi import APIRouter, Depends

from core.utils import get_current_user
from schemas import User
from services import UserService

router = APIRouter(tags=['users'], prefix='/users')


@router.get('/me')
async def get_me(
        current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    return current_user


@router.get('/{user_id}')
async def get_user(
        user_id: int,
        user_service: Annotated[UserService, Depends()]
) -> User:
    return await user_service.get_by_id(user_id)
