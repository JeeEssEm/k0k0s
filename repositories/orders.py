from .base import Repository
from models import Order
from schemas import OrderSchema, CreateOrder, ShortUser, ItemSchema, CategorySchema
from exceptions import OrderNotFound
from models import Status

from sqlalchemy import select


class OrdersRepository(Repository):
    async def _convert_model_to_schema(self, order: Order) -> OrderSchema:
        return OrderSchema(
            id=order.id,
            item_id=order.item_id,
            comment=order.comment,
            item=ItemSchema(
                id=order.item.id,
                title=order.item.title,
                description=order.item.description,
                is_hidden=order.item.is_hidden,
                amount=order.item.amount,
                price=order.item.price,
                category=CategorySchema(
                    id=order.item.category.id,
                    title=order.item.category.title,
                    is_hidden=order.item.category.is_hidden
                )
            ),
            user=ShortUser(
                id=order.user.id,
                fullname=order.user.name,
                email=order.user.email,
            )
        )

    async def _get_order_by_id(self, order_id: int) -> Order:
        order = await self.session.get(Order, order_id)
        if not order:
            raise OrderNotFound
        return order

    async def get_order_by_id(self, order_id: int) -> OrderSchema:
        return await self._convert_model_to_schema(
            await self._get_order_by_id(order_id)
        )

    async def create_order(self, data: CreateOrder, user_id: int) -> OrderSchema:
        order = Order(
            item_id=data.item.id,
            user_id=user_id,
            comment=data.comment
        )
        await self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return await self._convert_model_to_schema(order)

    async def update_order(self, order_id: int, data: CreateOrder) -> OrderSchema:
        order = await self._get_order_by_id(order_id)
        order.status = data.status
        await self.session.commit()
        await self.session.refresh(order)
        return await self._convert_model_to_schema(order)

    async def get_orders(self, status: Status | None = None) -> list[OrderSchema]:
        q = select(Order)
        if status:
            q = q.where(Order.status == status)
        orders = await self.session.execute(q)
        res = []
        for order in orders.scalars().all():  # TODO: pagination
            res.append(await self._convert_model_to_schema(order))
        return res
