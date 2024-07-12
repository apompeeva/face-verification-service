import pytest

from app.main import FaceVerificationService


@pytest.mark.parametrize('path', (
    pytest.param('src/tests/unit/images/img.jpg', id='woman'),
    pytest.param('src/tests/unit/images/s1200.jpeg', id='two_people')
))
def test_get_embedding(path):
    img_path = path

    embedding_objs = FaceVerificationService.get_embedding(img_path)

    for embedding_obj in embedding_objs:
        embedding = embedding_obj['embedding']
        assert isinstance(embedding, list)
        assert (len(embedding) == 128)


def test_get_embedding_invalid_image():
    img_path = 'path/to/invalid/image.jpg'

    with pytest.raises(ValueError):
        FaceVerificationService.get_embedding(img_path)
