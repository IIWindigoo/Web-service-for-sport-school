from fastapi import APIRouter, Response, Depends
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.auth import get_password_hash, verify_password, create_access_token
from app.users.schemas import SUserRegister, SUserAddDB
from app.users.dao import UserDAO
from app.users.models import User


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    # Проверка существования пользователя
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    user_data_dict = user_data.model_dump()
    user_data_dict.pop("confirm_password", None)
    # Добавление пользователя в БД
    await UserDAO.add(values=SUserAddDB(**user_data_dict))
    return {"message": "Вы успешно зарегистрированы"}