from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.event_schema import EventCreate, EventResponse
from app.services.event_service import EventService
from app.dependencies.service_dependency import get_event_service

router = APIRouter()


@router.post("/", response_model=EventResponse, status_code=201)
def create_event(
    event_data: EventCreate,
    service: EventService = Depends(get_event_service)
):
    """Create a new event."""
    try:
        return service.create_event(event_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[EventResponse])
def list_events(
    location: Optional[str] = None,
    service: EventService = Depends(get_event_service)
):
    """List all events, optionally filtered by location."""
    return service.list_events(location=location)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    service: EventService = Depends(get_event_service)
):
    """Get a specific event by ID."""
    try:
        return service.get_event(event_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/location/{location}", response_model=List[EventResponse])
def filter_events_by_location(
    location: str,
    service: EventService = Depends(get_event_service)
):
    """Filter events by location using a path parameter."""
    return service.list_events(location=location)
