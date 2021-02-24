from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from pichi.api.errors.http_error import http_error_handler
from pichi.api.errors.validation_error import http422_error_handler
from pichi.api.routes.api import router as api_router
from pichi.core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from pichi.core.events import startup_handler


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.add_event_handler("startup", startup_handler(application))

    application.include_router(api_router, prefix=API_PREFIX)

    return application


app = get_application()
