from deepface import DeepFace  # type: ignore


class FaceVerificationService:
    """Cервис преобразования лица на фото в вектор."""

    @staticmethod
    def get_embedding(img_path: str):
        """Генерация вектора на основе фотографии."""
        return DeepFace.represent(img_path=img_path, model_name='Facenet')


if __name__ == '__main__':
    FaceVerificationService.get_embedding('src/app/img.jpg')
