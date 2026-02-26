from app.repositories.participant_repository import ParticipantRepository
from app.repositories.event_repository import EventRepository
from app.schemas.participant_schema import ParticipantCreate, ParticipantResponse


class ParticipantService:

    def __init__(self, participant_repo: ParticipantRepository, event_repo: EventRepository):
        self.participant_repo = participant_repo
        self.event_repo = event_repo

    def register_participant(self, participant_data: ParticipantCreate) -> ParticipantResponse:
        # Business rule: Event must exist
        event = self.event_repo.get_raw(participant_data.event_id)
        if not event:
            raise LookupError(f"Event with ID {participant_data.event_id} does not exist.")

        # Business rule: Event must not exceed capacity
        if event["registered_count"] >= event["capacity"]:
            raise ValueError(
                f"Event '{event['name']}' has reached its maximum capacity of {event['capacity']}."
            )

        # Business rule: Email must be unique
        existing = self.participant_repo.find_by_email(participant_data.email)
        if existing:
            raise ValueError(f"A participant with email '{participant_data.email}' is already registered.")

        # Save participant and increment event's registered count
        result = self.participant_repo.save(participant_data)
        self.event_repo.increment_registered_count(participant_data.event_id)
        return result

    def get_participant(self, participant_id: int) -> ParticipantResponse:
        participant = self.participant_repo.get_by_id(participant_id)
        if not participant:
            raise LookupError(f"Participant with ID {participant_id} not found.")
        return participant
