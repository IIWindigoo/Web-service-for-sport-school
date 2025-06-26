from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, time
from app.database import Base, int_pk, str_uniq

class Training(Base):
    __tablename__ = "trainings"

    id: Mapped[int_pk]
    title: Mapped[str]
    description: Mapped[str] = mapped_column(Text)
    date: Mapped[date]
    start_time: Mapped[time]
    end_time: Mapped[time]
    trainer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    trainer: Mapped["User"] = relationship(back_populates="trainings") # type: ignore
    bookings: Mapped[list["Booking"]] = relationship(back_populates="training", cascade="all, delete-orphan") # type: ignore