"""Data loading, normalization, and schema validation."""

from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from fi_forecast.constants import REQUIRED_COLUMNS, VALID_RECORD_TYPES


class DataValidationError(ValueError):
    """Raised when input data violates a blocking schema rule."""


def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with lower-case snake-style column names."""
    normalized = frame.copy()
    normalized.columns = [
        str(column).strip().lower().replace(" ", "_").replace("-", "_")
        for column in normalized.columns
    ]
    return normalized


def validate_unified_schema(frame: pd.DataFrame) -> None:
    """Validate the minimum unified-schema contract.

    Raises:
        DataValidationError: If required columns are missing or record types are invalid.
    """
    missing = sorted(set(REQUIRED_COLUMNS) - set(frame.columns))
    if missing:
        raise DataValidationError(f"Missing required columns: {', '.join(missing)}")

    observed_types = set(frame["record_type"].dropna().astype(str).str.strip().str.lower())
    invalid_types = sorted(observed_types - set(VALID_RECORD_TYPES))
    if invalid_types:
        raise DataValidationError(f"Invalid record types: {', '.join(invalid_types)}")


def load_unified_data(path: str | Path) -> pd.DataFrame:
    """Load and validate a unified CSV file."""
    data_path = Path(path)
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    if data_path.suffix.lower() != ".csv":
        raise ValueError("Only CSV input is supported by the production loader")

    frame = normalize_columns(pd.read_csv(data_path))
    validate_unified_schema(frame)
    return frame


def resolve_data_path(candidates: Iterable[str | Path]) -> Path:
    """Return the first existing data path from an ordered set of candidates."""
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return path
    rendered = ", ".join(str(Path(candidate)) for candidate in candidates)
    raise FileNotFoundError(f"No financial inclusion dataset found. Checked: {rendered}")


def observation_series(frame: pd.DataFrame, indicator_code: str) -> pd.DataFrame:
    """Return a clean chronological observation series for one indicator."""
    validate_unified_schema(frame)
    observations = frame.loc[
        (frame["record_type"].astype(str).str.lower() == "observation")
        & (frame["indicator_code"].astype(str) == indicator_code)
    ].copy()

    observations["observation_date"] = pd.to_datetime(
        observations["observation_date"], errors="coerce"
    )
    observations["value_numeric"] = pd.to_numeric(observations["value_numeric"], errors="coerce")
    observations = observations.dropna(subset=["observation_date", "value_numeric"])
    observations["year"] = observations["observation_date"].dt.year
    return observations.sort_values("observation_date").reset_index(drop=True)


def available_indicator_codes(frame: pd.DataFrame) -> list[str]:
    """Return sorted observation indicator codes."""
    validate_unified_schema(frame)
    codes = frame.loc[
        frame["record_type"].astype(str).str.lower() == "observation", "indicator_code"
    ]
    return sorted(code for code in codes.dropna().astype(str).unique() if code)
