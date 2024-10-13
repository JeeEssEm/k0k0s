from typing import Annotated

from fastapi import APIRouter, Depends

from core.utils import get_current_authenticated_user, get_current_user
from services import CategoriesService
from schemas import ShortUser

router = APIRouter(tags=['categories'], prefix='/categories')


@router.post('/')
async def create_category():
    pass


@router.get('/{category_id}')
async def get_category_by_id(
        category_id: int,
        current_user: Annotated[ShortUser, Depends(get_current_user)],
        category_service: Annotated[CategoriesService, Depends()]
):
    return await category_service.get_category_by_id(category_id, current_user)


@router.patch('/{category_id}')
async def edit_category():
    pass


@router.delete('/{category_id}')
async def delete_category():
    pass


@router.get('/')
async def get_categories(
        category_service: Annotated[CategoriesService, Depends()]
):
    return await category_service.get_categories()
