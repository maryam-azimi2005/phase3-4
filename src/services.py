from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.db_models import MessageDB, UserDB
from src.exceptions import (
    CannotMessageSelfError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.models import MessageCreate, UserCreate
from src.security import hash_password, verify_password


def _user_to_dict(user: UserDB) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "hashed_password": user.hashed_password,
    }


def _message_to_dict(message: MessageDB) -> dict:
    return {
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
    }


def get_user_by_username(
    db: Session,
    username: str,
) -> dict | None:
    user = db.scalar(select(UserDB).where(UserDB.username == username))

    if user is None:
        return None

    return _user_to_dict(user)


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> dict | None:
    user = db.scalar(select(UserDB).where(UserDB.username == username))

    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return _user_to_dict(user)


def create_user(
    db: Session,
    user: UserCreate,
) -> dict:
    existing_user = db.scalar(select(UserDB).where(UserDB.username == user.username))

    if existing_user is not None:
        raise UserAlreadyExistsError(user.username)

    new_user = UserDB(
        username=user.username,
        hashed_password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return _user_to_dict(new_user)


def create_message(
    db: Session,
    sender: str,
    message: MessageCreate,
) -> dict:
    sender_user = db.scalar(select(UserDB).where(UserDB.username == sender))

    if sender_user is None:
        raise UserNotFoundError(sender)

    receiver_user = db.scalar(select(UserDB).where(UserDB.username == message.receiver))

    if receiver_user is None:
        raise UserNotFoundError(message.receiver)

    if sender == message.receiver:
        raise CannotMessageSelfError()

    new_message = MessageDB(
        sender_id=sender_user.id,
        receiver_id=receiver_user.id,
        content=message.content,
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return _message_to_dict(new_message)


def get_messages(
    db: Session,
    username: str,
    with_user: str | None = None,
) -> list[dict]:
    user = db.scalar(select(UserDB).where(UserDB.username == username))

    if user is None:
        raise UserNotFoundError(username)

    if with_user is None:
        query = select(MessageDB).where(
            (MessageDB.sender_id == user.id) | (MessageDB.receiver_id == user.id)
        )
    else:
        other_user = db.scalar(select(UserDB).where(UserDB.username == with_user))

        if other_user is None:
            raise UserNotFoundError(with_user)

        query = select(MessageDB).where(
            ((MessageDB.sender_id == user.id) & (MessageDB.receiver_id == other_user.id))
            | ((MessageDB.sender_id == other_user.id) & (MessageDB.receiver_id == user.id))
        )

    query = query.options(
        selectinload(MessageDB.sender),
        selectinload(MessageDB.receiver),
    ).order_by(MessageDB.id)

    result = db.scalars(query).all()

    return [_message_to_dict(message) for message in result]
