from app.dao.base import BaseDAO
from app.booking.models import Booking
from app.database import async_session
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def find_by_user(cls, user_id: int):
        async with async_session() as session:
            query = (select(Booking)
                     .options(selectinload(Booking.training))
                     .where(Booking.user_id == user_id))
            result = await session.execute(query)
            return result.scalars().all()