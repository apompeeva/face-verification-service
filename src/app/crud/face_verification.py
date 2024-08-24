from app.database import async_session_maker
from app.models.face_verification_models import FaceDataModel, Users


async def add_vector(vector_dict: dict):
    """Добавление записи в таблицу faces."""
    async with async_session_maker() as session:
        db_vector = FaceDataModel(**vector_dict)
        session.add(db_vector)
        await session.commit()


async def verify_user(user_id: int):
    """Изменение поля is_verified на True по user_id."""
    async with async_session_maker() as session:
        user = await session.get(Users, user_id)
        user.is_verified = True
        await session.commit()
