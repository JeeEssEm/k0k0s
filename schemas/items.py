from pydantic import BaseModel, Field


class CreateItem(BaseModel):
    title: str
    description: str | None = Field(default=0)
    price: int | None = Field(default=0)
    amount: int | None = Field(default=0)
    is_hidden: bool | None = Field(default=False)


class ItemSchema(CreateItem):
    id: int
