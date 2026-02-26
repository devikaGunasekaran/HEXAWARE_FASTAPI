from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import BusinessRuleViolation, NotFoundError, UnauthorizedOperation


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def handle_not_found(_: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"error": exc.message})

    @app.exception_handler(BusinessRuleViolation)
    async def handle_rule_violation(_: Request, exc: BusinessRuleViolation):
        return JSONResponse(status_code=400, content={"error": exc.message})

    @app.exception_handler(UnauthorizedOperation)
    async def handle_unauthorized(_: Request, exc: UnauthorizedOperation):
        return JSONResponse(status_code=403, content={"error": exc.message})
