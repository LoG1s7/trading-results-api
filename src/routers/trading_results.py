from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import Session
from src.filters.dynamics import DynamicsFilter
from src.filters.trading_results import TradingResultsFilter
from src.repository.trading_results import TradingResultsRepository

router = APIRouter(tags=["Trading Results"])


async def get_db() -> AsyncSession:
    async with Session() as session:
        yield session


@router.get("/last_trading_dates")
async def get_last_trading_dates(days: int, session: AsyncSession = Depends(get_db)):
    """Получение последних торговых дат."""
    return await TradingResultsRepository(session=session).get_last_trading_dates(
        days=days
    )


@router.get("/dynamics")
async def get_dynamics(
    data_filter: DynamicsFilter = Depends(DynamicsFilter),
    session: AsyncSession = Depends(get_db),
):
    """Получение динамики торгов за заданный период."""
    return await TradingResultsRepository(session=session).get_dynamics(
        data_filter=data_filter
    )


@router.get("/trading_results")
async def get_trading_results(
    data_filter: TradingResultsFilter = Depends(TradingResultsFilter),
    session: AsyncSession = Depends(get_db),
):
    """Получение результатов последних торгов."""
    return await TradingResultsRepository(session=session).get_trading_results(
        data_filter=data_filter
    )
