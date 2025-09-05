from datetime import datetime

from pydantic import BaseModel, Field


class TimeSlotCreate(BaseModel):
    provider_id: int
    start_time: datetime
    duration: int = Field(..., ge=1)  # Поле обязательно и его значение должно быть больше или равно 1


class TimeSlotResponse(BaseModel):
    id: int
    provider_id: int
    start_time: datetime
    duration: int
    is_booked: bool


class BookingCreate(BaseModel):
    timeslot_id: int
    client_id: int


class BookingResponse(BaseModel):
    id: int
    timeslot_id: int
    client_id: int


class LoginRequest(BaseModel):
    username: str


class TokenResponse(BaseModel):
    token_type: str
    roles: list[str]
