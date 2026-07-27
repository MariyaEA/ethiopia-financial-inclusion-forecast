from pathlib import Path

from src.data_loader import load_unified_data, split_records, validate_schema
from src.forecasting import build_forecast

ROOT = Path(__file__).resolve().parents[1]


def test_schema():
    d = load_unified_data(ROOT / "data/raw/ethiopia_fi_unified_data.csv")
    assert validate_schema(d) == []
    assert set(split_records(d)) == {"observation", "event", "impact_link", "target"}


def test_forecast():
    r = split_records(load_unified_data(ROOT / "data/raw/ethiopia_fi_unified_data.csv"))
    f = build_forecast(r["observation"], r["impact_link"], "ACC_OWNERSHIP")
    assert f.year.tolist() == [2025, 2026, 2027]
    assert f.forecast.between(0, 100).all()
