from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class Category(str, Enum):
    personal = "personal"
    work = "work"
    family = "family"


class ContactCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: str
    phone: Optional[str] = Field(default=None, min_length=10, max_length=15)
    category: Category

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email must contain '@'")
        return value


class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    email: Optional[str] = None
    phone: Optional[str] = Field(default=None, min_length=10, max_length=15)
    category: Optional[Category] = None

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and "@" not in value:
            raise ValueError("email must contain '@'")
        return value


class ContactResponse(ContactCreate):
    id: int
    created_at: str
