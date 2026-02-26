from fastapi import APIRouter, Depends, HTTPException
from app.schemas.participant_schema import ParticipantCreate, ParticipantResponse
from app.services.participant_service import ParticipantService
from app.dependencies.service_dependency import get_participant_service

router = APIRouter()


@router.post("/", response_model=ParticipantResponse, status_code=201)
def register_participant(
    participant_data: ParticipantCreate,
    service: ParticipantService = Depends(get_participant_service)
):
    """Register a participant for an event."""
    try:
        return service.register_participant(participant_data)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{participant_id}", response_model=ParticipantResponse)
def get_participant(
    participant_id: int,
    service: ParticipantService = Depends(get_participant_service)
):
    """Fetch a participant by their ID."""
    try:
        return service.get_participant(participant_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
