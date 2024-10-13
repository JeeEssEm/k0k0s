from pydantic import BaseModel, EmailStr, field_validator

from datetime import date


class BaseUser(BaseModel):
    fullname: str
    email: EmailStr


class CreateUser(BaseUser):
    password1: str
    password2: str
    phone: str | None = None

    @field_validator('password1', mode='after')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password2' in info.data and v != info.data['password2']:
            raise ValueError('passwords do not match')
        return v


class MiniUser(BaseUser):
    id: int


class User(MiniUser):
    joined: date
    is_admin: bool | None

    is_anonymous: bool = False
