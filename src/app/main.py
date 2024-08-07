from fastapi import FastAPI

from app.endpoints.endpoints import face_verification_router

app = FastAPI()

app.include_router(face_verification_router, tags=['face_verification'])
