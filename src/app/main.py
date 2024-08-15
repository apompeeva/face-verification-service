from fastapi import FastAPI

from app.endpoints.endpoints import face_verification_router
from app.consumer.consumer import consumer
from contextlib import asynccontextmanager
import asyncio
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logging.info("Starting up...")
        await consumer.start()
        asyncio.create_task(consumer.consume())
        yield
    except:
        yield
    finally:
        await consumer.stop()

app = FastAPI(lifespan=lifespan)

app.include_router(face_verification_router, tags=['face_verification'])
