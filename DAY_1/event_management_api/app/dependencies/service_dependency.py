from app.repositories.event_repository import EventRepository
from app.repositories.participant_repository import ParticipantRepository
from app.services.event_service import EventService
from app.services.participant_service import ParticipantService

# Singleton repository instances (shared in-memory storage)
_event_repository = EventRepository()
_participant_repository = ParticipantRepository()


def get_event_service() -> EventService:
    return EventService(event_repo=_event_repository)


def get_participant_service() -> ParticipantService:
    return ParticipantService(
        participant_repo=_participant_repository,
        event_repo=_event_repository
    )
