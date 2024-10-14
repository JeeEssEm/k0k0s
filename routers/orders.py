from typing import Annotated

from fastapi import APIRouter, Depends

from core.utils import get_current_authenticated_user
from services import OrdersService, CartService
from schemas import CreateOrder, User
from exceptions import CartIsEmpty


router = APIRouter(tags=['orders'], prefix='/orders')


@router.post('/')
async def create_order(
        data: CreateOrder,
        order_service: Annotated[OrdersService, Depends()],
        cart_service: Annotated[CartService, Depends()],
        current_user: Annotated[User, Depends(get_current_authenticated_user)],
):
    if await cart_service.is_cart_empty(current_user.cart_id):
        raise CartIsEmpty
    await cart_service.change_user_cart(current_user)
    return await order_service.create_order(data, current_user)


@router.get('/my')
async def get_my_orders(
    order_service: Annotated[OrdersService, Depends()],
    current_user: Annotated[User, Depends(get_current_authenticated_user)],
):
    return await order_service.get_user_orders(current_user.id)


@router.get('/{order_id}')
async def get_order(
    order_id: int,
    order_service: Annotated[OrdersService, Depends()],
    current_user: Annotated[User, Depends(get_current_authenticated_user)]
):
    return await order_service.get_order_by_id(order_id, current_user)


# @router.patch('/{order_id}')
# async def edit_order(
#     order_id: int,
#     data: EditOrder,
#     order_service: Annotated[OrdersService, Depends()],
#     current_user: Annotated[User, Depends(get_current_authenticated_user)],
# ):
#     if not current_user.is_admin:
#         raise NotEnoughRights  # заказы могут редактировать только админы
#     return await order_service.edit_order(order_id, data)


@router.delete('/{order_id}')
async def cancel_order(
    order_id: int,
    order_service: Annotated[OrdersService, Depends()],
    current_user: Annotated[User, Depends(get_current_authenticated_user)],
):
    await order_service.cancel_order(order_id, current_user)
    return 'Order cancelled successfully'


@router.post('/{order_id}/purchase')
async def purchase_order(
        order_id: int,
        order_service: Annotated[OrdersService, Depends()],
        current_user: Annotated[User, Depends(get_current_authenticated_user)],
):
    await order_service.purchase_order(order_id, current_user)
    return 'Order purchased successfully'
