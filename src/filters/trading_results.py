from dataclasses import dataclass

from fastapi import Query

from src.filters.base import BaseFilter


@dataclass
class TradingResultsFilter(BaseFilter):
    oil_id: str | None = Query(None)
    delivery_type_id: str | None = Query(None)
    delivery_basis_id: str | None = Query(None)
