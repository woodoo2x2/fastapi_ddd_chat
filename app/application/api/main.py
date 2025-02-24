from contextlib import asynccontextmanager

from fastapi import FastAPI

from application.api.messages.handlers import router as messages_router
from application.api.messages.lifespan import start_kafka, stop_kafka


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_kafka()
    yield
    await stop_kafka()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Simple Kafka Chat",
        docs_url="/api/docs",
        description="DDD + Kafka example",
        debug=True,
        lifespan=lifespan,
    )
    app.include_router(messages_router)
    return app
