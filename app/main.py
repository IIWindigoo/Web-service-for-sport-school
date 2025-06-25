from fastapi import FastAPI
from app.users.router import router as router_users


app = FastAPI()

@app.get("/")
async def top():
    return {"message": "top page"}

app.include_router(router_users)