from sqlalchemy import update, select
from sqlalchemy.exc import SQLAlchemyError
from app.dao.base import BaseDAO
from app.users.models import User, UserRole
from app.database import async_session


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def update_role(cls, user_id: int, new_role: UserRole):
        async with async_session() as session:
            stmt = update(User).where(User.id == user_id).values(role=new_role).returning(User)
            result = await session.execute(stmt)
            await session.commit()
            updated_user = result.scalar_one_or_none()
            return updated_user