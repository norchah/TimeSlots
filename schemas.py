from datetime import datetime

from pydantic import BaseModel, Field


class RoleCreate(BaseModel):
    name: str = Field(..., min_length=3)
    description: str | None = None


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)


class UserResponse(BaseModel):
    id: int
    username: str
    roles: list[RoleResponse]


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
