from fastapi import FastAPI, Request
from routers.auth_router import router as auth_router
from routers.admin_router import router as admin_router
from routers.manager_router import router as manager_router
from routers.employee_router import router as employee_router
from middleware.logging import LoggingMiddleware
from middleware.exception_handler import custom_exception_handler
from database.session import engine
from database.base import Base
import models.user, models.department, models.leave_request

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise Leave Management System (ELMS)")

# Add Middleware
app.add_middleware(LoggingMiddleware)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return await custom_exception_handler(request, exc)

# Include Routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(manager_router)
app.include_router(employee_router)

@app.get("/")
def root():
    return {"message": "Welcome to ELMS API"}
