from aiokafka import AIOKafkaConsumer
import asyncio
from app.config import KAFKA_BOOTSTRAP_SERVERS, TOPIC
import brotli

event_loop = asyncio.get_event_loop()  # ???
file_encoding = "utf-8"
file_compression_quality = 1


class Consumer(object):
    def __init__(self):
        self.__consumer = AIOKafkaConsumer(TOPIC,
                                           bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
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

        while True:
            async for msg in self.__consumer:
                print(
                    "consumed: ",
                    f"topic: {msg.topic},",
                    f"partition: {msg.partition},",
                    f"offset: {msg.offset},",
                    f"key: {msg.key},",
                    f"value: {await self.decompress(msg.value)},",
                    f"timestamp: {msg.timestamp}",
                )

    async def health_check(self) -> bool:
        """Checks if Kafka is available by fetching all metadata from the Kafka client."""
        try:
            await self.__consumer.client.fetch_all_metadata()
        except Exception as exc:
            pass  # logging.error(f'Kafka is not available: {exc}')
        else:
            return True
        return False


def get_consumer() -> Consumer:
    return Consumer()


consumer = get_consumer()
