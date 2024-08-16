import pytest
from unittest.mock import AsyncMock, MagicMock
import logging
from app.consumer.consumer import Consumer
from app.core.service import FaceVerificationService


async def test_consume_success(mocker, caplog):
    # Создаем мок для консьюмера
    consumer_mock = AsyncMock()
    consumer_mock.__aiter__.return_value = [
        MagicMock(value=b'1:/path/to/image')
    ]

    # Создаем мок для метода decompress
    decompress_mock = AsyncMock(return_value='1:/path/to/image')

    # Создаем мок для метода verify_user
    verify_user_mock = mocker.patch.object(
        FaceVerificationService, 'verify_user', return_value=[{'embedding': [1, 2, 3]}])

    # Создаем экземпляр класса с моками
    consumer = Consumer(consumer_mock)
    consumer.decompress = decompress_mock

    # Вызываем метод consume
    await consumer.consume()

    # Проверяем, что методы были вызваны с правильными аргументами
    decompress_mock.assert_called_once_with(b'1:/path/to/image')
    verify_user_mock.assert_called_once_with('/path/to/image', 1)

    # Проверяем, что логи содержат ожидаемое сообщение
    assert 'face_vector: [1, 2, 3]' in caplog.text
