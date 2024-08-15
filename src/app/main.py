from fastapi import FastAPI

from app.endpoints.endpoints import face_verification_router
from app.consumer.consumer import consumer
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer.start()
    consumer.consume()
    yield
    consumer.stop()

app = FastAPI()

app.include_router(face_verification_router, tags=['face_verification'])
