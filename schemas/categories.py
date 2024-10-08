from pydantic import BaseModel
from .items import CreateItem


class CreateCategory(BaseModel):
    title: str
    is_hidden: bool


class CategorySchema(CreateCategory):
    id: int


class ItemSchema(CreateItem):
    id: int
    category: CategorySchema | None
    # это сюда попало из-за circular import


class CategoryItemsSchema(CategorySchema):
    items: list[ItemSchema]
