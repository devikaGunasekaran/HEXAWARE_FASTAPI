from typing import List, Optional
from app.repositories.event_repository import EventRepository
from app.schemas.event_schema import EventCreate, EventResponse


class EventService:

    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def create_event(self, event_data: EventCreate) -> EventResponse:
        # Business rule: Prevent duplicate event names
        existing = self.event_repo.find_by_name(event_data.name)
        if existing:
            raise ValueError(f"An event with the name '{event_data.name}' already exists.")
        return self.event_repo.save(event_data)

    def list_events(self, location: Optional[str] = None) -> List[EventResponse]:
        if location:
            return self.event_repo.get_by_location(location)
        return self.event_repo.get_all()

    def get_event(self, event_id: int) -> EventResponse:
        event = self.event_repo.get_by_id(event_id)
        if not event:
            raise LookupError(f"Event with ID {event_id} not found.")
        return event
