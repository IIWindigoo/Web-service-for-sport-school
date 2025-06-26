from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует')

IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail='Неверная почта или пароль')

TokenExpiredException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail='Токен истек')

TokenNoFound = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Token not found')

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='Токен не валидный!')

NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Не найден ID пользователя')

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                   detail='Недостаточно прав!')

TrainingNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                 detail="Тренировка не найдена")

TrainingForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                           detail="Нет доступа к этой тренировкe")

BookingOnlyClient = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                  detail="Только клиенты могут записываться")

BookingExist = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Вы уже записаны")