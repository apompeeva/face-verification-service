import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.consumer.consumer import consumer
from app.endpoints.endpoints import face_verification_router

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Запуск консьюмера перед стартом приложения и удаление после."""
    try:
        await consumer.start()
        asyncio.create_task(consumer.consume())
        yield
    except:
        yield
    finally:
        await consumer.stop()

app = FastAPI(lifespan=lifespan)

app.include_router(face_verification_router, tags=['face_verification'])
