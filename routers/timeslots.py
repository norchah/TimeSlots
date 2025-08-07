from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from db import get_db
from utils.check_timeslot_overlap import check_timeslot_overlap
from utils.has_role import has_role

time_slot_router = APIRouter(tags=["TimeSlot"])


@time_slot_router.post("/timeslot/", response_model=schemas.TimeSlotResponse)
def create_timeslot(timeslot: schemas.TimeSlotCreate, db: Session = Depends(get_db)):
    if not has_role(db, timeslot.provider_id, 'provider'):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if check_timeslot_overlap(
            db=db,
            provider_id=timeslot.provider_id,
            start_time=timeslot.start_time,
            duration=timeslot.duration,
    ):
        raise HTTPException(status_code=403, detail="Timeslot overlap")
    new_timeslot = models.TimeSlotDB(
        provider_id=timeslot.provider_id,
        start_time=timeslot.start_time,
        duration=timeslot.duration,
    )
    db.add(new_timeslot)
    db.commit()
    db.refresh(new_timeslot)
    return new_timeslot


@time_slot_router.get("/timeslot/", response_model=list[schemas.TimeSlotResponse])
def get_timeslots(db: Session = Depends(get_db)):
    return db.query(models.TimeSlotDB).all()


@time_slot_router.get("/timeslot/{provider_id}", response_model=list[schemas.TimeSlotResponse])
def get_timeslot_by_id(provider_id: int, db: Session = Depends(get_db)):
    return db.query(models.TimeSlotDB).filter_by(provider_id=provider_id).all()
