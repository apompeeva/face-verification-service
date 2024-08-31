import asyncio
import logging

import brotli
from aiokafka import AIOKafkaConsumer

from app.config import KAFKA_HOST, KAFKA_PORT, TOPIC
from app.core.service import FaceVerificationService

event_loop = asyncio.get_event_loop()  # ???
file_encoding = 'utf-8'
file_compression_quality = 1


class Consumer:
    """Класс для чтения сообщений из kafka."""

    def __init__(self):
        """Инициализация консьюмера."""
        self.__consumer = AIOKafkaConsumer(
            TOPIC,
            bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}',
            loop=event_loop,
        )

    async def start(self) -> None:
        """Запуск консьюмера."""
        await self.__consumer.start()

    async def stop(self) -> None:
        """Остановка консьюмера."""
        await self.__consumer.stop()

    async def decompress(self, file_bytes: bytes) -> str:
        """Распаковка сообщение от Кафки."""
        return str(
            brotli.decompress(file_bytes),
            file_encoding,
        )

    async def consume(self):
        """Получение и печать сообщения от Kafka."""
        async for msg in self.__consumer:
            msg_value = await self.decompress(msg.value)
            user_id, img_path = msg_value.split('@')
            embedding = await FaceVerificationService.verify_user(
                img_path,
                int(user_id),
            )
            if embedding is not None:
                logging.info(f"face_vector: {str(embedding[0]['embedding'])}")
            else:
                logging.info(f'Unable get face vector for id: {user_id}')

    async def health_check(self) -> bool:
        """Проверяет, доступен ли Kafka, получая все метаданные от клиента Kafka."""
        try:
            await self.__consumer.client.fetch_all_metadata()
        except Exception as exc:
            logging.error(f'Kafka is not available: {exc}')
        else:
            return True
        return False


def get_consumer() -> Consumer:
    """Получение экземпляра класса Consumer."""
    return Consumer()


consumer = get_consumer()
