from dataclasses import dataclass

from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    # consumer: AIOKafkaConsumer

    async def send_message(self, key: bytes, topic: str, value: bytes) -> None:
        await self.producer.send(topic=topic, key=key, value=value)

    async def consume(self, topic: str): ...
