from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import time
from datetime import date as dt


class STrainingAdd(BaseModel):
    title: str = Field(min_length=2, max_length=50, description="Название тренировки, от 2 до 50 символов")
    description: str = Field(min_length=5, max_length=256, description="Описание тренировки, от 5 до 256 символов")
    date: dt = Field(desription="Дата проведения тренировки")
    start_time: time = Field(description="Время начала тренировки")
    end_time: time = Field(description="Время окончания тренировки")
    trainer_id: int = Field(description="ID тренера")

    model_config = ConfigDict(from_attributes=True)

class STrainingInfo(STrainingAdd):
    id: int = Field(description="id тренировки")

class STrainingUpd(BaseModel):
    title: str | None = None
    description: str | None = None
    date: dt | None = None 
    start_time: time | None = None
    end_time: time | None = None