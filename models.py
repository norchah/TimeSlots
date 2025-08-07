from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db import Base

# Ассоциативная таблица для many-to-many
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column("role_id", Integer, ForeignKey('roles.id'), primary_key=True)
)


class RoleDB(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    users: Mapped[list["UserDB"]] = relationship(
        secondary=user_roles,
        back_populates="roles",
        cascade="all, delete",
        lazy="selectin"
    )

    def __repr__(self):
        description = self.description if self.description else 'Empty'
        return f"<Role(id={self.id!r}, name={self.name!r}, description={description!r}, users={self.users!r})>"


class UserDB(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    roles: Mapped[list["RoleDB"]] = relationship(
        secondary=user_roles,
        back_populates='users',
        cascade="all, delete",
        lazy='selectin')
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    def __repr__(self):
        return (f"<User("
                f"id={self.id!r},"
                f"username={self.username!r},"
                f"roles={self.roles!r},"
                f"is_active={self.is_active!r})>"
                )


class TimeSlotDB(Base):
    __tablename__ = "timeslots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False)
    is_booked: Mapped[bool] = mapped_column(nullable=False, default=False)

    def __repr__(self):
        return (
            f"<TimeSlot("
            f"id={self.id!r}, "
            f"provider_id={self.provider_id!r},"
            f"start_time={self.start_time!r},"
            f"duration={self.duration!r},"
            f"is_booked={self.is_booked!r})>"
        )


class BookingDB(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    timeslot_id: Mapped[int] = mapped_column(ForeignKey("timeslots.id"), nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Booking(id={self.id!r}, timeslot_id={self.timeslot_id!r}, client_id={self.client_id!r})>"
