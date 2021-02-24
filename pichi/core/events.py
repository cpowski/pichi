from fastapi import FastAPI
from loguru import logger
from pichi.services.auth0 import Auth0Service
from typing import Callable


async def start_services(app: FastAPI) -> None:
    logger.info("Starting services")

    app.state.auth0_service = Auth0Service()

    logger.info("services started")


def startup_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await start_services(app)

    return start_app
