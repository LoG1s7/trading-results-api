from fastapi_filter.contrib.sqlalchemy import Filter

from src.models.trading_results import SpimexTradingResults


class TradingResultsFilter(Filter):
    oil_id: str | None
    delivery_type_id: str | None
    delivery_basis_id: str | None

    class Constants(Filter.Constants):
        model = SpimexTradingResults
