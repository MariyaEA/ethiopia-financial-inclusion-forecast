"""Typed configuration objects for forecasting and scenario analysis."""

from dataclasses import dataclass

from fi_forecast.constants import DEFAULT_FORECAST_YEARS, MAX_PERCENT, MIN_PERCENT


@dataclass(frozen=True, slots=True)
class Scenario:
    """An explicit scenario adjustment in percentage points."""

    name: str
    annual_adjustment_pp: float
    description: str


@dataclass(frozen=True, slots=True)
class ForecastConfig:
    """Configuration for bounded forecasts."""

    forecast_years: tuple[int, ...] = DEFAULT_FORECAST_YEARS
    lower_bound_percent: float = MIN_PERCENT
    upper_bound_percent: float = MAX_PERCENT
    interval_z_score: float = 1.96

    def __post_init__(self) -> None:
        """Validate configuration at creation time."""
        if not self.forecast_years:
            raise ValueError("forecast_years cannot be empty")
        if tuple(sorted(self.forecast_years)) != self.forecast_years:
            raise ValueError("forecast_years must be sorted")
        if self.lower_bound_percent >= self.upper_bound_percent:
            raise ValueError("lower bound must be smaller than upper bound")
        if self.interval_z_score <= 0:
            raise ValueError("interval_z_score must be positive")


DEFAULT_SCENARIOS: tuple[Scenario, ...] = (
    Scenario(
        name="Pessimistic",
        annual_adjustment_pp=-0.75,
        description="Slower activation and persistent affordability or trust barriers.",
    ),
    Scenario(
        name="Base",
        annual_adjustment_pp=0.0,
        description="Recent trend continues without an additional scenario adjustment.",
    ),
    Scenario(
        name="Optimistic",
        annual_adjustment_pp=0.75,
        description="Improved activation, interoperability, identity, and merchant acceptance.",
    ),
)
