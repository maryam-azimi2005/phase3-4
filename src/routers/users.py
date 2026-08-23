import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
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
def add_user(
    user: UserCreate,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    try:
        new_user = create_user(db, user)

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
