import logging

from fastapi import FastAPI, HTTPException, status

from src.models import (
    MessageCreate,
    MessageResponse,
    UserCreate,
    UserResponse,
)
from src.services import create_message, create_user, get_messages


app = FastAPI(
    title="Messenger API",
    version="0.1.0",
)

logger = logging.getLogger("uvicorn.error")


@app.get("/")
def root():
    return {"message": "Messenger API is running"}


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_user(user: UserCreate):
    try:
        new_user = create_user(user)

        logger.info("User created: %s", user.username)

        return new_user

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@app.post(
    "/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_message(message: MessageCreate):
    try:
        new_message = create_message(message)

        logger.info(
            "Message sent from %s to %s",
            message.sender,
            message.receiver,
        )

        return new_message

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@app.get(
    "/messages",
    response_model=list[MessageResponse],
)
def list_messages():
    return get_messages()