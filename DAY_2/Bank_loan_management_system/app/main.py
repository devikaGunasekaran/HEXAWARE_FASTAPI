import logging

from fastapi import FastAPI

from app.controllers.application_controller import router as application_router
from app.controllers.product_controller import router as product_router
from app.controllers.repayment_controller import router as repayment_router
from app.controllers.user_controller import router as user_router
from app.exceptions.exception_handlers import register_exception_handlers
from app.middleware.cors import configure_cors
from app.middleware.logging_middleware import LoggingMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def create_app() -> FastAPI:
    app = FastAPI(title="Banking Loan Management System", version="1.0.0")

    configure_cors(app)
    app.add_middleware(LoggingMiddleware)

    app.include_router(user_router, prefix="/users", tags=["users"])
    app.include_router(product_router, prefix="/loan-products", tags=["loan-products"])
    app.include_router(application_router, prefix="/loan-applications", tags=["loan-applications"])
    app.include_router(repayment_router, tags=["repayments"])

    register_exception_handlers(app)
    return app


app = create_app()
