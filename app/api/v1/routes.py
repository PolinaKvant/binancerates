import json

from datetime import datetime
from dataclasses import dataclass
from typing import Annotated

from fastapi import (
    APIRouter, 
    Depends, 
    Query,
    status, 
)

from app.api import models
from app.database.session import get_db_session
from app.database.helpers import db_get_pair_rates, db_get_pair_last_rate
from app.redis_client import redis_client

router = APIRouter(prefix="/v1", tags=["v1"])


@dataclass
class GetRatesAgrs:
    pairs: Annotated[
        list[str], 
        Query(
            title='Список валютных пар',
        )
    ]
    date_from: datetime | None = None
    date_to: datetime | None = None


@router.get("/rate/{pair}", status_code=status.HTTP_200_OK)
async def get_pair_last_rate(pair: str) -> models.CurrencyRatePayload | None:
    """ 
    Возвращает последний курс валютной пары. 

    `:param pair:` Пара валют.
    """
    async with redis_client.client() as conn:
        cached_pair = await conn.get(pair)
        if cached_pair :
            return models.CurrencyRatePayload.model_validate(json.loads(cached_pair))

    async with get_db_session() as session:
        return await db_get_pair_last_rate(session, pair.upper())


@router.get("/rates", status_code=status.HTTP_200_OK)
async def get_pairs_rates(
    args: GetRatesAgrs = Depends(),
) -> list[models.CurrencyRatePayload] | None:
    """ 
    Возвращает курсы валют.

    `:param pairs:` Список пар валют.  
    `:param date_from:` Дата начала периода.  
    `:param date_to:` Дата окончания периода.  

    `:return:` Курсы валют. Если не указаны временные рамки - возвращает курсы за всё время.
    """
    async with get_db_session() as session:
        rates = await db_get_pair_rates(
            session, 
            args.pairs,
            args.date_from, 
            args.date_to
        )
    return rates

