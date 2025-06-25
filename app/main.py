from fastapi import FastAPI
from app.users.router import router as router_users
from app.trainings.router import router as router_trainings


app = FastAPI()

@app.get("/")
async def top():
    return {"message": "top page"}

app.include_router(router_users)
app.include_router(router_trainings)