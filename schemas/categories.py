from pydantic import BaseModel


class CreateCategory(BaseModel):
    title: str
    is_hidden: bool


class CategorySchema(CreateCategory):
    id: int

