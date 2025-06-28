from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from app.database import async_session


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, filters: BaseModel | None = None):
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_dict)
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
    async def add(cls, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        async with async_session() as session:
            async with session.begin():
                new_instance = cls.model(**values_dict)
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