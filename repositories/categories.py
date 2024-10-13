from .base import Repository
from schemas import (Category, CreateCategory, CategoryItems, Item)
import models
from exceptions import CategoryNotFound

from sqlalchemy import select, and_


class CategoriesRepository(Repository):
    def _convert_model_to_schema(self, category: models.Category) -> Category:
        return Category(
            id=category.id,
            title=category.title,
            is_hidden=category.is_hidden,
            is_deleted=category.deleted
        )

    async def _get_category_by_id(self, cid: int) -> Category:
        cat = await self.session.get(models.Category, cid)
        if not cat:
            raise CategoryNotFound
        return cat

    async def get_category_by_id(self, cid: int) -> Category:
        return self._convert_model_to_schema(
            await self._get_category_by_id(cid)
        )

    async def create_category(self, data: CreateCategory) -> Category:
        cat = models.Category(
            title=data.title,
            is_hidden=data.is_hidden
        )
        self.session.add(cat)
        await self.session.commit()
        await self.session.refresh(cat)
        return self._convert_model_to_schema(cat)

    async def edit_category(self, cid: int, data: CreateCategory) -> Category:
        cat = await self._get_category_by_id(cid)
        cat.title = data.title or cat.title
        cat.is_hidden = data.is_hidden or cat.is_hidden
        await self.session.commit()
        await self.session.refresh(cat)
        return self._convert_model_to_schema(cat)

    async def delete_category(self, cid: int):
        cat = await self._get_category_by_id(cid)
        cat.deleted = True
        await self.session.commit()
        await self.session.refresh(cat)

    async def get_category_items(self, cid: int) -> CategoryItems:
        cat = await self._get_category_by_id(cid)
        items = [Item(
                id=item.id,
                title=item.title,
                description=item.description,
                is_hidden=item.is_hidden,
                amount=item.amount,
                price=item.price
            ) for item in cat.items]

        return CategoryItems(
            id=cat.id,
            title=cat.title,
            is_hidden=cat.is_hidden,
            items=items
        )

    async def get_categories(self, hidden_included: bool) -> list[Category]:
        q = select(models.Category).where(models.Category.deleted == False)  # noqa

        if not hidden_included:
            q = q.where(models.Category.is_hidden == False)  # noqa
        categories = await self.session.scalars(q)
        return list(map(
            self._convert_model_to_schema, categories.all())
        )
