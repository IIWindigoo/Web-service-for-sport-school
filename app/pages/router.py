from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from datetime import date, time, datetime, timezone
from typing import Any
import locale

from app.trainings.router import get_trainings
from app.users.dependencies import get_current_user_or_none
from app.users.models import User


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
    return templates.TemplateResponse(template_name, context)

templates.env.filters["format_date"] = format_date
templates.env.filters["format_time"] = format_time

@router.get("/")
async def home_page(request: Request, 
                    trainings=Depends(get_trainings)):
    return render_template(request,
                           template_name="index.html",
                           context={
                                "trainings": trainings,
                                "now": datetime.now(timezone.utc).timestamp(),
                                })