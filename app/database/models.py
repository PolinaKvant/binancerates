import uuid

from datetime import datetime

from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    """Base database model."""

    pk: orm.Mapped[uuid.UUID] = orm.mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )


class CurrencyRates(Base):

    __tablename__ = "currency_rates"

    pair: orm.Mapped[str]
    price: orm.Mapped[float]
    timestamp: orm.Mapped[datetime]

