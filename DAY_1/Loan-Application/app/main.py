from fastapi import FastAPI
from app.controllers import loan_controller
from app.middleware.cors import setup_cors
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# Setup Middleware
setup_cors(app)

# Include Routers
app.include_router(loan_controller.router)

@app.get("/")
def health_check():
    return {"status": "healthy", "service": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
