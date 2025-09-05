from fastapi import HTTPException

from models.bookings import BookingDB


def create_booking(db, booking):
    timeslot = db.query(BookingDB).filter(BookingDB.id == booking.timeslot_id).first()
    if not timeslot:
        raise HTTPException(status_code=400, detail="Timeslot not found")
    if timeslot.is_booked:
        raise HTTPException(status_code=400, detail="Timeslot is already booked")
    if not has_role(db, booking.client_id, "client"):
        raise HTTPException(status_code=400, detail="Client not authorized")

    timeslot.is_booked = True
    new_booking = BookingDB(
        client_id=booking.client_id,
        timeslot_id=booking.timeslot_id,
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking
