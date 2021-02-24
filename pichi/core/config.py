from loguru import logger
from pichi.core.logging import InterceptHandler
from starlette.config import Config
from starlette.datastructures import Secret
import logging
import sys

PROJECT_NAME = "pichi"
API_PREFIX = "/api"
VERSION = "1.0.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

AUTH0_DOMAIN: str = config("AUTH0_DOMAIN", default="")
AUTH0_API_ID: str = config("AUTH0_API_ID", default="")
AUTH0_CLIENT_ID: str = config("AUTH0_CLIENT_ID", default="")
AUTH0_CLIENT_SECRET: Secret = config("AUTH0_CLIENT_SECRET", cast=Secret)

DYNAMODB_ENDPOINT: str = config("DYNAMODB_ENDPOINT", default="")
DYNAMODB_AWS_REGION: str = config("DYNAMODB_AWS_REGION", default="")

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
