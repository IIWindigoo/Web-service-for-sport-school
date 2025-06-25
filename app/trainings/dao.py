from app.dao.base import BaseDAO
from app.trainings.models import Training


class TrainingDAO(BaseDAO):
    model = Training