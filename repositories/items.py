from .base import Repository
from schemas import ItemSchema, CreateItem, CategorySchema
from models import Item
from exceptions import ItemNotFound


class ItemsRepository(Repository):
    async def _convert_model_to_schema(self, item: Item) -> ItemSchema:
        return ItemSchema(
            id=item.id,
            title=item.title,
            description=item.description,
            is_hidden=item.is_hidden,
            amount=item.amount,
            price=item.price,
            category=CategorySchema(
                id=item.category.id,
                title=item.category.title,
                is_hidden=item.category.is_hidden
            )
        )

    async def _get_item_by_id(self, item_id: int) -> Item:
        item = await self.session.get(Item, item_id)
        if not item:
            raise ItemNotFound
        return item

    async def get_item_by_id(self, item_id: int) -> ItemSchema:
        return await self._convert_model_to_schema(
            await self._get_item_by_id(item_id)
        )

    async def create_item(self, data: CreateItem) -> ItemSchema:
        item = Item(
            title=data.title,
            description=data.description,
            is_hidden=data.is_hidden,
            amount=data.amount,
            price=data.price
        )
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return await self._convert_model_to_schema(item)

    async def update_item(self, item_id: int, data: CreateItem) -> ItemSchema:
        item = await self._get_item_by_id(item_id)
        item.title = data.title or item.title
        item.description = data.description or item.description
        item.is_hidden = data.is_hidden or item.is_hidden
        item.amount = data.amount or item.amount
        item.price = data.price or item.price

        await self.session.commit()
        await self.session.refresh(item)
        return await self._convert_model_to_schema(item)

    async def delete_item(self, item_id: int) -> None:
        item = await self._get_item_by_id(item_id)
        item.deleted = True
        await self.session.commit()
        await self.session.refresh(item)
