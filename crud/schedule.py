import logging
from datetime import date

from sqlalchemy.orm import Session

from db.instance_base import save_instances_to_db
from db.schedule_crud_base import (
    get_provider_schedules_from_db,
    get_provider_schedule_by_weekday_from_db, get_provider_schedule_on_date_on_time
)
from db.user_crud_base import get_user_or_404, get_user_by_id_from_db
from models.schedule import ScheduleDB, ScheduleOverrideDB
from schemas.schedule import ScheduleTimeRequest, OverrideTime
from services.get_schedule import get_schedule_range, get_schedule_for_date
from services.init_schedule_for_provider import init_empty_schedule_for_provider

logger = logging.getLogger(__name__)


# ---------------------------
# Создание расписания
# ---------------------------
def crud_create_schedule_for_provider(
        db: Session, user_id: str,
        schedule_data: list[ScheduleTimeRequest] | None = None
):
    """
    Создает стандартный паттерн расписания на неделю провайдера
    """
    if not get_provider_schedules_from_db(db, user_id):
        init_empty_schedule_for_provider(db, user_id)
    return crud_update_schedule(db, provider_id=user_id, schedule_data=schedule_data)


# ---------------------------
# Обновление расписания
# ---------------------------
def crud_update_schedule(db: Session, provider_id: str, schedule_data: list[ScheduleTimeRequest]):
    """
    Обновляет паттерн расписания провайдера.
    """
    get_user_or_404(get_user_by_id_from_db(db, provider_id))
    updated_schedules = []
    for item in schedule_data:
        schedule = get_provider_schedule_by_weekday_from_db(db, provider_id, item.weekday)
        schedule.is_available = True
        schedule.schedule_start_time = item.schedule_start_time
        schedule.schedule_end_time = item.schedule_end_time
        updated_schedules.append(schedule)
    # Сохраняем все изменения разом
    new_schedule = save_instances_to_db(db, updated_schedules)
    return new_schedule


def crud_update_override(db: Session, provider_id: str, override_data: list[OverrideTime]):
    """
    Создает/обновляет исключения паттерна расписания провайдера
    """
    get_user_or_404(get_user_by_id_from_db(db, provider_id))
    for item in override_data:
        # Получаем исключение на конкретную дату и время
        existing_override = get_provider_schedule_on_date_on_time(
            db,
            provider_id,
            item.date,
            item.start_time,
            item.end_time
        )
        if len(existing_override) > 0:
            # Обновляем существующую
            existing_override.is_available = item.is_available
            existing_override.reason = item.reason
        else:
            # Создаем новый override
            new_override = ScheduleOverrideDB(
                provider_id=provider_id,
                date=item.date,
                is_available=item.is_available,
                start_time=item.start_time,
                end_time=item.end_time,
                reason=item.reason
            )
            db.add(new_override)
    db.commit()


def crud_get_all_schedules(db: Session):
    """
    Возвращает все расписания всех провайдеров TODO Для dev потом можно удалить
    """
    return db.query(ScheduleDB).all()


def crud_get_all_override(db: Session):
    """
    Возвращает все исключения всех провайдеров TODO Для dev потом можно удалить
    """
    return db.query(ScheduleOverrideDB).all()


def crud_get_schedule(db: Session, provider_id: str, request_date: date, days: int):
    """
    Возвращает актуальное расписание провайдера с исключениями и бронированиями
    """
    if not request_date:
        request_date = date.today()
    if not days:
        return get_schedule_range(db, provider_id, start_date=request_date, days=30)
    if days > 1:
        return get_schedule_range(db, provider_id, start_date=request_date, days=days)
    schedule = get_schedule_for_date(db, provider_id, target_date=request_date)
    return schedule
