from typing import Annotated

from fastapi import APIRouter, Depends

from services import CategoriesService

router = APIRouter(tags=['categories'], prefix='/categories')


@router.post('/')
async def create_category():
    pass


@router.get('/{category_id}')
async def get_category_by_id(
        category_id: int,
        category_service: Annotated[CategoriesService, Depends()]
):
    return await category_service.get_category_by_id(category_id)


@router.patch('/{category_id}')
async def edit_category():
    pass


@router.delete('/{category_id}')
async def delete_category():
    pass
