from pathlib import Path

import pandas as pd
import pytest

from fi_forecast.data import (
    DataValidationError,
    available_indicator_codes,
    load_unified_data,
    normalize_columns,
    observation_series,
    resolve_data_path,
    validate_unified_schema,
)


def test_normalize_columns() -> None:
    frame = pd.DataFrame(columns=["Record Type", "Indicator-Code"])
    assert list(normalize_columns(frame).columns) == ["record_type", "indicator_code"]


def test_validate_schema_rejects_missing_columns(valid_frame: pd.DataFrame) -> None:
    with pytest.raises(DataValidationError, match="Missing required columns"):
        validate_unified_schema(valid_frame.drop(columns=["pillar"]))


def test_validate_schema_rejects_invalid_record_type(valid_frame: pd.DataFrame) -> None:
    invalid = valid_frame.copy()
    invalid.loc[0, "record_type"] = "prediction"
    with pytest.raises(DataValidationError, match="Invalid record types"):
        validate_unified_schema(invalid)


def test_load_demo_data_and_extract_series(demo_path: Path) -> None:
    frame = load_unified_data(demo_path)
    series = observation_series(frame, "ACC_OWNERSHIP")
    assert series["year"].tolist() == [2011, 2014, 2017, 2021, 2024]
    assert series.iloc[-1]["value_numeric"] == 49


def test_available_indicator_codes(valid_frame: pd.DataFrame) -> None:
    assert available_indicator_codes(valid_frame) == ["ACC_OWNERSHIP"]


def test_resolve_data_path_returns_first_existing(tmp_path: Path) -> None:
    existing = tmp_path / "data.csv"
    existing.write_text("x\n1\n", encoding="utf-8")
    assert resolve_data_path([tmp_path / "missing.csv", existing]) == existing


def test_load_rejects_non_csv(tmp_path: Path) -> None:
    path = tmp_path / "data.xlsx"
    path.write_text("not a workbook", encoding="utf-8")
    with pytest.raises(ValueError, match="Only CSV"):
        load_unified_data(path)
