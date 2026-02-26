from fastapi import FastAPI
from database.base import Base
from database.session import engine
from routers import auth_router, superadmin_router, itadmin_router, manager_router, employee_router
from middleware.logging import LoggingMiddleware
from middleware.exception_handler import global_exception_handler, sqlalchemy_exception_handler
from sqlalchemy.exc import SQLAlchemyError
from models import user, department, asset, asset_assignment, asset_request, audit_trail, maintenance

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise Asset Management System (EAMS)")

# Middleware
app.add_middleware(LoggingMiddleware)

# Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)

# Routers
app.include_router(auth_router.router)
app.include_router(superadmin_router.router)
app.include_router(itadmin_router.router)
app.include_router(manager_router.router)
app.include_router(employee_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Enterprise Asset Management System API"}
