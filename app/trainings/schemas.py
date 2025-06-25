from pydantic import BaseModel, Field, ConfigDict
from datetime import date, time


class STrainingAdd(BaseModel):
    title: str = Field(min_length=2, max_length=50, description="Название тренировки, от 2 до 50 символов")
    description: str = Field(min_length=5, max_length=256, description="Описание тренировки, от 5 до 256 символов")
    date: date
    start_time: time
    end_time: time

    model_config = ConfigDict(from_attributes=True)

class STrainingInfo(STrainingAdd):
    id: int = Field(description="id тренировки")

    model_config = ConfigDict(from_attributes=True)

