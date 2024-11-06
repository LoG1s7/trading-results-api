import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis

from src.routers import trading_results
from src.settings.config import REDIS_URL, settings
from src.utils.cache import clear_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """События жизненного цикла приложения."""
    logger.info("Настройка кэша и планировщика...")

    if settings.MODE != "TEST":
        redis = Redis.from_url(REDIS_URL)

        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

        scheduler.add_job(clear_cache, "cron", hour=14, minute=11)
        scheduler.start()
        logger.info("Планировщик запущен")

    yield

    if settings.MODE != "TEST":
        logger.info("Остановка планировщика.")
        scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(trading_results.router, prefix="/api")
