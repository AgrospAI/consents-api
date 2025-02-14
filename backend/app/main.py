from fastapi import FastAPI

from app.api.main import api_router

app = FastAPI()

app.include_router(api_router)


# https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/models.py
