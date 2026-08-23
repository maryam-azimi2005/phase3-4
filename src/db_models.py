from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    sent_messages: Mapped[list["MessageDB"]] = relationship(
        back_populates="sender",
        foreign_keys="MessageDB.sender_id",
    )
    received_messages: Mapped[list["MessageDB"]] = relationship(
        back_populates="receiver",
        foreign_keys="MessageDB.receiver_id",
    )


class MessageDB(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    receiver_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    sender: Mapped["UserDB"] = relationship(
        back_populates="sent_messages",
        foreign_keys=[sender_id],
    )
    receiver: Mapped["UserDB"] = relationship(
        back_populates="received_messages",
        foreign_keys=[receiver_id],
    )
