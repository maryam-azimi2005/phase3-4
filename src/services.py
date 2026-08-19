from src.exceptions import (
    CannotMessageSelfError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.models import MessageCreate, UserCreate
from src.security import hash_password

users: list[dict] = []
messages: list[dict] = []


def get_user_by_username(
    username: str,
) -> dict | None:
    for user in users:
        if user["username"] == username:
            return user

    return None


def create_user(user: UserCreate) -> dict:
    if get_user_by_username(user.username) is not None:
        raise UserAlreadyExistsError(user.username)

    new_user = {
        "id": len(users) + 1,
        "username": user.username,
        "hashed_password": hash_password(user.password),
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
