from dataclasses import dataclass
from datetime import date

from fastapi import HTTPException, Query

from src.filters.trading_results import TradingResultsFilter


@dataclass
class DynamicsFilter(TradingResultsFilter):
    start_date: date = Query(..., description="Start date for filtering.")
    end_date: date = Query(..., description="End date for filtering.")

    def validate(self):
        if self.start_date > self.end_date:
            raise HTTPException(
                status_code=400,
                detail="`start_date` must be less than or equal to `end_date`.",
            )
