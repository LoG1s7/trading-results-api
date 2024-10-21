import logging

from redis.asyncio import Redis

from src.settings.config import REDIS_URL
from utils.exceptions import CacheError

logger = logging.getLogger(__name__)


async def clear_cache():
    """Полная очистка кэша Redis."""
    redis = Redis.from_url(REDIS_URL)
    try:
        await redis.flushall()
        logger.info("Кэш успешно очищен.")
    except CacheError:
        logger.exception("Ошибка при очистке кэша:")
