from contextlib import nullcontext as does_not_raise

from tests.fixtures.postgres.trading_results import TRADING_RESULTS

PARAMS_TEST_GET_LAST_TRADING_DATES_ENDPOINT = [
    (
        "/api/last_trading_dates?days=2",
        200,
        ["2023-01-02", "2023-01-01"],
        does_not_raise(),
    ),
    ("/api/last_trading_dates?days=1", 200, ["2023-01-02"], does_not_raise()),
]

PARAMS_TEST_GET_TRADING_RESULTS_ENDPOINT = [
    ("/api/trading_results?oil_id=A100", 200, [TRADING_RESULTS[0]], does_not_raise()),
    ("/api/trading_results?oil_id=A600", 200, [], does_not_raise()),
]

PARAMS_TEST_GET_DYNAMICS_ENDPOINT = [
    (
        "/api/dynamics?oil_id=A100&start_date=2023-01-01&end_date=2023-01-02",
        200,
        [TRADING_RESULTS[0]],
        does_not_raise(),
    ),
    (
        "/api/dynamics?oil_id=A592&start_date=2023-01-01&end_date=2023-01-02",
        200,
        [TRADING_RESULTS[1]],
        does_not_raise(),
    ),
    (
        "/api/dynamics?oil_id=A600&start_date=2023-01-01&end_date=2023-01-02",
        200,
        [],
        does_not_raise(),
    ),
]
