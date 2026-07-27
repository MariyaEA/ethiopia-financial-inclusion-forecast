"""Business metrics for financial inclusion analysis."""

from math import isfinite

import pandas as pd

from fi_forecast.constants import MAX_PERCENT, MIN_PERCENT


def percentage_point_change(start_percent: float, end_percent: float) -> float:
    """Calculate the percentage-point difference between two rates."""
    _validate_percent(start_percent)
    _validate_percent(end_percent)
    return float(end_percent - start_percent)


def annualized_change_pp(
    start_percent: float,
    end_percent: float,
    start_year: int,
    end_year: int,
) -> float:
    """Calculate average percentage-point change per year."""
    years = end_year - start_year
    if years <= 0:
        raise ValueError("end_year must be greater than start_year")
    return percentage_point_change(start_percent, end_percent) / years


def progress_to_target(current_percent: float, target_percent: float) -> float:
    """Return progress toward a positive target as a percentage of the target."""
    _validate_percent(current_percent)
    _validate_percent(target_percent)
    if target_percent == 0:
        raise ValueError("target_percent must be greater than zero")
    return min((current_percent / target_percent) * 100.0, 100.0)


def gap_to_target(current_percent: float, target_percent: float) -> float:
    """Return the remaining percentage-point gap to a target."""
    _validate_percent(current_percent)
    _validate_percent(target_percent)
    return max(target_percent - current_percent, 0.0)


def activation_rate(active_accounts: float, registered_accounts: float) -> float:
    """Calculate active accounts as a percentage of registered accounts."""
    if registered_accounts <= 0:
        raise ValueError("registered_accounts must be greater than zero")
    if active_accounts < 0:
        raise ValueError("active_accounts cannot be negative")
    if active_accounts > registered_accounts:
        raise ValueError("active_accounts cannot exceed registered_accounts")
    return (active_accounts / registered_accounts) * 100.0


def latest_value(series: pd.DataFrame) -> tuple[int, float]:
    """Return the latest year and value from a cleaned observation series."""
    if series.empty:
        raise ValueError("series cannot be empty")
    required = {"year", "value_numeric"}
    if not required.issubset(series.columns):
        raise ValueError("series must contain year and value_numeric columns")
    latest = series.sort_values("year").iloc[-1]
    return int(latest["year"]), float(latest["value_numeric"])


def _validate_percent(value: float) -> None:
    if not isfinite(value):
        raise ValueError("percentage must be finite")
    if value < MIN_PERCENT or value > MAX_PERCENT:
        raise ValueError("percentage must be between 0 and 100")
