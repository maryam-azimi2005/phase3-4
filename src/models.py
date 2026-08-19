from pydantic import BaseModel, Field, field_validator


def clean_username(value: str) -> str:
    value = value.strip()

    if not value.replace("_", "").isalnum():
        raise ValueError("Username may only contain letters, digits, and underscores.")

    if not value[0].isalpha():
        raise ValueError("Username must start with a letter.")

    return value


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=32,
    )
    password: str = Field(
        min_length=8,
        max_length=128,
    )

    @field_validator(
        "username",
        mode="before",
    )
    @classmethod
    def validate_username(
        cls,
        value: str,
    ) -> str:
        if not isinstance(value, str):
            return value

        return clean_username(value)


class UserResponse(BaseModel):
    id: int
    username: str


class MessageCreate(BaseModel):
    receiver: str = Field(
        min_length=3,
        max_length=32,
    )
    content: str = Field(
        min_length=1,
        max_length=2000,
    )

    @field_validator(
        "receiver",
        mode="before",
    )
    @classmethod
    def validate_receiver(
        cls,
        value: str,
    ) -> str:
        if not isinstance(value, str):
            return value

        return clean_username(value)

    @field_validator(
        "content",
        mode="before",
    )
    @classmethod
    def clean_content(
        cls,
        value: str,
    ) -> str:
        if isinstance(value, str):
            return value.strip()

        return value


class MessageResponse(BaseModel):
    id: int
    sender: str
    receiver: str
    content: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
