from src.exceptions import (
    CannotMessageSelfError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.models import MessageCreate, UserCreate
from src.security import hash_password, verify_password

users: list[dict] = []
messages: list[dict] = []


def get_user_by_username(
    username: str,
) -> dict | None:
    for user in users:
        if user["username"] == username:
            return user

    return None


def authenticate_user(
    username: str,
    password: str,
) -> dict | None:
    user = get_user_by_username(username)

    if user is None:
        return None

    if not verify_password(
        password,
        user["hashed_password"],
    ):
        return None

    return user


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


def create_message(
    sender: str,
    message: MessageCreate,
) -> dict:
    if get_user_by_username(sender) is None:
        raise UserNotFoundError(sender)

    if get_user_by_username(message.receiver) is None:
        raise UserNotFoundError(message.receiver)

    if sender == message.receiver:
        raise CannotMessageSelfError()

    new_message = {
        "id": len(messages) + 1,
        "sender": sender,
        "receiver": message.receiver,
        "content": message.content,
    }

    messages.append(new_message)

    return new_message


def get_messages() -> list[dict]:
    return messages.copy()
