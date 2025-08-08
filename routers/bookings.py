from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from db.db import get_db
from utils.has_role import has_role

booking_router = APIRouter(tags=["Booking"])


@booking_router.post("/booking/", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    timeslot = db.query(models.TimeSlotDB).filter(models.TimeSlotDB.id == booking.timeslot_id).first()
    if not timeslot:
        raise HTTPException(status_code=400, detail="Timeslot not found")
    if timeslot.is_booked:
        raise HTTPException(status_code=400, detail="Timeslot is already booked")
    if not has_role(db, booking.client_id, "client"):
        raise HTTPException(status_code=400, detail="Client not authorized")

    timeslot.is_booked = True
    new_booking = models.BookingDB(
        client_id=booking.client_id,
        timeslot_id=booking.timeslot_id,
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@booking_router.get("/booking/", response_model=list[schemas.BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(models.BookingDB).all()


@booking_router.get("/booking/client/{client_id}", response_model=list[schemas.BookingResponse])
def get_all_booking_client(client_id: str, db: Session = Depends(get_db)):
    return db.query(models.BookingDB).filter_by(client_id=client_id).all()


@booking_router.get("/booking/provider/{provider_id}", response_model=list[schemas.BookingResponse])
def get_all_booking_provider(provider_id: str, db: Session = Depends(get_db)):
    return db.query(models.BookingDB).join(
        models.TimeSlotDB, models.BookingDB.timeslot_id == models.TimeSlotDB.id
    ).filter(models.TimeSlotDB.provider_id == provider_id).all()
