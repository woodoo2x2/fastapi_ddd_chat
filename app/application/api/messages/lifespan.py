from infrastructure.message_brokers.base import BaseMessageBroker
from logic.dependency import init_container


async def start_kafka():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.producer.start()


async def stop_kafka():
    container = init_container()
    message_broker = container.resolve(BaseMessageBroker)
    await message_broker.producer.stop()
