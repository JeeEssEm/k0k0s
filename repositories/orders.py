from sqlalchemy import select

import models
from .base import Repository
from schemas import (Order, CreateOrder, MiniUser, MiniItem, EditOrder,
                     MiniOrder, Cart)
from exceptions import OrderNotFound, OrderAlreadyPaid


class OrdersRepository(Repository):
    async def _convert_model_to_schema(self, order: models.Order) -> Order:
        return Order(
            id=order.id,
            comment=order.comment,
            status=order.status,
            is_paid=order.is_paid,
            cart=Cart(
                id=order.cart_id,
                items=[MiniItem(
                    id=item.item.id,
                    title=item.item.title,
                    price=item.item.price,
                    amount=item.amount
                )
                    for item in (await order.awaitable_attrs.cart).items
                ]
            ),
            user=MiniUser(
                id=order.user.id,
                fullname=order.user.fullname,
                email=order.user.email
            )
        )

    async def _get_order_by_id(self, order_id: int) -> models.Order:
        order = await self.session.get(models.Order, order_id)
        if not order:
            raise OrderNotFound
        return order

    async def get_order_by_id(self, order_id: int) -> Order:
        return await self._convert_model_to_schema(
            await self._get_order_by_id(order_id)
        )

    async def create_order(self, data: CreateOrder, user_id: int, cart_id: int) -> Order:
        order = models.Order(
            user_id=user_id,
            comment=data.comment,
            cart_id=cart_id,
        )
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return await self._convert_model_to_schema(order)

    async def edit_order(self, order_id: int, data: EditOrder) -> Order:
        order = await self._get_order_by_id(order_id)
        order.status = data.status
        await self.session.commit()
        await self.session.refresh(order)
        return await self._convert_model_to_schema(order)

    async def get_orders(self, status: models.Status | None = None) -> list[Order]:
        q = select(models.Order)
        if status:
            q = q.where(models.Order.status == status)  # noqa
        orders = await self.session.scalars(q)
        # return list(map(self._convert_model_to_schema, orders.scalars().all()))
        return [await self._convert_model_to_schema(order) for order in orders.all()]
        # TODO: pagination

    async def cancel_order(self, order_id: int):
        order = await self._get_order_by_id(order_id)
        order.status = models.Status.cancelled
        await self.session.commit()
        await self.session.refresh(order)

    async def get_user_orders(self, user_id: int) -> list[MiniOrder]:
        q = select(models.Order).where(models.Order.user_id == user_id)  # noqa
        orders = await self.session.scalars(q)

        return [MiniOrder(
            id=order.id,
            comment=order.comment,
            is_paid=order.is_paid,
            status=order.status
        )
                for order in orders.all()]

    async def purchase_order(self, order_id: int):
        order = await self._get_order_by_id(order_id)
        if order.is_paid:
            raise OrderAlreadyPaid
        order.is_paid = True
        await self.session.commit()
        await self.session.refresh(order)
