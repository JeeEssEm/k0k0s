from .base import Repository
from schemas import ItemSchema, CreateItem
from models import Item


class ItemsRepository(Repository):
    async def get_by_id(self, item_id: int) -> ItemSchema:
        item = self.session.get(item_id)
        return ItemSchema(
            id=item_id,
            title=item.title,
            description=item.description,
            is_hidden=item.is_hidden,
            amount=item.amount,
            price=item.price
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
        return ItemSchema(
                ...
        )
