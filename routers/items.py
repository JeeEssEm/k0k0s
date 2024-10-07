
# from services import UserService
# from schemas import CreateUser, Token

from typing import Annotated

from fastapi import APIRouter, Response, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import status

router = APIRouter(tags=['items'], prefix='/items')


@router.post('/')
async def create_item():
    pass

@router.get('/{item_id}')
async def get_item_by_id():
    pass


@router.patch('/{item_id}')
async def edit_item():
    pass


@router.delete('/{item_id}')
async def delete_item():
    pass
