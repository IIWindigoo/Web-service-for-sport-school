import re
from typing import Self
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator, model_validator
from enum import Enum
from app.users.auth import get_password_hash

class UserRole(str, Enum):
    client = "client"
    admin = "admin"
    trainer = "trainer"

class EmailModel(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    model_config = ConfigDict(from_attributes=True)

class UserBase(EmailModel):
    phone_number: str = Field(description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")

    @field_validator("phone_number")
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{5,15}$', value):
            raise ValueError("Номер телефона должен начинаться с '+' и содержать от 5 до 15 цифр")
        return value

class SUserRegister(UserBase):
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 символов")
    confirm_password: str = Field(min_length=5, max_length=50, description="Повторите пароль")
    role: UserRole = UserRole.client

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Пароли не совпадают")
        self.password = get_password_hash(self.password)
        return self