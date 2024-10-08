from .base import Repository
from schemas import CategorySchema, CreateCategory
from models import Category


class CategoriesRepository(Repository):
    async def get_by_id(self, cid: int):
        cat = await self.session.get(cid)
        return CategorySchema(
            id=cid,
            title=cat.title,
            is_hidden=cat.is_hidden
        )

    async def create_category(self, data: CreateCategory) -> CategorySchema:
        cat = Category(
            title=data.title,
            is_hidden=data.is_hidden
        )
        self.session.add(cat)
        await self.session.commit()
        await self.session.refresh(cat)
        return CategorySchema(
            id=cat.id,
            title=cat.title,
            is_hidden=cat.is_hidden
        )

    async def update_category(self, cid: int, data: CreateCategory) -> CategorySchema:
        cat = self.session.get(cid)
        cat.title = data.title or cat.title
        cat.is_hidden = data.is_hidden or cat.is_hidden
        await self.session.refresh(cat)
        await self.session.commit()
        return CategorySchema(
            id=cid,
            title=cat.title,
            is_hidden=cat.is_hidden
        )

    async def delete_category(self, cid: int):
        cat = self.session.get(cid)
        self.session.delete(cat)
        await self.session.commit()

