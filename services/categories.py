from .base import Service
from repositories import CategoriesRepository
from schemas import CategorySchema


class CategoriesService(Service):
    repository: CategoriesRepository

    async def get_category_by_id(self, category_id: int) -> CategorySchema:
        # ... some validations
        return await self.repository.get_category_by_id(category_id)
