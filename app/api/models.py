import uuid

from datetime import datetime

from pydantic import BaseModel


class CurrencyRatePayload(BaseModel):
    pair: str
    price: float
    timestamp: datetime

    class Config:
        from_attributes=True


class CurrencyRate(CurrencyRatePayload):
    pk: uuid.UUID
