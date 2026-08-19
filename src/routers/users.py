import logging

from fastapi import APIRouter, HTTPException, status

from src.exceptions import UserAlreadyExistsError
from src.models import UserCreate, UserResponse
from src.services import create_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

logger = logging.getLogger(__name__)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_user(user: UserCreate):
    try:
        new_user = create_user(user)

        logger.info(
            "User created: %s",
            user.username,
        )

        return new_user

    except UserAlreadyExistsError as error:
        logger.warning(
            "User registration failed: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error
