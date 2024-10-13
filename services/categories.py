from .base import Service
from repositories import CategoriesRepository
from schemas import Category, ShortUser
from exceptions import CategoryNotFound


class CategoriesService(Service):
    repository: CategoriesRepository

    async def get_category_by_id(self, category_id: int, current_user: ShortUser) -> Category:
        category = await self.repository.get_category_by_id(category_id)
        if category.is_hidden and not current_user.is_admin:
            raise CategoryNotFound
        return category

    async def get_categories(self) -> list[Category]:
        return await self.repository.get_public_categories()
