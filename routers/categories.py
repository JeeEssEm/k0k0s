from typing import Annotated

from fastapi import APIRouter, Depends

from core.utils import get_current_authenticated_user, get_current_user
from services import CategoriesService, ItemsService
from schemas import ShortUser, CreateCategory
from exceptions import NotEnoughRights

router = APIRouter(tags=['categories'], prefix='/categories')


@router.post('/')
async def create_category(
    data: CreateCategory,
    current_user: Annotated[ShortUser, Depends(get_current_authenticated_user)],
    category_service: Annotated[CategoriesService, Depends()]
):
    if not current_user.is_admin:
        raise NotEnoughRights
    return await category_service.create_category(data)


@router.get('/{category_id}')
async def get_category_by_id(
        category_id: int,
        current_user: Annotated[ShortUser, Depends(get_current_user)],
        category_service: Annotated[CategoriesService, Depends()]
):
    return await category_service.get_category_by_id(category_id, current_user)


@router.patch('/{category_id}')
async def edit_category(
    category_id: int,
    data: CreateCategory,
    current_user: Annotated[ShortUser, Depends(get_current_authenticated_user)],
    category_service: Annotated[CategoriesService, Depends()]
):
    if not current_user.is_admin:
        raise NotEnoughRights
    return await category_service.edit_category(category_id, data)


@router.delete('/{category_id}')
async def delete_category(
    category_id: int,
    current_user: Annotated[ShortUser, Depends(get_current_authenticated_user)],
    category_service: Annotated[CategoriesService, Depends()]
):
    if not current_user.is_admin:
        raise NotEnoughRights
    await category_service.delete_category(category_id)
    return 'Deleted successfully'


@router.get('/')
async def get_categories(
        category_service: Annotated[CategoriesService, Depends()],
        current_user: Annotated[ShortUser, Depends(get_current_user)],
):
    return await category_service.get_categories(current_user)


@router.get('/{category_id}/items')
async def get_category_items(
    category_id: int,
    current_user: Annotated[ShortUser, Depends(get_current_user)],
    items_service: Annotated[ItemsService, Depends()],
    category_service: Annotated[CategoriesService, Depends()]
):
    category = await category_service.get_category_by_id(category_id, current_user)
    return await items_service.get_items_by_category(
        category, current_user
    )
