from fastapi import Query
from fastapi_cache.decorator import cache
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.filters.dynamics import DynamicsFilter
from src.filters.trading_results import TradingResultsFilter
from src.models.trading_results import SpimexTradingResults


class TradingResultsRepository:
    model = SpimexTradingResults

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @cache(expire=3600)
    async def get_last_trading_dates(self, days: int):
        """Возвращает список дат последних торговых дней,
        ограниченных указанным количеством дней.
        """
        stmt = (
            select(self.model.date)
            .distinct()
            .order_by(self.model.date.desc())
            .limit(days)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def _build_query(self, data_filter) -> Query:
        """Строит запрос на основе фильтров."""
        query = select(self.model)

        if data_filter.oil_id:
            query = query.where(self.model.oil_id == data_filter.oil_id)

        if data_filter.delivery_type_id:
            query = query.where(
                self.model.delivery_type_id == data_filter.delivery_type_id
            )

        if data_filter.delivery_basis_id:
            query = query.where(
                self.model.delivery_basis_id == data_filter.delivery_basis_id
            )

        query = query.offset(data_filter.offset).limit(data_filter.limit)

        return query

    @cache(expire=3600)
    async def get_dynamics(self, data_filter: DynamicsFilter):
        """Возвращает динамику торгов за заданный период с учетом фильтров."""
        data_filter.validate()
        query = await self._build_query(data_filter)

        query = query.where(self.model.date >= data_filter.start_date)
        query = query.where(self.model.date <= data_filter.end_date)

        res: Result = await self.session.execute(query)
        return res.scalars().all()

    @cache(expire=3600)
    async def get_trading_results(self, data_filter: TradingResultsFilter):
        """Возвращает результаты последних торгов с учетом фильтров."""
        query = await self._build_query(data_filter)
        query = query.order_by(self.model.date.desc())

        res: Result = await self.session.execute(query)
        return res.scalars().all()
