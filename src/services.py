from src.models import MessageCreate, UserCreate

users: list[dict] = []
messages: list[dict] = []

def create_user(user: UserCreate) -> dict:
    for existing_user in users:
        if existing_user["username"] == user.username:
            raise ValueError("Username already exists")

    new_user = {
        "id": len(users) + 1,
        "username": user.username,
    }

    users.append(new_user)

    return new_user


def create_message(message: MessageCreate) -> dict:
    usernames = {user["username"] for user in users}

    if message.sender not in usernames:
        raise ValueError("Sender does not exist")

    if message.receiver not in usernames:
        raise ValueError("Receiver does not exist")

    new_message = {
        "id": len(messages) + 1,
        **message.model_dump(),
    }

    messages.append(new_message)

    return new_message


def get_messages() -> list[dict]:
    return messages.copy()