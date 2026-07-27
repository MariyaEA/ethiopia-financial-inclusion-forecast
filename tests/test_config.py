import pytest

from fi_forecast.config import ForecastConfig


def test_forecast_config_accepts_sorted_years() -> None:
    config = ForecastConfig(forecast_years=(2025, 2026, 2027))
    assert config.forecast_years[-1] == 2027


def test_forecast_config_rejects_unsorted_years() -> None:
    with pytest.raises(ValueError, match="sorted"):
        ForecastConfig(forecast_years=(2026, 2025))


def test_forecast_config_rejects_invalid_bounds() -> None:
    with pytest.raises(ValueError, match="lower bound"):
        ForecastConfig(lower_bound_percent=100, upper_bound_percent=0)
