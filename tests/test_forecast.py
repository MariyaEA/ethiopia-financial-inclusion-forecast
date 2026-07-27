import pandas as pd
import pytest

from fi_forecast.config import DEFAULT_SCENARIOS, ForecastConfig, Scenario
from fi_forecast.forecast import apply_scenario, build_scenario_forecasts, forecast_bounded_rate

YEARS = [2011, 2014, 2017, 2021, 2024]
VALUES = [14, 22, 35, 46, 49]


def test_forecast_is_bounded_and_has_expected_years() -> None:
    result = forecast_bounded_rate(YEARS, VALUES)
    assert result["year"].tolist() == [2025, 2026, 2027]
    assert result[["forecast_percent", "lower_percent", "upper_percent"]].ge(0).all().all()
    assert result[["forecast_percent", "lower_percent", "upper_percent"]].le(100).all().all()


def test_forecast_rejects_too_few_points() -> None:
    with pytest.raises(ValueError, match="at least three"):
        forecast_bounded_rate([2021, 2024], [46, 49])


def test_apply_scenario_requires_expected_columns() -> None:
    with pytest.raises(ValueError, match="missing columns"):
        apply_scenario(pd.DataFrame({"year": [2025]}), DEFAULT_SCENARIOS[0], 2024)


def test_scenario_forecasts_are_ordered() -> None:
    result = build_scenario_forecasts(YEARS, VALUES)
    pivot = result.pivot(index="year", columns="scenario", values="forecast_percent")
    assert (pivot["Pessimistic"] < pivot["Base"]).all()
    assert (pivot["Base"] < pivot["Optimistic"]).all()


def test_custom_scenario_adjustment_is_cumulative() -> None:
    baseline = pd.DataFrame(
        {
            "year": [2025, 2026],
            "forecast_percent": [50.0, 51.0],
            "lower_percent": [45.0, 46.0],
            "upper_percent": [55.0, 56.0],
        }
    )
    scenario = Scenario("Custom", 1.0, "Test")
    result = apply_scenario(baseline, scenario, anchor_year=2024)
    assert result["forecast_percent"].tolist() == [51.0, 53.0]


def test_custom_forecast_years() -> None:
    config = ForecastConfig(forecast_years=(2025, 2028))
    result = forecast_bounded_rate(YEARS, VALUES, config=config)
    assert result["year"].tolist() == [2025, 2028]
