from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk, str_uniq


class UserRole(str, Enum):
    client = "client"
    admin = "admin"
    trainer = "trainer"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str_uniq]
    email: Mapped[str_uniq]
    password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), default=UserRole.client)
    trainings: Mapped[list["Training"]] = relationship(back_populates="trainer", cascade="all, delete-orphan") # type: ignore