from src.exceptions import (
    CannotMessageSelfError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.models import MessageCreate, UserCreate

users: list[dict] = []
messages: list[dict] = []


def create_user(user: UserCreate) -> dict:
    for existing_user in users:
        if existing_user["username"] == user.username:
            raise UserAlreadyExistsError(user.username)

    new_user = {
        "id": len(users) + 1,
        "username": user.username,
    }

    users.append(new_user)

    return new_user


def create_message(message: MessageCreate) -> dict:
    usernames = {user["username"] for user in users}

    if message.sender not in usernames:
        raise UserNotFoundError(message.sender)

    if message.receiver not in usernames:
        raise UserNotFoundError(message.receiver)

    if message.sender == message.receiver:
        raise CannotMessageSelfError()

    new_message = {
        "id": len(messages) + 1,
        **message.model_dump(),
    }

    messages.append(new_message)

    return new_message


def get_messages() -> list[dict]:
    return messages.copy()
