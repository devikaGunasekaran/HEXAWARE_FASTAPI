from fastapi import FastAPI
from .core.config import settings
from .controllers import user_controller, job_controller, application_controller
from .middleware.cors import add_cors_middleware
from .middleware.logging import logging_middleware
from .exceptions.custom_exceptions import HiringAppException
from .exceptions.exception_handlers import hiring_app_exception_handler, global_exception_handler
from .core.database import Base, engine

# Create tables (Note: In production use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Middleware
add_cors_middleware(app)
app.middleware("http")(logging_middleware)

# Exception Handlers
app.add_exception_handler(HiringAppException, hiring_app_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Routers
app.include_router(user_controller.router)
app.include_router(job_controller.router)
app.include_router(application_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hiring Application API"}
