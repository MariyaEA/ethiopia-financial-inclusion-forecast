"""Named constants used across the project."""

from typing import Final

MIN_PERCENT: Final[float] = 0.0
MAX_PERCENT: Final[float] = 100.0
NUMERIC_EPSILON: Final[float] = 1e-6
DEFAULT_TARGET_PERCENT: Final[float] = 60.0
DEFAULT_FORECAST_YEARS: Final[tuple[int, ...]] = (2025, 2026, 2027)
VALID_RECORD_TYPES: Final[frozenset[str]] = frozenset(
    {"observation", "event", "impact_link", "target"}
)
REQUIRED_COLUMNS: Final[tuple[str, ...]] = (
    "record_type",
    "pillar",
    "indicator",
    "indicator_code",
    "value_numeric",
    "observation_date",
)
PERCENTAGE_INDICATOR_TOKENS: Final[tuple[str, ...]] = (
    "RATE",
    "SHARE",
    "PERCENT",
    "PENETRATION",
    "COVERAGE",
    "OWNERSHIP",
    "ADOPTION",
)
