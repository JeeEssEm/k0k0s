from typing import Annotated

from fastapi import APIRouter, Depends

from core.utils import get_current_authenticated_user
from schemas import User, EditItem, Cart
from services import CartService, ItemsService

router = APIRouter(prefix='/cart', tags=['cart'])


@router.get('/my')
async def get_my_cart(
        current_user: Annotated[User, Depends(get_current_authenticated_user)],
        cart_service: Annotated[CartService, Depends()]
) -> Cart:
    return await cart_service.get_cart_by_id(current_user.cart_id)


@router.post('/{item_id}')
async def add_item_to_cart(
        item_id: int,
        current_user: Annotated[User, Depends(get_current_authenticated_user)],
        cart_service: Annotated[CartService, Depends()],
        item_service: Annotated[ItemsService, Depends()]
) -> str:
    await item_service.get_item_by_id(item_id, current_user)
    await cart_service.add_item_to_cart(item_id, current_user)
    return 'Item added to cart successfully'


@router.delete('/{item_id}')
async def remove_item_from_cart(
        item_id: int,
        current_user: Annotated[User, Depends(get_current_authenticated_user)],
        cart_service: Annotated[CartService, Depends()],
) -> str:
    await cart_service.remove_item_from_cart(item_id, current_user)
    return 'Item removed from cart successfully'


@router.patch('/{item_id}')
async def edit_item_amount(
        item_id: int,
        edit_item: EditItem,
        current_user: Annotated[User, Depends(get_current_authenticated_user)],
        cart_service: Annotated[CartService, Depends()],
) -> str:
    await cart_service.edit_item_amount(current_user, item_id, edit_item.amount)
    return 'Item amount edited successfully'
