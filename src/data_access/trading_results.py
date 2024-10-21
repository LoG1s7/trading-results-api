from fastapi_cache.decorator import cache
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.filters.dynamics import DynamicsFilter
from src.filters.trading_results import TradingResultsFilter
from src.models.trading_results import SpimexTradingResults


class TradingResultsDataAccess:
    @staticmethod
    @cache(expire=3600)
    async def get_last_trading_dates(db: AsyncSession, days: int):
        """Возвращает список дат последних торговых дней,
        ограниченных указанным количеством дней.
        """
        stmt = (
            select(SpimexTradingResults.date)
            .distinct()
            .order_by(SpimexTradingResults.date.desc())
            .limit(days)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    @cache(expire=3600)
    async def get_dynamics(
        db: AsyncSession, data_filter: DynamicsFilter = FilterDepends(DynamicsFilter)
    ):
        """Возвращает динамику торгов за заданный период с учетом фильтров."""
        stmt = select(SpimexTradingResults)
        stmt = data_filter.filter(stmt)

        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    @cache(expire=3600)
    async def get_trading_results(
        db: AsyncSession,
        data_filter: TradingResultsFilter = FilterDepends(TradingResultsFilter),
    ):
        """Возвращает результаты последних торгов с учетом фильтров."""
        stmt = select(SpimexTradingResults)
        stmt = data_filter.filter(stmt)

        result = await db.execute(stmt)
        return result.scalars().all()
