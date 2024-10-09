from sqlalchemy import select

import models
from .base import Repository
from schemas import Order, CreateOrder, ShortUser, Item, Category
from exceptions import OrderNotFound


class OrdersRepository(Repository):
    def _convert_model_to_schema(self, order: models.Order) -> Order:
        return Order(
            id=order.id,
            item_id=order.item_id,
            comment=order.comment,
            item=Item(
                id=order.item.id,
                title=order.item.title,
                description=order.item.description,
                is_hidden=order.item.is_hidden,
                amount=order.item.amount,
                price=order.item.price,
                category=Category(
                    id=order.item.category.id,
                    title=order.item.category.title,
                    is_hidden=order.item.category.is_hidden
                )
            ),
            user=ShortUser(
                id=order.user.id,
                fullname=order.user.fullname,
                email=order.user.email,
            )
        )

    async def _get_order_by_id(self, order_id: int) -> models.Order:
        order = await self.session.get(models.Order, order_id)
        if not order:
            raise OrderNotFound
        return order

    async def get_order_by_id(self, order_id: int) -> Order:
        return self._convert_model_to_schema(
            await self._get_order_by_id(order_id)
        )

    async def create_order(self, data: CreateOrder, user_id: int) -> Order:
        order = models.Order(
            item_id=data.item.id,
            user_id=user_id,
            comment=data.comment
        )
        await self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return self._convert_model_to_schema(order)

    async def update_order(self, order_id: int, data: CreateOrder) -> Order:
        order = await self._get_order_by_id(order_id)
        order.status = data.status
        await self.session.commit()
        await self.session.refresh(order)
        return self._convert_model_to_schema(order)

    async def get_orders(self, status: models.Status | None = None) -> list[Order]:
        q = select(models.Order)
        if status:
            q = q.where(models.Order.status == status)
        orders = await self.session.execute(q)
        return list(map(self._convert_model_to_schema, orders.scalars().all()))
        # TODO: pagination
