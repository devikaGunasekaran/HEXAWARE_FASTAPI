from typing import List, Optional
from app.schemas.event_schema import EventCreate, EventResponse


_events: List[dict] = []
_id_counter: int = 0


class EventRepository:

    def save(self, event_data: EventCreate) -> EventResponse:
        global _id_counter
        _id_counter += 1
        event = {
            "id": _id_counter,
            "name": event_data.name,
            "location": event_data.location,
            "capacity": event_data.capacity,
            "registered_count": 0
        }
        _events.append(event)
        return EventResponse(**event)

    def get_all(self) -> List[EventResponse]:
        return [EventResponse(**e) for e in _events]

    def get_by_id(self, event_id: int) -> Optional[EventResponse]:
        for event in _events:
            if event["id"] == event_id:
                return EventResponse(**event)
        return None

    def get_by_location(self, location: str) -> List[EventResponse]:
        return [
            EventResponse(**e)
            for e in _events
            if e["location"].lower() == location.lower()
        ]

    def find_by_name(self, name: str) -> Optional[dict]:
        for event in _events:
            if event["name"].lower() == name.lower():
                return event
        return None

    def increment_registered_count(self, event_id: int) -> None:
        for event in _events:
            if event["id"] == event_id:
                event["registered_count"] += 1
                break

    def get_raw(self, event_id: int) -> Optional[dict]:
        for event in _events:
            if event["id"] == event_id:
                return event
        return None
