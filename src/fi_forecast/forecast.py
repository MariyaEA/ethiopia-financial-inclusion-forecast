"""Bounded and explainable forecast utilities for sparse percentage data."""

from collections.abc import Sequence

import numpy as np
import pandas as pd

from fi_forecast.config import DEFAULT_SCENARIOS, ForecastConfig, Scenario
from fi_forecast.constants import NUMERIC_EPSILON


def _to_logit(percent_values: np.ndarray) -> np.ndarray:
    proportions = np.clip(percent_values / 100.0, NUMERIC_EPSILON, 1.0 - NUMERIC_EPSILON)
    return np.log(proportions / (1.0 - proportions))


def _from_logit(log_odds: np.ndarray) -> np.ndarray:
    return (1.0 / (1.0 + np.exp(-log_odds))) * 100.0


def _validate_history(years: Sequence[int], values_percent: Sequence[float]) -> None:
    if len(years) != len(values_percent):
        raise ValueError("years and values_percent must have the same length")
    if len(years) < 3:
        raise ValueError("at least three historical observations are required")
    if len(set(years)) != len(years):
        raise ValueError("historical years must be unique")
    if any(value < 0 or value > 100 for value in values_percent):
        raise ValueError("historical percentages must be between 0 and 100")


def forecast_bounded_rate(
    years: Sequence[int],
    values_percent: Sequence[float],
    config: ForecastConfig | None = None,
) -> pd.DataFrame:
    """Fit a logit-linear trend and forecast bounded percentage outcomes.

    The interval is an explainable residual-based uncertainty band in logit space.
    It is a planning range, not a claim of fully calibrated statistical coverage.
    """
    active_config = config or ForecastConfig()
    _validate_history(years, values_percent)

    year_array = np.asarray(years, dtype=float)
    value_array = np.asarray(values_percent, dtype=float)
    centered_years = year_array - year_array.mean()
    logit_values = _to_logit(value_array)

    slope, intercept = np.polyfit(centered_years, logit_values, deg=1)
    fitted = intercept + slope * centered_years
    residuals = logit_values - fitted
    residual_std = float(np.std(residuals, ddof=1)) if len(years) > 2 else 0.0

    forecast_years = np.asarray(active_config.forecast_years, dtype=float)
    forecast_centered = forecast_years - year_array.mean()
    forecast_logit = intercept + slope * forecast_centered

    margin = active_config.interval_z_score * residual_std
    point = _from_logit(forecast_logit)
    lower = _from_logit(forecast_logit - margin)
    upper = _from_logit(forecast_logit + margin)

    result = pd.DataFrame(
        {
            "year": forecast_years.astype(int),
            "forecast_percent": point,
            "lower_percent": lower,
            "upper_percent": upper,
        }
    )
    numeric_columns = ["forecast_percent", "lower_percent", "upper_percent"]
    result[numeric_columns] = result[numeric_columns].clip(
        lower=active_config.lower_bound_percent,
        upper=active_config.upper_bound_percent,
    )
    return result


def apply_scenario(
    baseline: pd.DataFrame,
    scenario: Scenario,
    anchor_year: int,
) -> pd.DataFrame:
    """Apply a transparent cumulative percentage-point scenario adjustment."""
    required = {"year", "forecast_percent", "lower_percent", "upper_percent"}
    missing = required - set(baseline.columns)
    if missing:
        raise ValueError(f"baseline missing columns: {', '.join(sorted(missing))}")

    scenario_frame = baseline.copy()
    elapsed_years = scenario_frame["year"] - anchor_year
    adjustment = elapsed_years * scenario.annual_adjustment_pp
    for column in ("forecast_percent", "lower_percent", "upper_percent"):
        scenario_frame[column] = (scenario_frame[column] + adjustment).clip(0.0, 100.0)
    scenario_frame["scenario"] = scenario.name
    scenario_frame["scenario_assumption"] = scenario.description
    scenario_frame["annual_adjustment_pp"] = scenario.annual_adjustment_pp
    return scenario_frame


def build_scenario_forecasts(
    years: Sequence[int],
    values_percent: Sequence[float],
    scenarios: Sequence[Scenario] = DEFAULT_SCENARIOS,
    config: ForecastConfig | None = None,
) -> pd.DataFrame:
    """Build one bounded forecast table for multiple explicit scenarios."""
    baseline = forecast_bounded_rate(years, values_percent, config=config)
    anchor_year = max(years)
    frames = [apply_scenario(baseline, scenario, anchor_year) for scenario in scenarios]
    return (
        pd.concat(frames, ignore_index=True)
        .sort_values(["year", "scenario"])
        .reset_index(drop=True)
    )
