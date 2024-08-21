from deepface import DeepFace  # type: ignore

from app.crud.face_verification import add_vector, verify_user


class FaceVerificationService:
    """Cервис преобразования лица на фото в вектор."""

    embedding_storage: dict = {}

    @staticmethod
    def get_embedding(img_path: str):
        """Генерация вектора на основе фотографии."""
        return DeepFace.represent(img_path=img_path, model_name='Facenet')

    @classmethod
    async def verify_user(cls, img_path: str, user_id: int):
        """Верификация пользователя."""
        try:
            embedding = cls.get_embedding(img_path)
        except ValueError:
            return None
        await add_vector(
            {
                'user_id': user_id,
                'embedding': str(embedding[0]['embedding']),
                'path_to_image': img_path,
            },
        )
        await verify_user(user_id)
        return embedding
