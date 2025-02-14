from fastapi import FastAPI

from .routers import consents

app = FastAPI()

app.include_router(consents.router)


@app.get("/")
async def root():
    return {"message": "Hello"}