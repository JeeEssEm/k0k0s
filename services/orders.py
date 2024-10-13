from .base import Service
from repositories import OrdersRepository
from schemas import CreateOrder, Order, User, EditOrder, MiniOrder
from exceptions import NotEnoughRights


class OrdersService(Service):
    repository: OrdersRepository

    async def create_order(self, data: CreateOrder, user: User) -> Order:
        return await self.repository.create_order(data, user.id)

    async def get_order_by_id(self, order_id: int, current_user: User) -> Order:
        order = await self.repository.get_order_by_id(order_id)
        if order.user.id != current_user.id and not current_user.is_admin:
            raise NotEnoughRights
        return order

    async def edit_order(self, order_id: int, data: EditOrder) -> Order:
        return await self.repository.edit_order(order_id, data)

    async def cancel_order(self, order_id: int, current_user: User):
        order = await self.repository.get_order_by_id(order_id)
        if order.user.id != current_user.id and not current_user.is_admin:
            raise NotEnoughRights
        await self.repository.cancel_order(order_id)

    async def get_user_orders(self, user_id: int) -> list[MiniOrder]:
        return await self.repository.get_user_orders(user_id)

    async def purchase_order(self, order_id: int, current_user: User):
        order = await self.repository.get_order_by_id(order_id)
        if order.user.id != current_user.id:
            raise NotEnoughRights
        await self.repository.purchase_order(order_id)
