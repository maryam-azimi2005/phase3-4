import logging

from fastapi import FastAPI

from src.routers import (
    auth,
    messages,
    users,
)
from src.settings import setup_logging


setup_logging(
    log_filename="api.log"
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Messenger API",
    version="0.2.0",
)


app.include_router(
    users.router
)

app.include_router(
    auth.router
)

app.include_router(
    messages.router
)


@app.on_event("startup")
def startup_event() -> None:
    logger.info(
        "Messenger API started."
    )


@app.on_event("shutdown")
def shutdown_event() -> None:
    logger.info(
        "Messenger API stopped."
    )


@app.get("/")
def root():
    logger.debug(
        "Root endpoint requested."
    )

    return {
        "message": "Messenger API is running"
    }