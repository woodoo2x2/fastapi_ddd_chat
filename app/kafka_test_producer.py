import asyncio

from aiokafka import AIOKafkaProducer


async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers="kafka:29092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("test-topic", b"Super chats message")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


asyncio.run(send_one())
