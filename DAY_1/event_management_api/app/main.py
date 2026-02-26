from fastapi import FastAPI
from app.controllers.event_controller import router as event_router
from app.controllers.participant_controller import router as participant_router
from app.middleware.cors_middleware import add_cors_middleware

app = FastAPI(
    title="Event Management API",
    description="A clean-architecture FastAPI backend for managing events and participants.",
    version="1.0.0"
)

# Apply CORS middleware
add_cors_middleware(app)

# Register routers
app.include_router(event_router, prefix="/events", tags=["Events"])
app.include_router(participant_router, prefix="/participants", tags=["Participants"])


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Event Management API is running"}
