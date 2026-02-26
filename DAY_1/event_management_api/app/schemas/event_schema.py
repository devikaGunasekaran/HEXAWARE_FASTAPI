from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    name: str = Field(..., min_length=3, description="Name of the event")
    location: str = Field(..., min_length=2, description="Location of the event")
    capacity: int = Field(..., gt=0, description="Maximum number of participants allowed")


class EventResponse(BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    registered_count: int = 0
