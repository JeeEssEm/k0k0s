from .base import Service
from repositories import CategoriesRepository
from schemas import Category


class CategoriesService(Service):
    repository: CategoriesRepository

    async def get_category_by_id(self, category_id: int) -> Category:
        # ... some validations
        return await self.repository.get_category_by_id(category_id)

    async def get_categories(self) -> list[Category]:
        return await self.repository.get_public_categories()
