from typing import List, Optional
from app.schemas.participant_schema import ParticipantCreate, ParticipantResponse

# In-memory storage for participants
_participants: List[dict] = []
_id_counter: int = 0


class ParticipantRepository:

    def save(self, participant_data: ParticipantCreate) -> ParticipantResponse:
        global _id_counter
        _id_counter += 1
        participant = {
            "id": _id_counter,
            "name": participant_data.name,
            "email": participant_data.email,
            "event_id": participant_data.event_id
        }
        _participants.append(participant)
        return ParticipantResponse(**participant)

    def get_by_id(self, participant_id: int) -> Optional[ParticipantResponse]:
        for participant in _participants:
            if participant["id"] == participant_id:
                return ParticipantResponse(**participant)
        return None

    def find_by_email(self, email: str) -> Optional[dict]:
        for participant in _participants:
            if participant["email"].lower() == email.lower():
                return participant
        return None

    def get_all(self) -> List[ParticipantResponse]:
        return [ParticipantResponse(**p) for p in _participants]
