from schemas import Item, CreateItem, ShortUser, Category
from .base import Service
from repositories import ItemsRepository
from exceptions import ItemNotFound


class ItemsService(Service):
    repository: ItemsRepository

    async def create_item(self, data: CreateItem) -> Item:
        return await self.repository.create_item(data)

    async def get_item_by_id(self, item_id: int, current_user: ShortUser) -> Item:
        item = await self.repository.get_item_by_id(item_id)
        if (item.is_hidden and not current_user.is_admin) or item.is_deleted:
            raise ItemNotFound
        return item

    async def edit_item(self, item_id: int, data: CreateItem) -> Item:
        item = await self.repository.get_item_by_id(item_id)
        if item.is_deleted:
            raise ItemNotFound
        return await self.repository.edit_item(item_id, data)

    async def delete_item(self, item_id: int):
        item = await self.repository.get_item_by_id(item_id)
        if item.is_deleted:
            raise ItemNotFound
        await self.repository.delete_item(item_id)

    async def get_items_by_category(self, category: Category, current_user: ShortUser) -> list[Item]:
        return await self.repository.get_items_by_category(
            category, current_user.is_admin
        )
