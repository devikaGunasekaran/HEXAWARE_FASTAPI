from pydantic import BaseModel, Field, EmailStr


class ParticipantCreate(BaseModel):
    name: str = Field(..., min_length=2, description="Name of the participant")
    email: EmailStr = Field(..., description="Email address of the participant")
    event_id: int = Field(..., gt=0, description="ID of the event to register for")


class ParticipantResponse(BaseModel):
    id: int
    name: str
    email: str
    event_id: int
