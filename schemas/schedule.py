from datetime import date, time

from pydantic import BaseModel


class ScheduleTimeRequest(BaseModel):
    weekday: int
    schedule_start_time: time | None = None
    schedule_end_time: time | None = None


class ScheduleTimeResponse(ScheduleTimeRequest):
    is_available: bool


class ShiftTime(BaseModel):
    pattern: str
    months_ahead: int | None = None
    start_time: time | None = None
    end_time: time | None = None


class OverrideTime(BaseModel):
    date: date
    is_available: bool
    start_time: time | None = None
    end_time: time | None = None
    reason: str | None = None


class ScheduleRequest(BaseModel):
    provider_id: str
    request_date: date | None = None
    days: int | None = None
