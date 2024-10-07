
from typing import Annotated

from fastapi import APIRouter, Response, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import status

router = APIRouter(tags=['categories'], prefix='/categories')

@router.post('/')
async def create_category():
    pass

@router.get('/{category_id}')
async def get_category_by_id():
    pass


@router.patch('/{category_id}')
async def edit_category():
    pass


@router.delete('/{category_id}')
async def delete_category():
    pass

