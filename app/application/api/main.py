from fastapi import FastAPI
from application.api.messages.handlers import router as messages_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='Simple Kafka Chat',
        docs_url='/api/docs',
        description='DDD + Kafka example',
        debug=True
    )
    app.include_router(messages_router)
    return app

