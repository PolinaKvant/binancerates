import json, asyncio, aioredis
import uvicorn, websockets

from contextlib import asynccontextmanager
from datetime import datetime

from typing import NoReturn

from fastapi import FastAPI

from .config import settings

from .api import models
from .api.v1.routes import router as v1_router

from .database.helpers import add_pairs_rate_to_db
from .database.initdb import init_db
from .redis_client import redis_client


async def hendler(
    websocket,
    redis: aioredis.Redis
) -> NoReturn:
    while True:
        pairs = json.loads(await websocket.recv())
        for index, pair in enumerate(pairs):

            pair = models.CurrencyRatePayload(
                pair=pair['s'],
                price=pair['c'],
                timestamp=datetime.fromtimestamp(pair['E'] / 1000)
            )
            pairs[index] = pair

            async with redis.client() as conn:
                await conn.set(pair.pair, pair.model_dump_json())

        asyncio.create_task(add_pairs_rate_to_db(pairs))


@asynccontextmanager
async def lifespan(
    app: FastAPI
):
    await init_db()
    url = 'wss://stream.binance.com:443/ws/!miniTicker@arr'
    async with websockets.connect(url) as websocket:
        asyncio.create_task(hendler(websocket, redis_client))
        yield


app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={"displayRequestDuration": True}
)
app.include_router(v1_router, prefix="/api")


if __name__ == '__main__':
    uvicorn.run(
        'app.app:app', 
        port=settings.API_PORT
    )
