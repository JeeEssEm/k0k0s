from sqlalchemy import select, and_

from .base import Repository
from schemas import Item, CreateItem, Category, CategoryItems, MiniItem
import models
from exceptions import ItemNotFound


class ItemsRepository(Repository):
    def _convert_model_to_schema(self, item: models.Item) -> Item:
        item = Item(
            id=item.id,
            title=item.title,
            description=item.description,
            is_hidden=item.is_hidden,
            is_deleted=item.is_deleted,
            amount=item.amount,
            price=item.price,
            category=Category(
                id=item.category.id,
                title=item.category.title,
                is_hidden=item.category.is_hidden,
                is_deleted=item.category.is_deleted
            )
        )
        return item

    def _convert_category_items_to_schema(self, items: list[models.Item],
                                          category: Category) -> CategoryItems:
        return CategoryItems(
            id=category.id,
            title=category.title,
            is_hidden=category.is_hidden,
            is_deleted=category.is_deleted,
            items=[
                MiniItem(
                    id=item.id,
                    title=item.title,
                    price=item.price
                )
                for item in items
            ]
        )

    async def _get_item_by_id(self, item_id: int) -> models.Item:
        item = await self.session.get(models.Item, item_id)
        if not item:
            raise ItemNotFound
        return item

    async def get_item_by_id(self, item_id: int) -> Item:
        return self._convert_model_to_schema(
            await self._get_item_by_id(item_id)
        )

    async def create_item(self, data: CreateItem) -> Item:
        item = models.Item(
            title=data.title,
            description=data.description,
            is_hidden=data.is_hidden,
            amount=data.amount,
            price=data.price
        )
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return self._convert_model_to_schema(item)

    async def edit_item(self, item_id: int, data: CreateItem) -> Item:
        item = await self._get_item_by_id(item_id)
        item.title = data.title or item.title
        item.description = data.description or item.description
        item.is_hidden = data.is_hidden or item.is_hidden
        item.amount = data.amount or item.amount
        item.price = data.price or item.price

        await self.session.commit()
        await self.session.refresh(item)
        return self._convert_model_to_schema(item)

    async def delete_item(self, item_id: int):
        item = await self._get_item_by_id(item_id)
        item.deleted = True
        await self.session.commit()
        await self.session.refresh(item)

    async def get_items_by_category(
            self, category: Category,
            hidden_included: bool
    ) -> CategoryItems:
        q = select(models.Item).where(and_(
            models.Item.category_id == category.id,
            models.Item.is_deleted == False
        ))  # noqa
        if not hidden_included:
            q = q.where(models.Item.is_hidden == False)  # noqa
        items = await self.session.scalars(q)
        return self._convert_category_items_to_schema(items.all(), category)
