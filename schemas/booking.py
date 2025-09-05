from datetime import datetime, date, time

from pydantic import BaseModel


class BookingCreate(BaseModel):
    provider_id: str
    client_id: str
    service_id: str
    booking_date: date
    start_time: time
    end_time: time
    status: str | None = None


class BookingResponse(BaseModel):
    id: int | None = None
    provider_id: str | None = None
    client_id: str | None = None
    service_id: str | None = None
    booking_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    status: str | None = None
    created_at: datetime | None = None


class BookingUpdate(BookingResponse):
    pass
