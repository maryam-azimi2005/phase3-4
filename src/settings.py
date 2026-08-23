import json
import logging
import logging.handlers
from enum import StrEnum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 30


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    messenger_jwt_secret: str
    messenger_env: Environment = Environment.DEVELOPMENT
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(
                record,
                "%Y-%m-%d %H:%M:%S",
            ),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        return json.dumps(
            payload,
            ensure_ascii=False,
        )


def setup_logging(
    log_filename: str = "messenger-api.log",
) -> None:
    console_enabled = settings.messenger_env == Environment.DEVELOPMENT

    log_dir = Path("logs")

    log_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    root_logger = logging.getLogger()

    root_logger.setLevel(logging.DEBUG)

    if getattr(
        root_logger,
        "_messenger_configured",
        False,
    ):
        return

    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / log_filename,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.DEBUG)

    file_handler.setFormatter(JsonFormatter())

    root_logger.addHandler(file_handler)

    if console_enabled:
        console_handler = logging.StreamHandler()

        console_handler.setLevel(logging.INFO)

        console_handler.setFormatter(logging.Formatter("%(levelname)-8s %(name)s: %(message)s"))

        root_logger.addHandler(console_handler)

    root_logger._messenger_configured = True

    logger = logging.getLogger(__name__)

    logger.info(
        "Logging configured (environment=%s, console_enabled=%s)",
        settings.messenger_env.value,
        console_enabled,
    )
