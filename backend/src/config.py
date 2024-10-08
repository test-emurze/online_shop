import logging
import os
from enum import Enum
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings

LOG_FORMAT_DEBUG = (
    "%(levelname)s:     %(message)s  %(pathname)s:%(funcName)s:%(lineno)d"
)
DEFAULT_LOG_FORMAT = "%(levelname)s:     %(message)s"


class LogLevel(str, Enum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    debug = "DEBUG"


def configure_logging(log_level: str | None, debug: bool) -> None:
    if not log_level:
        log_level = LogLevel.debug if debug else LogLevel.warning

    log_level = log_level.upper()

    if log_level not in list(LogLevel):
        # We use LogLevel.error as the default log level
        logging.basicConfig(level=LogLevel.error)

    elif log_level == LogLevel.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)

    else:
        logging.basicConfig(level=log_level, format=DEFAULT_LOG_FORMAT)


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    # FastAPI
    api_v1_prefix: str = "/api/v1"
    app_title: str = "App"
    allowed_origins: list[str] = [
        "http://localhost:3000",
    ]
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    version: str = "0.0.0"
    secret_key: SecretStr = "secret"
    debug: bool = True
    log_level: LogLevel | None = None
    base_dir: Path = Path(__file__).parent

    # Postgres
    pool_size: int = 10
    pool_max_overflow: int = 0
    db_echo: bool = False
    db_dsn: str = "postgresql+asyncpg://postgres:password@db:5432/postgres"
    redis_dsn: str = "redis://db:6379/0"


def get_db_dsn_for_environment(app_config: AppConfig = AppConfig()) -> str:
    """
    Get database url for entrypoint inside docker container or localhost.
    Allows you to run your commands outside container.
    """

    if os.getenv("IS_DOCKER_CONTAINER"):
        return app_config.db_dsn

    return app_config.db_dsn.replace("db", "localhost")


config = AppConfig()  # global
