import logging
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from src.settings import (
    JWT_ALGORITHM,
    JWT_EXPIRE_MINUTES,
    settings,
)

logger = logging.getLogger(__name__)

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    username: str,
) -> str:
    now = datetime.now(UTC)

    expires_at = now + timedelta(
        minutes=JWT_EXPIRE_MINUTES,
    )

    payload = {
        "sub": username,
        "iat": now,
        "exp": expires_at,
        "jti": secrets.token_urlsafe(16),
    }

    token = jwt.encode(
        payload,
        settings.messenger_jwt_secret,
        algorithm=JWT_ALGORITHM,
    )

    logger.debug(
        "Access token created for user '%s'.",
        username,
    )

    return token


def decode_access_token(
    token: str,
) -> dict[str, Any]:
    payload = jwt.decode(
        token,
        settings.messenger_jwt_secret,
        algorithms=[JWT_ALGORITHM],
        options={
            "require": [
                "sub",
                "exp",
                "jti",
            ]
        },
    )

    logger.debug("Access token decoded successfully.")

    return payload
