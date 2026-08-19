import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.dependencies import get_current_user
from src.exceptions import CannotMessageSelfError, UserNotFoundError
from src.models import MessageCreate, MessageResponse
from src.services import create_message, get_messages

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)

logger = logging.getLogger(__name__)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    message: MessageCreate,
    current_user: Annotated[
        dict,
        Depends(get_current_user),
    ],
):
    try:
        new_message = create_message(
            sender=current_user["username"],
            message=message,
        )

        logger.info(
            "Message sent from '%s' to '%s'.",
            current_user["username"],
            message.receiver,
        )

        return new_message

    except UserNotFoundError as error:
        logger.warning(
            "Message sending failed: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except CannotMessageSelfError as error:
        logger.warning(
            "Message sending failed: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get(
    "",
    response_model=list[MessageResponse],
)
def list_messages(
    current_user: Annotated[
        dict,
        Depends(get_current_user),
    ],
    with_user: Annotated[
        str | None,
        Query(
            min_length=3,
            max_length=32,
        ),
    ] = None,
):
    try:
        return get_messages(
            username=current_user["username"],
            with_user=with_user,
        )

    except UserNotFoundError as error:
        logger.warning(
            "Message listing failed: %s",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
