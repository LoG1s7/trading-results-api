"""Интеграционные тесты для эндпоинтов Trading Results."""

import pytest

from tests.fixtures import (
    PARAMS_TEST_GET_DYNAMICS_ENDPOINT,
    PARAMS_TEST_GET_LAST_TRADING_DATES_ENDPOINT,
    PARAMS_TEST_GET_TRADING_RESULTS_ENDPOINT,
)


class TestTradingResultsEndpoints:
    @pytest.mark.asyncio
    @pytest.mark.usefixtures("setup_trading_results")
    @pytest.mark.parametrize(
        ("url", "expected_status_code", "expected_response", "expectation"),
        PARAMS_TEST_GET_LAST_TRADING_DATES_ENDPOINT,
    )
    async def test_get_last_trading_dates(
        self, url: str, expected_status_code: int, expected_response, expectation, client
    ):
        with expectation:
            response = await client.get(url)
            assert response.status_code == expected_status_code
            assert response.json() == expected_response

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("setup_trading_results")
    @pytest.mark.parametrize(
        ("url", "expected_status_code", "expected_response", "expectation"),
        PARAMS_TEST_GET_TRADING_RESULTS_ENDPOINT,
    )
    async def test_get_trading_results(
        self, url: str, expected_status_code: int, expected_response, expectation, client
    ):
        with expectation:
            response = await client.get(url)
            assert response.status_code == expected_status_code
            response_data = response.json()
            assert len(response_data) == len(expected_response)
            for res, exp in zip(response_data, expected_response, strict=False):
                assert res["exchange_product_id"] == exp["exchange_product_id"]

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("setup_trading_results")
    @pytest.mark.parametrize(
        ("url", "expected_status_code", "expected_response", "expectation"),
        PARAMS_TEST_GET_DYNAMICS_ENDPOINT,
    )
    async def test_get_dynamics(
        self, url: str, expected_status_code: int, expected_response, expectation, client
    ):
        with expectation:
            response = await client.get(url)
            assert response.status_code == expected_status_code
            response_data = response.json()
            assert len(response_data) == len(expected_response)
            for res, exp in zip(response_data, expected_response, strict=False):
                assert res["exchange_product_id"] == exp["exchange_product_id"]
