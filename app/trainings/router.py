from fastapi import APIRouter, Depends, HTTPException
from app.trainings.schemas import STrainingInfo, STrainingAdd
from app.trainings.dao import TrainingDAO
from app.users.models import User, UserRole
from app.users.dependencies import role_required
from app.users.dao import UserDAO


router = APIRouter(prefix="/trainings", tags=["Trainings"])

@router.get("/", summary="Получить все тренировки")
async def get_trainings() -> list[STrainingInfo]:
    return await TrainingDAO.find_all()

@router.post("/", summary="Создать тренировку")
async def create_training(training_data: STrainingAdd, 
                          user_data: User = Depends(role_required([UserRole.admin, UserRole.trainer]))
                          ) -> STrainingInfo | dict:
    # Проверка: только admin может создавать тренировку для другого тренера
    if user_data.role == UserRole.trainer and training_data.trainer_id != user_data.id:
        raise HTTPException(status_code=403, detail="Тренер может создавать только свои тренировки")
    
    # Проверка: существует ли тренер
    trainer = await UserDAO.find_one_or_none_by_id(training_data.trainer_id)
    if not trainer or trainer.role != UserRole.trainer:
        raise HTTPException(status_code=404, detail="Указанный тренер не найден или не является тренером")

    new_training = await TrainingDAO.add(values=training_data)
    if new_training:
        return STrainingInfo.model_validate(new_training)
    return {"message": "Ошибка при добавлении заметки"}