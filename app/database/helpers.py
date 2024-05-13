from . import models as db_models
from ..api import models

from .session import get_db_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from datetime import datetime


async def _add_pair_rate_to_db(
    session: AsyncSession, 
    pair: models.CurrencyRatePayload
) -> None:
    await session.execute(
        insert(db_models.CurrencyRates).values(
            pair=pair.pair,
            price=pair.price,
            timestamp=pair.timestamp
        )
    )


async def add_pairs_rate_to_db(pairs: list[models.CurrencyRatePayload]) -> None:
    async with get_db_session() as session:
        for pair in pairs:
            await _add_pair_rate_to_db(session, pair)
        await session.commit()


async def db_get_pair_last_rate(
    session: AsyncSession, 
    pair: str,
) -> models.CurrencyRatePayload | None:
    rates = await session.scalars(
        select(
            db_models.CurrencyRates,
        ).where(
            db_models.CurrencyRates.pair == pair
        ).order_by(
            db_models.CurrencyRates.timestamp.desc()
        )
    )
    rate = rates.first()
    if rate:
        return models.CurrencyRatePayload.model_validate(rate)


async def db_get_pair_rates(
    session: AsyncSession, 
    pairs: list[str],
    date_from: datetime | None = None,
    date_to: datetime | None = None
) -> list[models.CurrencyRatePayload] | None:
    sql = select(
            db_models.CurrencyRates,
        ).where(
            db_models.CurrencyRates.pair.in_(pairs),
            db_models.CurrencyRates.timestamp >= date_from if date_from else True,
            db_models.CurrencyRates.timestamp <= date_to if date_to else True
        ).order_by(
            db_models.CurrencyRates.timestamp if pairs else db_models.CurrencyRates.pair
        )
    rates = await session.scalars(sql)
    rates = rates.all()
    if rates:
        return [models.CurrencyRatePayload.model_validate(rate) for rate in rates]

