import logging
from datetime import date, timedelta

from sqlalchemy.orm import Session

from db.booking_crud_base import get_bookings_for_provider_on_date_from_db
from db.schedule_crud_base import get_provider_override_by_date_from_db, get_provider_schedule_by_weekday_from_db

logger = logging.getLogger(__name__)


def get_schedule_for_date(db: Session, provider_id: str, target_date: date) -> dict:
    """
    Возвращает расписание на один день с учётом override и бронирований.
    """
    weekday = target_date.isoweekday()
    slots = []

    # 1. Берем стандартное расписание
    schedule = get_provider_schedule_by_weekday_from_db(db, provider_id, weekday)
    # Если нет стартового времени, значит выходной
    if not schedule.is_available:
        return {
            "date": target_date.isoformat(),
            "weekday": weekday,
            "is_available": False,
            "slots": [],
            "reason": "day off"
        }

    working_slot = {
        "schedule_start_time": schedule.schedule_start_time,
        "schedule_end_time": schedule.schedule_end_time,
        "is_booked": False
    }

    # 2. Проверяем override
    override = get_provider_override_by_date_from_db(db, provider_id, target_date)
    # Если весь день недоступен, то выходной и провайдер не принимает
    if len(override) > 0:
        if not override[0].is_available:
            return {
                "date": target_date.isoformat(),
                "weekday": weekday,
                "is_available": override.is_available,
                "slots": [],
                "reason": override.reason
            }
        # Если день доступен, то не принимает в определенные часы
        for item in override:
            slots.append(
                {
                    "start_time": item.start_time,
                    "end_time": item.end_time,
                    "is_booked": True,
                    "reason": item.reason
                }
            )
    # 3. Получаем бронирования на этот день
    bookings = get_bookings_for_provider_on_date_from_db(db, provider_id, target_date)
    logger.warning(f'!!!!!!! bookings: {bookings}')
    if len(bookings) > 0:
        for item in bookings:
            slots.append(
                {
                    "start_time": item.start_time,
                    "end_time": item.end_time,
                    "is_booked": True,
                }
            )
    return {
        "date": target_date.isoformat(),
        "weekday": weekday,
        "is_available": True,
        "slots": slots,
        "working_slots": working_slot
    }


def get_schedule_range(db: Session, provider_id: str, start_date: date, days: int):
    """
    Возвращает расписание провайдера на диапазон дней.
    """
    result = []
    for i in range(days):
        target_date = start_date + timedelta(days=i)
        day_schedule = get_schedule_for_date(db, provider_id, target_date)
        result.append(day_schedule)
    return result
