from sqlalchemy import select

from .base import Repository
import models
from schemas import Cart, MiniItem
from exceptions import ItemNotInCart


class CartRepository(Repository):
    def _convert_model_to_schema(self, items: list[models.CartItem], cart_id: int) -> Cart:
        return Cart(
            id=cart_id,
            items=[MiniItem(
                id=cart_item.item.id,
                title=cart_item.item.title,
                price=cart_item.item.price,
                amount=cart_item.amount
            ) for cart_item in items]
        )

    async def get_cart_by_id(self, cart_id: int) -> Cart:
        q = select(models.CartItem).where(models.CartItem.cart_id == cart_id)
        res = (await self.session.scalars(q)).all()
        return self._convert_model_to_schema(res, cart_id)

    async def change_user_cart(self, user_id: int):
        # привязывание новой пустой корзины к пользователю
        cart = models.Cart()
        user = await self.session.get(models.User, user_id)
        user.cart = cart
        self.session.add(cart)
        await self.session.commit()
        await self.session.refresh(user)

    async def _get_cart_item(self, cart_id: int, item_id: int) -> models.CartItem:
        cart_item = await self.session.get(models.CartItem, {
            'cart_id': cart_id, 'item_id': item_id
        })
        return cart_item

    async def _get_existing_cart_item(self, cart_id: int, item_id: int) -> models.CartItem:
        cart_item = await self._get_cart_item(cart_id, item_id)
        if not cart_item:
            raise ItemNotInCart
        return cart_item

    async def is_item_in_cart(self, cart_id: int, item_id: int) -> bool:
        cart_item = await self._get_cart_item(cart_id, item_id)
        return cart_item is not None

    async def add_to_cart(self, cart_id: int, item_id: int):
        cart_item = models.CartItem(
            item_id=item_id,
            cart_id=cart_id,
            amount=1
        )
        self.session.add(cart_item)
        await self.session.commit()
        await self.session.refresh(cart_item)

    async def remove_item_from_cart(self, cart_id: int, item_id: int):
        q = await self._get_existing_cart_item(cart_id, item_id)
        await self.session.delete(q)
        await self.session.commit()

    async def edit_item_amount(self, cart_id: int, item_id: int, amount: int):
        cart_item = await self._get_existing_cart_item(cart_id, item_id)
        cart_item.amount = amount

        await self.session.commit()
