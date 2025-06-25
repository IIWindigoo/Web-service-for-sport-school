from fastapi import Depends, Request, HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timezone
from app.users.dao import UserDAO
from app.users.models import User
from app.config import settings
from app.exceptions import (TokenExpiredException, TokenNoFound, NoJwtException, 
                            NoUserIdException, ForbiddenException)


def get_access_token(request: Request):
    # Извлечение токена из кук
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNoFound
    return token

async def get_current_user(token: str = Depends(get_access_token)) -> User:
    # Проверяем токен и возвращаем пользователя
    try:
        # Декодируем токен
        auth_data = settings.get_auth_data
        payload = jwt.decode(token, auth_data["secret_key"], algorithms=auth_data["algorithm"])
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise NoJwtException
    
    expire: str = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise NoUserIdException
    
    user = await UserDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found")
    return user

async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    # Проверка пользователя на права админа
    if current_user.role == "admin":
        return current_user
    raise ForbiddenException

async def get_current_trainer_user(current_user: User = Depends(get_current_user)):
    # Проверка пользователя на права тренера
    if current_user.role == "trainer":
        return current_user
    raise ForbiddenException