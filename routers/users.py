from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse

from core.users import get_current_authenticated_user
from schemas import User
from services import UserService

router = APIRouter(tags=['users'], prefix='/users')


@router.get('/me')
async def get_me(
        current_user: Annotated[User, Depends(get_current_authenticated_user)]
) -> User:
    return current_user


@router.get('/{user_id}')
async def get_user(
        user_id: int,
        user_service: Annotated[UserService, Depends()]
) -> User:
    return await user_service.get_by_id(user_id)


@router.get('/{user_id}/image')
async def get_user_image(
        user_id: int,
        user_service: Annotated[UserService, Depends()]
):
    return StreamingResponse(
        await user_service.get_user_image(user_id),
        media_type='image/webp',
    )


@router.post('/image')
async def load_user_image(
        image: UploadFile,
        current_user: Annotated[User, Depends(get_current_authenticated_user)],
        user_service: Annotated[UserService, Depends()],
):
    return await user_service.upload_image(current_user.id, image)
