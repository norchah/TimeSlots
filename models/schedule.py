from datetime import date, time

from sqlalchemy import Time, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base


class ScheduleDB(Base):
    __tablename__ = 'user_schedule'

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[str] = mapped_column(nullable=False, index=True)
    weekday: Mapped[int] = mapped_column(nullable=False, index=True)
    is_available: Mapped[bool] = mapped_column(nullable=False, index=True)
    schedule_start_time: Mapped[time | None] = mapped_column(Time, nullable=True, index=True)
    schedule_end_time: Mapped[time | None] = mapped_column(Time, nullable=True, index=True)
    __table_args__ = (
        UniqueConstraint("provider_id", "weekday", name="uq_provider_weekday"),
    )

    def __repr__(self):
        return (
            f"<UserSchedule(id={self.id!r},"
            f" provider_id={self.provider_id!r},"
            f" weekday={self.weekday!r},"
            f" is_available={self.is_available!r},"
            f" start_time={self.schedule_start_time!r},"
            f" end_time={self.schedule_end_time!r})>)"
        )


class ShiftPatternsDB(Base):
    __tablename__ = 'user_shift_pattern'

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[str] = mapped_column(nullable=False, index=True)
    pattern: Mapped[str] = mapped_column(index=True)

    def __repr__(self):
        return (
            f"<UserShiftPatterns("
            f" id={self.id!r},"
            f" provider_id={self.provider_id!r},"
            f" pattern={self.pattern!r})>"
        )


class ShiftDB(Base):
    __tablename__ = 'user_shifts'

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[str] = mapped_column(nullable=False, index=True)
    start_time: Mapped[date] = mapped_column(index=True)
    end_time: Mapped[date] = mapped_column(index=True)

    def __repr__(self):
        return (
            f"<UserShift("
            f"id={self.id!r},"
            f" provider_id={self.provider_id!r},"
            f" start_time={self.start_time!r},"
            f" end_time={self.end_time!r})>"
        )


class ScheduleOverrideDB(Base):
    __tablename__ = 'user_schedule_override'

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[str] = mapped_column(nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    is_available: Mapped[bool] = mapped_column(index=True)
    start_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    end_time: Mapped[time | None] = mapped_column(Time, nullable=True, index=True)
    reason: Mapped[str | None] = mapped_column(nullable=True)
