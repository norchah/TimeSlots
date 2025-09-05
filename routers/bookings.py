import logging

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from crud.schedule import crud_get_schedule
from db.db import get_db
from db.schedule_crud_base import get_provider_schedule_by_weekday_from_db
from models.bookings import BookingDB
from schemas.booking import BookingCreate, BookingResponse

logger = logging.getLogger(__name__)

booking_router = APIRouter(prefix="/booking", tags=["Бронирования"])


@booking_router.post("/create", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    current_schedule_provider_date = crud_get_schedule(
        db,
        provider_id=booking.provider_id,
        request_date=booking.booking_date,
        days=1
    )
    # Проверяем рабочий ли день у провайдера
    if not current_schedule_provider_date.get('is_available'):
        raise HTTPException(status_code=400, detail="it is a weekend day for provider")
    # Проверяем попадает ли бронирование в рабочие часы
    working_slots = current_schedule_provider_date.get('working_slots')
    if not (working_slots['schedule_start_time'] <= booking.start_time < working_slots['schedule_end_time']):
        raise HTTPException(status_code=400, detail="This time provider not working")
        # Ищем свободный слот
    selected_slot = None
    for slot in current_schedule_provider_date['slots']:
        logger.warning(f'!!!!! slot {slot}')
        if (slot['start_time'] <= booking.start_time < slot['end_time']) and not slot['is_booked']:
            selected_slot = slot
            break  # нашли подходящий слот, дальше не ищем
    logger.warning(f'!!!!!! selected_slot:::: {selected_slot}')
    if selected_slot:
        raise HTTPException(status_code=400, detail="slot is busy")

    # Сохраняем бронирование в базу
    new_booking = BookingDB(**booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


@booking_router.get("/all/", response_model=list[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(BookingDB).all()


@booking_router.get("/provider/{client_id}", response_model=list[BookingResponse])
def get_all_booking_client(client_id: str, db: Session = Depends(get_db)):
    return db.query(BookingDB).filter_by(client_id=client_id).all()


@booking_router.get("/provider_get")
def get_all_booking_client(weekend: int, db: Session = Depends(get_db)):
    exist_schedule_provider_time = get_provider_schedule_by_weekday_from_db(
        db,
        "f492ca92a78d4ddab44786c8316e21a2",
        weekend
    )
    return exist_schedule_provider_time


@booking_router.delete('/del/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(id: int, db: Session = Depends(get_db)):
    db.query(BookingDB).filter_by(id=id).delete()
    db.commit()
    return id
