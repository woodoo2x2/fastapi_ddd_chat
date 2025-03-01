from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv("../../.env")


class Settings(BaseSettings):
    MONGO_DB_PATH: str = Field(default="mongodb://localhost:27017")
    MONGO_DB_DATABASE_NAME: str = Field(default="chat")
    MONGO_DB_CHAT_COLLECTION_NAME: str = Field(default="chat")
    MONGO_DB_MESSAGES_COLLECTION_NAME: str = Field(default="messages")

    NEW_MESSAGE_EVENTS_TOPIC : str = Field(default="new-messages-topic")
    NEW_CHAT_EVENTS_TOPIC: str = Field(default="new-chat-topic")

    KAFKA_URL: str = Field(default="kafka:29092")
