from datetime import datetime, timedelta

from sqlalchemy import String
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from ..models.times import TimeSlotDB


def check_timeslot_overlap(
        db: Session,
        provider_id: int,
        start_time: datetime,
        duration: int,
        exclude_timeslot_id: int | None = None
) -> bool:
    """
    Проверяет, пересекается ли новый временной слот с существующими слотами провайдера.

    Args:
        db: Сессия SQLAlchemy.
        provider_id: ID провайдера.
        start_time: Начало нового слота.
        duration: Длительность нового слота в минутах.
        exclude_timeslot_id: ID слота, который нужно исключить из проверки (для обновления).

    Returns:
        bool: True, если есть пересечение, False, если слот свободен.
    """
    end_time = start_time + timedelta(minutes=duration)

    query = db.query(TimeSlotDB).filter(
        TimeSlotDB.provider_id == provider_id,
        TimeSlotDB.start_time < end_time,
        func.datetime(TimeSlotDB.start_time, '+' + func.cast(TimeSlotDB.duration, String) + ' minutes') > start_time
    )

    if exclude_timeslot_id is not None:
        query = query.filter(TimeSlotDB.id != exclude_timeslot_id)

    return query.first() is not None
