"""Данные, используемые в тестах."""

__all__ = [
    "PARAMS_TEST_GET_DYNAMICS_ENDPOINT",
    "PARAMS_TEST_GET_LAST_TRADING_DATES_ENDPOINT",
    "PARAMS_TEST_GET_TRADING_RESULTS_ENDPOINT",
    "TRADING_RESULTS",
]

from tests.fixtures.postgres.trading_results import TRADING_RESULTS
from tests.fixtures.test_cases import (
    PARAMS_TEST_GET_DYNAMICS_ENDPOINT,
    PARAMS_TEST_GET_LAST_TRADING_DATES_ENDPOINT,
    PARAMS_TEST_GET_TRADING_RESULTS_ENDPOINT,
)
