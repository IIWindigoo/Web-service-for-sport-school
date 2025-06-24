from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def top():
    return {"message": "top page"}  