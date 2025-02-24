from dataclasses import dataclass

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    # consumer: AIOKafkaConsumer

    async def send_message(self, topic: str, value: bytes) -> None:
        await self.producer.start()
        await self.producer.send_and_wait(topic=topic, value=value)

    async def consume(self, topic: str): ...
