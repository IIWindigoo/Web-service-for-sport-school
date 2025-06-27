from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from datetime import date, time, datetime, timezone
import locale

from app.trainings.router import get_trainings


locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

router = APIRouter(prefix="/page", tags=["Фронтэнд"])
templates = Jinja2Templates(directory="app/templates")

# Форматирование даты
def format_date(value: date):
    return value.strftime("%d %B (%A)")

# Форматирование времени
def format_time(value: time):
    return value.strftime("%H:%M")

templates.env.filters["format_date"] = format_date
templates.env.filters["format_time"] = format_time

@router.get("/")
async def home_page(request: Request, trainings=Depends(get_trainings)):
    return templates.TemplateResponse(name="index.html",
                                      context={
                                          "request": request,
                                          "trainings": trainings,
                                          "now": datetime.now(timezone.utc).timestamp()
                                      })