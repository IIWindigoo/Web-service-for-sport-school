from fastapi import APIRouter, Depends
from app.booking.dao import BookingDAO
from app.booking.schemas import SBookingAdd, SBookingInfo, SBookingAddFull
from app.users.models import User, UserRole
from app.users.dependencies import get_current_user
from app.trainings.dao import TrainingDAO
from app.exceptions import BookingExist, BookingOnlyClient, TrainingNotFound


router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", summary="Записаться на тренировку", response_model=SBookingInfo)
async def create_booking(booking_data: SBookingAdd,
                         user_data: User = Depends(get_current_user)):
    if user_data.role != UserRole.client:
        raise BookingOnlyClient
    training = await TrainingDAO.find_one_or_none_by_id(booking_data.training_id)
    if not training:
        raise TrainingNotFound
    existing = await BookingDAO.find_by_user(user_data.id)
    if any(b.training_id == booking_data.training_id for b in existing):
        raise BookingExist
    
    booking = await BookingDAO.add(SBookingAddFull(training_id=booking_data.training_id, 
                                                   user_id=user_data.id))
    return booking

@router.get("/", summary="Мои записи", response_model=list[SBookingInfo])
async def get_user_bookings(user_data: User = Depends(get_current_user)):
    return await BookingDAO.find_by_user(user_data.id)

@router.delete("/", summary="Отменить запись", status_code=204)
async def cancel_booking(booking_data: SBookingAdd,
                         user_data: User = Depends(get_current_user)):
    await BookingDAO.delete(user_id=user_data.id, training_id=booking_data.training_id)