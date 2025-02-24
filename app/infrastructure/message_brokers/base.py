from abc import ABC, abstractmethod
from dataclasses import dataclass

from aiokafka import AIOKafkaProducer


@dataclass
class BaseMessageBroker(ABC):
    producer: AIOKafkaProducer

    @abstractmethod
    async def send_message(self, key:bytes, topic: str, value: bytes) -> None: ...

    @abstractmethod
    async def consume(self, topic: str): ...
