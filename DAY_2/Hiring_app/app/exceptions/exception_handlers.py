from fastapi import Request
from fastapi.responses import JSONResponse
from .custom_exceptions import HiringAppException
from ..core.logger import logger

async def hiring_app_exception_handler(request: Request, exc: HiringAppException):
    logger.error(f"Error occurred: {exc.name} - {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.name, "message": exc.message},
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "InternalServerError", "message": "An unexpected error occurred."},
    )
