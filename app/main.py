from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.middleware.auth import AuthMiddleware
from app.users.router import router as router_users
from app.trainings.router import router as router_trainings
from app.booking.router import router as router_bookings
from app.pages.router import router as router_pages
from app.pages.router import templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), "static")

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 403:
        return templates.TemplateResponse(
            "errors/403.html",
            {"request": request, "detail": exc.detail},
            status_code=exc.status_code
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get("/")
async def top():
    return {"message": "top page"}

app.add_middleware(AuthMiddleware)
app.include_router(router_users)
app.include_router(router_trainings)
app.include_router(router_bookings)
app.include_router(router_pages)