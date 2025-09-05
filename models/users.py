import uuid

from sqlalchemy import Column, String, ForeignKey, Table, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.db import Base

# Ассоциативная таблица для many-to-many
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', String(32), ForeignKey('users.id'), primary_key=True),
    Column("role_id", Integer, ForeignKey('roles.id'), primary_key=True)
)


class RoleDB(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(200), nullable=True)

    users: Mapped[list["UserDB"]] = relationship(
        secondary=user_roles,
        back_populates="roles",
        # cascade="all, delete",
        lazy="selectin"
    )

    def __repr__(self):
        description = self.description if self.description else 'Empty'
        return f"<Role(id={self.id!r}, name={self.name!r}, description={description!r})>"


class UserDB(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        String(32),
        primary_key=True,
        default=lambda: uuid.uuid4().hex,
        index=True
    )

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True, index=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True, index=True)

    roles: Mapped[list["RoleDB"]] = relationship(
        secondary=user_roles,
        back_populates='users',
        # cascade="all, delete",
        lazy='selectin'
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    def __repr__(self):
        return (
            f"<User("
            f"id={self.id!r}, "
            f"username={self.username!r}, "
            f"roles={self.roles!r}, "
            f"is_active={self.is_active!r})>"
        )
