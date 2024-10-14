from schemas import Cart, User
from .base import Service
from repositories import CartRepository
from exceptions import ItemAlreadyInCart


class CartService(Service):
    repository: CartRepository

    async def is_cart_empty(self, cart_id: int) -> bool:
        return len(
            (await self.repository.get_cart_by_id(cart_id)).items
        ) == 0

    async def get_cart_by_id(self, cart_id: int) -> Cart:
        return await self.repository.get_cart_by_id(cart_id)

    async def change_user_cart(self, user: User):
        await self.repository.change_user_cart(user.id)

    async def add_item_to_cart(self, item_id: int, user: User):
        if await self.repository.is_item_in_cart(user.cart_id, item_id):
            raise ItemAlreadyInCart
        await self.repository.add_to_cart(user.cart_id, item_id)

    async def remove_item_from_cart(self, item_id: int, user: User):
        await self.repository.remove_item_from_cart(user.cart_id, item_id)

    async def edit_item_amount(self, user: User, item_id: int, amount: int):
        await self.repository.edit_item_amount(user.cart_id, item_id, amount)
