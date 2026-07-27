import pandas as pd

from fi_forecast.quality import findings_frame, quality_summary, run_quality_checks


def test_valid_frame_has_no_failures(valid_frame: pd.DataFrame) -> None:
    findings = run_quality_checks(valid_frame)
    summary = quality_summary(findings)
    assert summary["FAIL"] == 0
    assert summary["decision"] == "PASS"


def test_duplicate_ids_block_publication(valid_frame: pd.DataFrame) -> None:
    invalid = valid_frame.copy()
    invalid.loc[1, "record_id"] = "A"
    summary = quality_summary(run_quality_checks(invalid))
    assert summary["decision"] == "BLOCK"


def test_out_of_range_percentage_blocks_publication(valid_frame: pd.DataFrame) -> None:
    invalid = valid_frame.copy()
    invalid.loc[0, "value_numeric"] = 120
    findings = run_quality_checks(invalid)
    result = findings_frame(findings)
    row = result[result["check"] == "Percentage ranges"].iloc[0]
    assert row["severity"] == "FAIL"
    assert row["count"] == 1


def test_missing_source_generates_warning(valid_frame: pd.DataFrame) -> None:
    warning_frame = valid_frame.copy()
    warning_frame.loc[0, ["source_name", "source_url"]] = None
    summary = quality_summary(run_quality_checks(warning_frame))
    assert summary["decision"] == "REVIEW"


def test_missing_required_columns_returns_only_blocking_finding() -> None:
    frame = pd.DataFrame({"record_type": ["observation"]})
    findings = run_quality_checks(frame)
    assert len(findings) == 1
    assert findings[0].severity == "FAIL"
