import logging

from fastapi import APIRouter, HTTPException, status

from src.models import UserCreate, UserResponse
from src.services import create_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

logger = logging.getLogger("uvicorn.error")


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_user(user: UserCreate):
    try:
        new_user = create_user(user)

        logger.info("User created: %s", user.username)

        return new_user

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error