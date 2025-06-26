from app.dao.base import BaseDAO
from app.trainings.models import Training
from app.booking.models import Booking
from app.database import async_session
from sqlalchemy.orm import selectinload
from sqlalchemy import select


class TrainingDAO(BaseDAO):
    model = Training

    @classmethod
    async def find_by_trainer_with_clients(cls, trainer_id: int):
        async with async_session() as session:
            query = (select(Training)
                     .where(Training.trainer_id == trainer_id)
                     .options(selectinload(Training.bookings).selectinload(Booking.user)))
            result = await session.execute(query)
            return result.scalars().all()