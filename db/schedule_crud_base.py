from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date, time

from models.schedule import ScheduleDB, ScheduleOverrideDB, ShiftDB


def get_provider_schedules_from_db(db: Session, provider_id: str) -> list[ScheduleDB]:
    """
    Извлекает все записи расписания по провайдеру.
    """
    return db.query(ScheduleDB).filter(ScheduleDB.provider_id == provider_id).all()


def get_provider_schedule_by_weekday_from_db(db: Session, provider_id: str, weekday: int):
    """
    Извлекает запись расписания по провайдеру и дню недели.
    """
    return db.query(ScheduleDB).filter(
        ScheduleDB.provider_id == provider_id,
        ScheduleDB.weekday == weekday
    ).first()


def get_provider_schedule_on_date_on_time(
        db: Session,
        provider_id: str,
        current_date: date,
        start_time: time,
        end_time: time
):
    """
    Извлекает исключение на дату и время
    """
    return db.query(ScheduleOverrideDB).filter(
            ScheduleOverrideDB.provider_id == provider_id,
            ScheduleOverrideDB.date == current_date,
            ScheduleOverrideDB.start_time == start_time,
            ScheduleOverrideDB.end_time == end_time
        ).first()



def get_provider_overrides_from_db(db: Session, provider_id: str):
    """
    Извлекает исключения из расписания провайдера
    """
    return db.query(ScheduleOverrideDB).filter_by(provider_id=provider_id).all()


def get_provider_override_by_date_from_db(db: Session, provider_id: str, override_date: date):
    """
    Извлекает запись о переопределении расписания (override) для конкретного провайдера на указанную дату.
    """
    return db.query(ScheduleOverrideDB).filter_by(provider_id=provider_id, date=override_date).all()
