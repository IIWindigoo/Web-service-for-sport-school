from fastapi import APIRouter, Response, Depends, HTTPException
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.auth import create_access_token, authenticate_user
from app.users.schemas import SUserRegister, SUserAddDB, SUserAuth, SUserInfo, SUserRoleUpd
from app.users.dao import UserDAO
from app.users.models import User, UserRole
from app.users.dependencies import (get_current_user, role_required)


router = APIRouter(prefix="/user", tags=["Auth"])

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

@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if not (user and await authenticate_user(user=user, password=user_data.password)):
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"ok": True, "message": "Авторизация успешна"}

@router.post("/logout")
async def logout_user(response: Response) -> dict:
    response.delete_cookie("users_access_token")
    return {"message": "Пользователь успешно вышел из системы"}

@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)) -> SUserInfo:
    return SUserInfo.model_validate(user_data)

@router.get("/all_users/")
async def get_all_users(user_data: User = Depends(role_required(["admin"]))) -> list[SUserInfo]:
    return await UserDAO.find_all()

@router.patch("/{user_id}/role", summary="Изменить роль пользователя")
async def change_user_role(user_id: int, 
                           role_data: SUserRoleUpd, 
                           user_data: User = Depends(role_required([UserRole.admin]))
                           ) -> dict:
    if user_data.id == user_id:
        raise HTTPException(status_code=403, detail="Админ не может менять свою роль")
    
    user = await UserDAO.find_one_or_none_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    updated_user = await UserDAO.update_role(user_id=user_id, new_role=role_data.new_role)
    return {"message": f"Роль пользователя {user_id} обновлена: {updated_user.role.value}"}