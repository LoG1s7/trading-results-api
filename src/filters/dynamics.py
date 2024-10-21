from datetime import date

from src.filters.trading_results import TradingResultsFilter


class DynamicsFilter(TradingResultsFilter):
    start_date: date | None = None
    end_date: date | None = None
