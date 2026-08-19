from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from src.security import decode_access_token
from src.services import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = decode_access_token(token)
        username = payload.get("sub")

        if not isinstance(username, str):
            raise credentials_exception

    except InvalidTokenError as error:
        raise credentials_exception from error

    user = get_user_by_username(username)

    if user is None:
        raise credentials_exception

    return user
