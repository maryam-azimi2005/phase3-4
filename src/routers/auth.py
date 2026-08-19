import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies import get_current_user
from src.models import TokenResponse, UserResponse
from src.security import create_access_token
from src.services import authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

logger = logging.getLogger(__name__)


@router.post(
    "/token",
    response_model=TokenResponse,
)
def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
):
    user = authenticate_user(
        form_data.username,
        form_data.password,
    )

    if user is None:
        logger.warning(
            "Failed login attempt for user '%s'.",
            form_data.username,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    access_token = create_access_token(user["username"])

    logger.info(
        "User '%s' logged in successfully.",
        user["username"],
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: Annotated[
        dict,
        Depends(get_current_user),
    ],
):
    return current_user
