from fastapi import APIRouter, Depends
from app.trainings.schemas import STrainingInfo, STrainingAdd
from app.trainings.dao import TrainingDAO
from app.users.models import User
from app.users.dependencies import role_required


router = APIRouter(prefix="/trainings", tags=["Trainings"])

@router.get("/", summary="Получить все тренировки")
async def get_trainings() -> list[STrainingInfo]:
    return await TrainingDAO.find_all()

@router.post("/", summary="Создать тренировку")
async def create_training(training_data: STrainingAdd, 
                          user_data: User = Depends(role_required(["admin", "trainer"]))
                          ) -> STrainingInfo | dict:
    new_training = await TrainingDAO.add(**training_data.model_dump())
    if new_training:
        return STrainingInfo.model_validate(new_training)
    return {"message": "Ошибка при добавлении заметки"}