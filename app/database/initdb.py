import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from ..config import settings
from ..database.models import Base


async def init_db() -> None:
    engine = create_async_engine(settings.DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
