import logging
from datetime import date

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import schemas.schedule as schemas
from crud.schedule import (
    crud_get_all_schedules,
    crud_get_all_override,
    crud_update_schedule,
    crud_update_override,
    crud_create_schedule_for_provider,
    crud_get_schedule
)
from db.db import get_db

schedule_router = APIRouter(prefix="/schedule", tags=["Расписание"])

logger = logging.getLogger(__name__)


@schedule_router.get("/get_all_schedule", status_code=status.HTTP_200_OK)
def get_all_schedule(db: Session = Depends(get_db)):
    """
    Возвращает все расписания всех провайдеров TODO после разработки можно удалить
    """
    return crud_get_all_schedules(db)


@schedule_router.get("/get_all_override", status_code=status.HTTP_200_OK)
def get_all_override(db: Session = Depends(get_db)):
    """
    Возвращает все исключения расписаний всех провайдеров TODO после разработки можно удалить
    """
    return crud_get_all_override(db)


@schedule_router.get("/provider_schedule/{provider_id}", status_code=status.HTTP_200_OK)
def get_schedule_for_provider(
        provider_id: str,
        request_date: date | None = None,
        days: int | None = None,
        db: Session = Depends(get_db)):
    """
    Возвращает актуальное расписание провайдера с исключениями и бронированиями
    начиная с даты request_data на протяжении days дней
    """
    schedule = crud_get_schedule(db, provider_id, request_date, days)
    return schedule


@schedule_router.post("/create_schedule/{provider_id}", status_code=status.HTTP_200_OK)
def create_schedule_for_provider(
        provider_id: str,
        schedule_data: list[schemas.ScheduleTimeRequest] | None = None,
        db: Session = Depends(get_db)
):
    """
    Создает паттерн расписания провайдера.
    """
    crud_create_schedule_for_provider(db, provider_id, schedule_data)
    return {"detail": "Schedule updated successfully"}


@schedule_router.put("/update_schedule/{provider_id}", status_code=status.HTTP_200_OK)
def update_schedule_for_provider(
        provider_id: str,
        schedule_data: list[schemas.ScheduleTimeRequest],
        db: Session = Depends(get_db)
):
    """
    Обновляет паттерн расписания провайдера.
    """
    crud_update_schedule(db, provider_id, schedule_data)
    return {"detail": "Schedule updated successfully"}


@schedule_router.put("/update_override/{provider_id}", status_code=status.HTTP_200_OK)
def update_override_for_provider(
        provider_id: str,
        override_data: list[schemas.OverrideTime],
        db: Session = Depends(get_db)
):
    """
    Обновляет исключения из паттерна расписания провайдера.
    """
    crud_update_override(db, provider_id, override_data)
    return {"detail": "Overrides updated successfully"}
