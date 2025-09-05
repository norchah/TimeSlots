from datetime import date, time, datetime

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base


class BookingDB(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    provider_id: Mapped[str] = mapped_column(nullable=False)
    client_id: Mapped[str] = mapped_column(nullable=False)
    service_id: Mapped[str] = mapped_column(nullable=False, index=True)
    booking_date: Mapped[date] = mapped_column(Date, index=True)
    start_time: Mapped[time] = mapped_column(index=True)
    end_time: Mapped[time] = mapped_column(index=True)
    status: Mapped[str] = mapped_column(index=True, default='confirmed')
    created_at: Mapped[datetime] = mapped_column(index=True, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"<Booking("
            f"id={self.id!r},"
            f" provider_id={self.provider_id!r},"
            f" client_id={self.client_id!r},"
            f" service_id={self.service_id!r},"
            f" date_booking={self.booking_date!r},"
            f" start_time={self.start_time!r},"
            f" end_time={self.end_time!r},"
            f" status={self.status!r},"
            f" created_at={self.created_at!r})>"
        )
