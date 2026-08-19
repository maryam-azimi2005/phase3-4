class UserAlreadyExistsError(Exception):
    def __init__(self, username: str) -> None:
        super().__init__(f"User '{username}' already exists.")


class UserNotFoundError(Exception):
    def __init__(self, username: str) -> None:
        super().__init__(f"User '{username}' not found.")


class CannotMessageSelfError(Exception):
    def __init__(self) -> None:
        super().__init__("You cannot send a private message to yourself.")
