from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.data_access.trading_results import TradingResultsDataAccess
from src.database.db import Session
from src.filters.dynamics import DynamicsFilter
from src.filters.trading_results import TradingResultsFilter

router = APIRouter(tags=["Trading Results"])


async def get_db() -> AsyncSession:
    async with Session() as session:
        yield session


@router.get("/last_trading_dates")
async def get_last_trading_dates(days: int, db: AsyncSession = Depends(get_db)):
    """Получение последних торговых дат."""
    return await TradingResultsDataAccess.get_last_trading_dates(db, days)


@router.get("/dynamics")
async def get_dynamics(
    data_filter: DynamicsFilter = Depends(DynamicsFilter), db: AsyncSession = Depends(get_db)
):
    """Получение динамики торгов за заданный период."""
    return await TradingResultsDataAccess.get_dynamics(db, data_filter)


@router.get("/trading_results")
async def get_trading_results(
    data_filter: TradingResultsFilter = Depends(TradingResultsFilter),
    db: AsyncSession = Depends(get_db),
):
    """Получение результатов последних торгов."""
    return await TradingResultsDataAccess.get_trading_results(db, data_filter)
