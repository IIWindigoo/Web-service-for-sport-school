from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.users.router import router as router_users
from app.trainings.router import router as router_trainings
from app.booking.router import router as router_bookings
from app.pages.router import router as router_pages


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), "static")

@app.get("/")
async def top():
    return {"message": "top page"}

app.include_router(router_users)
app.include_router(router_trainings)
app.include_router(router_bookings)
app.include_router(router_pages)