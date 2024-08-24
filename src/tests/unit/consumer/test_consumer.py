import logging
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.consumer.consumer import Consumer
from app.core.service import FaceVerificationService


async def test_consume(mocker, caplog):
    LOGGER = logging.getLogger("app.consumer.consumer")
    LOGGER.propagate = True
    caplog.set_level(logging.INFO)

    consumer_mock = AsyncMock()
    consumer_mock.__aiter__.return_value = [
        MagicMock(value=b'1:/path/to/image')
    ]

    decompress_mock = mocker.patch(
        'app.consumer.consumer.brotli.decompress', return_value=b'1:/path/to/image')

    # Создаем мок для метода verify_user
    verify_user_mock = mocker.patch(
        'app.consumer.consumer.FaceVerificationService.verify_user', return_value=[{'embedding': [1, 2, 3]}])

    # Создаем экземпляр класса с моками
    with patch('app.consumer.consumer.AIOKafkaConsumer', return_value=consumer_mock):
        consumer = Consumer()
        await consumer.consume()

    # Проверяем, что методы были вызваны с правильными аргументами
    decompress_mock.assert_called_once_with(b'1:/path/to/image')
    verify_user_mock.assert_called_once_with('/path/to/image', 1)

    # Проверяем, что логи содержат ожидаемое сообщение
    assert 'face_vector: [1, 2, 3]' in caplog.text
