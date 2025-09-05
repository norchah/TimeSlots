from sqlalchemy import Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base


class ProviderServiceDB(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    provider_id: Mapped[str] = mapped_column(nullable=False, index=True)

    name: Mapped[str] = mapped_column(nullable=False, index=True)  # "Консультация"
    description: Mapped[str] = mapped_column(nullable=True)
    duration_minutes: Mapped[int] = mapped_column(nullable=False)  # длительность услуги
    is_group: Mapped[bool] = mapped_column(Boolean, default=False, index=False)
    capacity: Mapped[int] = mapped_column(default=1)  # кол-во участников
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)

    def __repr__(self):
        return (
            f"<Service(id={self.id!r}, provider_id={self.provider_id!r}, "
            f"name={self.name!r}, duration={self.duration_minutes!r}, "
            f"is_group={self.is_group!r}, capacity={self.capacity!r}, price={self.price!r})>"
        )
