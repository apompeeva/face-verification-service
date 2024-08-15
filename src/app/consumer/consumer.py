from aiokafka import AIOKafkaConsumer
import asyncio
from app.config import KAFKA_HOST, KAFKA_PORT, TOPIC
import brotli
import logging
from app.core.service import FaceVerificationService

event_loop = asyncio.get_event_loop()  # ???
file_encoding = "utf-8"
file_compression_quality = 1


class Consumer(object):
    def __init__(self):
        self.__consumer = AIOKafkaConsumer(TOPIC,
                                           bootstrap_servers=f"{
                                               KAFKA_HOST}:{KAFKA_PORT}",
                                           loop=event_loop,
                                           )

    async def start(self) -> None:
        await self.__consumer.start()

    async def stop(self) -> None:
        await self.__consumer.stop()

    async def decompress(self, file_bytes: bytes) -> str:
        """Decompress message from Kafka."""

        return str(
            brotli.decompress(file_bytes),
            file_encoding,
        )

    async def consume(self):
        """Consume and print messages from Kafka."""
        async for msg in self.__consumer:
            value = await self.decompress(msg.value)
            user_id, img_path = value.split(':')
            embedding = FaceVerificationService.verify_user(img_path, int(user_id))
            if embedding is not None:
                logging.info(f'face_vector: {str(embedding[0]['embedding'])}')
            else:
                logging.info(f'Unable get face vector for id: {user_id}')

    async def health_check(self) -> bool:
        """Checks if Kafka is available by fetching all metadata from the Kafka client."""
        try:
            await self.__consumer.client.fetch_all_metadata()
        except Exception as exc:
            logging.error(f'Kafka is not available: {exc}')
        else:
            return True
        return False


def get_consumer() -> Consumer:
    return Consumer()


consumer = get_consumer()
