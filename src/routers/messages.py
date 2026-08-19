import logging

from fastapi import APIRouter, HTTPException, status

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
def send_message(message: MessageCreate):
    try:
        new_message = create_message(message)

        logger.info(
            "Message sent from %s to %s",
            message.sender,
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
def list_messages():
    return get_messages()
