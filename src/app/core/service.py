from deepface import DeepFace  # type: ignore


class FaceVerificationService:
    """Cервис преобразования лица на фото в вектор."""

    embedding_storage: dict = {}

    @staticmethod
    def get_embedding(img_path: str):
        """Генерация вектора на основе фотографии."""
        return DeepFace.represent(img_path=img_path, model_name='Facenet')

    @classmethod
    def verify_user(cls, img_path: str, user_id: int):
        """Верификация пользователя."""
        try:
            embedding = cls.get_embedding(img_path)
        except ValueError:
            return None
        cls.embedding_storage.update({user_id: embedding})
        return embedding
