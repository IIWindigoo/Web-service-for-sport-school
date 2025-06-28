from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import date, time, datetime, timezone
from typing import Any
import locale

from app.trainings.router import get_my_trainings, get_trainings
from app.trainings.models import Training
from app.booking.router import get_user_bookings
from app.users.dependencies import role_required
from app.users.schemas import SUserFilter
from app.users.models import UserRole, User
from app.users.dao import UserDAO
from app.users.router import get_all_users
from app.database import async_session


locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

router = APIRouter(prefix="/page", tags=["Фронтэнд"])
templates = Jinja2Templates(directory="app/templates")

# Форматирование даты
def format_date(value: date):
    return value.strftime("%d %B (%A)")

# Форматирование времени
def format_time(value: time):
    return value.strftime("%H:%M")

def render_template(request: Request, template_name: str, context: dict[str, Any]):
    context["request"] = request
    context["user"] = getattr(request.state, "user", None)
    context["now"] = datetime.now(timezone.utc).timestamp()
    return templates.TemplateResponse(template_name, context)

templates.env.filters["format_date"] = format_date
templates.env.filters["format_time"] = format_time

@router.get("/")
async def home_page(request: Request):
    async with async_session() as session:
        query = select(Training).options(joinedload(Training.trainer))
        result = await session.execute(query)
        trainings = result.unique().scalars().all()

        trainers = []
        if request.state.user and request.state.user.role == UserRole.admin:
            trainers = await UserDAO.find_all(SUserFilter(role=UserRole.trainer))

        return render_template(request,
                            template_name="index.html",
                            context={
                                    "trainings": trainings,
                                    "trainers": trainers,
                                    })

@router.get("/me_trainer/")
async def get_me_trainer_page(request: Request,
                      trainings=Depends(get_my_trainings),
                      user_data: User = Depends(role_required([UserRole.trainer]))):
    return render_template(request,
                           template_name="account_trainer.html",
                           context={
                               "trainings": trainings,
                           })

@router.get("/me/")
async def get_me_page(request: Request,
                      bookings=Depends(get_user_bookings)):
    return render_template(request,
                           template_name="account.html",
                           context={
                               "bookings": bookings,
                           })

@router.get("/me_admin")
async def get_me_admin_page(request: Request,
                      users=Depends(get_all_users),
                      user_data: User = Depends(role_required([UserRole.admin]))):
    
    # Получаем все тренировки с тренерами
    async with async_session() as session:
        query = select(Training).options(joinedload(Training.trainer))
        result = await session.execute(query)
        trainings = result.unique().scalars().all()

    return render_template(request,
                           template_name="account_admin.html",
                           context={
                               "trainings": trainings,
                               "users": users,
                               "current_user_id": user_data.id
                           })