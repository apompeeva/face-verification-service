from fastapi import APIRouter, HTTPException, status

from app.core.service import FaceVerificationService
from app.consumer.consumer import consumer

face_verification_router = APIRouter()


@face_verification_router.post(
    '/verify', status_code=status.HTTP_200_OK,
)
async def verify_user(user_id: int, path: str):
    """Верификация пользователя."""
    embedding = FaceVerificationService.verify_user(path, user_id)
    if embedding is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid path',
        )


@face_verification_router.get('/healthz/ready')
async def health_check():
    """Проверка работоспособности сервиса."""
    return status.HTTP_200_OK
