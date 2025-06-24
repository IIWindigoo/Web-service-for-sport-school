from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls):
        async with async_session() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def update(cls, filter_by, **values):
        async with async_session() as session:
            async with session.begin():
                stmt = (
                    update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(stmt)
                try:
                    session.commit()
                except SQLAlchemyError as e:
                    session.rollback()
                    raise e
                return result.rowcount
    
    @classmethod
    async def add(cls, **values):
        async with async_session() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance
    
    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        if not delete_all and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления")
        async with async_session() as session:
            async with session.begin():
                stmt = delete(cls.model).filter_by(**filter_by)
                result = await session.execute(stmt)
                try:
                    session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount