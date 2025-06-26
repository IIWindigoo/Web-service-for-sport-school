from fastapi import APIRouter, Depends, HTTPException
from app.trainings.schemas import STrainingInfo, STrainingAdd, STrainingUpd
from app.trainings.dao import TrainingDAO
from app.users.models import User, UserRole
from app.users.dependencies import role_required, get_current_user
from app.users.dao import UserDAO
from app.exceptions import TrainingNotFound, TrainingForbiddenException


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

@router.patch("/{training_id}/", summary="Редактировать тренировку")
async def update_training(training_id: int,
                          data: STrainingUpd,
                          user_data: User = Depends(get_current_user)
                          ) -> STrainingInfo:
    training = await TrainingDAO.find_one_or_none_by_id(training_id)
    if not training:
        raise TrainingNotFound
    if user_data.role != UserRole.admin and training.trainer_id != user_data.id:
        raise TrainingForbiddenException
    
    updated_count = await TrainingDAO.update(
        {"id": training_id},
        **data.model_dump(exclude_unset=True)
    )

    if updated_count == 0:
        raise HTTPException(status_code=400, detail="Обновление не выполнено")
    updated = await TrainingDAO.find_one_or_none_by_id(training_id)
    return STrainingInfo.model_validate(updated)

@router.delete("/{training_id}/", summary="Удалить тренировку")
async def delete_training(training_id: int,
                          user_data: User = Depends(get_current_user)) -> dict:
    training = await TrainingDAO.find_one_or_none_by_id(training_id)
    if not training:
        raise TrainingNotFound
    if user_data.role != UserRole.admin and training.trainer_id != user_data.id:
        raise TrainingForbiddenException
    
    deleted_count = await TrainingDAO.delete(id=training_id)
    if deleted_count:
        return {"message": f"Тренировка {training_id} успешно удалена"}
    return {"message": "Ошибка при удалении тренировки"}