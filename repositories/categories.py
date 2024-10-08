from .base import Repository
from schemas import (CategorySchema, CreateCategory, CategoryItemsSchema,
                     ItemSchema)
from models import Category
from exceptions import CategoryNotFound

from sqlalchemy import select, and_


class CategoriesRepository(Repository):
    async def _convert_model_to_schema(self, category: Category) -> CategorySchema:
        return CategorySchema(
            id=category.id,
            title=category.title,
            is_hidden=category.is_hidden
        )

    async def _get_category_by_id(self, cid: int) -> Category:
        cat = await self.session.get(Category, cid)
        if not cat:
            raise CategoryNotFound
        return cat

    async def get_category_by_id(self, cid: int) -> CategorySchema:
        return await self._convert_model_to_schema(
            await self._get_category_by_id(cid)
        )

    async def create_category(self, data: CreateCategory) -> CategorySchema:
        cat = Category(
            title=data.title,
            is_hidden=data.is_hidden
        )
        self.session.add(cat)
        await self.session.commit()
        await self.session.refresh(cat)
        return await self._convert_model_to_schema(cat)

    async def update_category(self, cid: int, data: CreateCategory) -> CategorySchema:
        cat = await self._get_category_by_id(cid)
        cat.title = data.title or cat.title
        cat.is_hidden = data.is_hidden or cat.is_hidden
        await self.session.refresh(cat)
        await self.session.commit()
        return await self._convert_model_to_schema(cat)

    async def delete_category(self, cid: int):
        cat = await self._get_category_by_id(cid)
        cat.deleted = True
        await self.session.commit()
        await self.session.refresh(cat)

    async def get_category_items(self, cid: int) -> CategoryItemsSchema:
        cat = await self._get_category_by_id(cid)
        items = []
        for item in cat.items:
            items.append(ItemSchema(
                id=item.id,
                title=item.title,
                description=item.description,
                is_hidden=item.is_hidden,
                amount=item.amount,
                price=item.price
            ))
        return CategoryItemsSchema(
            id=cat.id,
            title=cat.title,
            is_hidden=cat.is_hidden,
            items=items
        )

    async def get_public_categories(self) -> list[CategorySchema]:
        q = select(Category).where(and_(
            Category.is_hidden == False, Category.deleted == False  # noqa
        ))
        categories = await self.session.execute(q)
        res = []
        for category in categories.scalars().all():  # TODO: pagination
            res.append(await self._convert_model_to_schema(category))
        return res
