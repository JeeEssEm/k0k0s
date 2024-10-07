from models import Order
from core.utils import get_current_user
# from schemas import 
# from services import 

from typing import Annotated
from fastapi import APIRouter, Path, Depends
from fastapi import status

router = APIRouter(tags=['orders'], prefix='/orders')


@router.post('/')
async def create_order():
    pass


@router.get('/{order_id}')
async def get_order_by_id():
    pass


@router.patch('/{order_id}')
async def edit_order():
    pass


@router.delete('/{order_id}')
async def delete_order():
    pass


@router.get('/mine_orders')
async def get_mine_orders():
    pass


@router.post('/{order_id}/purchase')
async def purchase_order():
    pass