import threading

from src.exceptions import (
    CannotMessageSelfError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.models import MessageCreate, UserCreate
from src.security import hash_password, verify_password

users: list[dict] = []
messages: list[dict] = []

_users_lock = threading.RLock()
_messages_lock = threading.RLock()


def get_user_by_username(
    username: str,
) -> dict | None:
    with _users_lock:
        for user in users:
            if user["username"] == username:
                return user.copy()

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


def create_user(
    user: UserCreate,
) -> dict:
    hashed_password = hash_password(user.password)

    with _users_lock:
        for existing_user in users:
            if existing_user["username"] == user.username:
                raise UserAlreadyExistsError(user.username)

        new_user = {
            "id": len(users) + 1,
            "username": user.username,
            "hashed_password": hashed_password,
        }

        users.append(new_user)

        return new_user.copy()


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

    with _messages_lock:
        new_message = {
            "id": len(messages) + 1,
            "sender": sender,
            "receiver": message.receiver,
            "content": message.content,
        }

        messages.append(new_message)

        return new_message.copy()


def get_messages(
    username: str,
    with_user: str | None = None,
) -> list[dict]:
    if get_user_by_username(username) is None:
        raise UserNotFoundError(username)

    if with_user is not None and get_user_by_username(with_user) is None:
        raise UserNotFoundError(with_user)

    with _messages_lock:
        if with_user is None:
            result = [
                message
                for message in messages
                if (message["sender"] == username or message["receiver"] == username)
            ]

        else:
            result = [
                message
                for message in messages
                if (
                    (message["sender"] == username and message["receiver"] == with_user)
                    or (message["sender"] == with_user and message["receiver"] == username)
                )
            ]

        return [message.copy() for message in result]
