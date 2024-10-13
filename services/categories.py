from .base import Service
from repositories import CategoriesRepository
from schemas import Category, ShortUser, CreateCategory
from exceptions import CategoryNotFound


class CategoriesService(Service):
    repository: CategoriesRepository

    async def get_category_by_id(self, category_id: int, current_user: ShortUser) -> Category:
        category = await self.repository.get_category_by_id(category_id)
        if (category.is_hidden and not current_user.is_admin) or category.is_deleted:
            raise CategoryNotFound
        return category

    async def get_categories(self, current_user: ShortUser) -> list[Category]:
        return await self.repository.get_categories(current_user.is_admin)

    async def edit_category(self, category_id: int, data: CreateCategory) -> Category:
        category = await self.repository.get_category_by_id(category_id)
        if category.is_deleted:
            raise CategoryNotFound
        return await self.repository.edit_category(category_id, data)

    async def create_category(self, data: CreateCategory) -> Category:
        return await self.repository.create_category(data)

    async def delete_category(self, category_id: int):
        category = await self.repository.get_category_by_id(category_id)
        if category.is_deleted:
            raise CategoryNotFound
        await self.repository.delete_category(category_id)
