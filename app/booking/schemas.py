from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.trainings.schemas import STrainingShort

class SBookingAdd(BaseModel):
    training_id: int = Field(description="ID тренировки")

class SBookingAddFull(SBookingAdd):
    user_id: int = Field(description="ID клиента")

class SBookingInfo(BaseModel):
    id: int = Field(description="ID записи")
    created_at: datetime = Field(description="Дата записи")
    training: STrainingShort = Field(description="Информация о тренировке")

    model_config = ConfigDict(from_attributes=True)