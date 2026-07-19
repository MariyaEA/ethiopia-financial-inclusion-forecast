from pathlib import Path

from src.data_loader import load_reference_codes, load_unified_data, validate_schema
from src.eda import account_ownership_series

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "ethiopia_fi_enriched.csv"
REFS = ROOT / "data" / "raw" / "reference_codes.csv"


def test_files_load_successfully():
    assert not load_unified_data(DATA).empty
    assert not load_reference_codes(REFS).empty


def test_record_types_and_counts():
    df = load_unified_data(DATA)
    assert set(df["record_type"].dropna()) == {"observation", "event", "impact_link", "target"}
    assert len(df) == 65


def test_events_are_pillar_neutral():
    df = load_unified_data(DATA)
    assert df.loc[df["record_type"].eq("event"), "pillar"].isna().all()


def test_impact_links_point_to_events():
    df = load_unified_data(DATA)
    event_ids = set(df.loc[df["record_type"].eq("event"), "record_id"])
    parent_ids = set(df.loc[df["record_type"].eq("impact_link"), "parent_id"])
    assert parent_ids.issubset(event_ids)


def test_schema_validation_has_no_critical_issues():
    df = load_unified_data(DATA)
    issues = validate_schema(df)
    assert issues.empty, issues.to_dict("records")


def test_account_trajectory_includes_required_years():
    df = load_unified_data(DATA)
    years = set(account_ownership_series(df)["year"].astype(int))
    assert {2011, 2014, 2017, 2021, 2024}.issubset(years)


def test_new_ndps_event_and_links_present():
    df = load_unified_data(DATA)
    assert "EVT_0011" in set(df["record_id"])
    assert {"IMP_0015", "IMP_0016"}.issubset(set(df["record_id"]))
