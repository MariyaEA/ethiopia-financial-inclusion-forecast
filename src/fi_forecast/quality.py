"""Deterministic data-quality and model-risk controls."""

from dataclasses import dataclass
from typing import Literal

import pandas as pd

from fi_forecast.constants import (
    MAX_PERCENT,
    MIN_PERCENT,
    PERCENTAGE_INDICATOR_TOKENS,
    REQUIRED_COLUMNS,
    VALID_RECORD_TYPES,
)

Severity = Literal["PASS", "WARNING", "FAIL"]


@dataclass(frozen=True, slots=True)
class QualityFinding:
    """One deterministic quality-control result."""

    check: str
    severity: Severity
    count: int
    message: str


def run_quality_checks(frame: pd.DataFrame) -> list[QualityFinding]:
    """Run publication-oriented quality checks on a unified dataset."""
    findings: list[QualityFinding] = []
    findings.append(_check_required_columns(frame))

    if findings[0].severity == "FAIL":
        return findings

    findings.extend(
        [
            _check_record_types(frame),
            _check_duplicate_ids(frame),
            _check_observation_dates(frame),
            _check_percentage_ranges(frame),
            _check_source_evidence(frame),
        ]
    )
    return findings


def quality_summary(findings: list[QualityFinding]) -> dict[str, int | str]:
    """Summarize quality findings and derive a publication decision."""
    counts = {
        "PASS": sum(finding.severity == "PASS" for finding in findings),
        "WARNING": sum(finding.severity == "WARNING" for finding in findings),
        "FAIL": sum(finding.severity == "FAIL" for finding in findings),
    }
    decision = "BLOCK" if counts["FAIL"] else "REVIEW" if counts["WARNING"] else "PASS"
    return {**counts, "decision": decision}


def findings_frame(findings: list[QualityFinding]) -> pd.DataFrame:
    """Convert findings to a dashboard-ready table."""
    return pd.DataFrame(
        [
            {
                "check": finding.check,
                "severity": finding.severity,
                "count": finding.count,
                "message": finding.message,
            }
            for finding in findings
        ]
    )


def _check_required_columns(frame: pd.DataFrame) -> QualityFinding:
    missing = sorted(set(REQUIRED_COLUMNS) - set(frame.columns))
    if missing:
        return QualityFinding(
            check="Required columns",
            severity="FAIL",
            count=len(missing),
            message=f"Missing columns: {', '.join(missing)}",
        )
    return QualityFinding("Required columns", "PASS", 0, "All minimum columns are present.")


def _check_record_types(frame: pd.DataFrame) -> QualityFinding:
    values = set(frame["record_type"].dropna().astype(str).str.strip().str.lower())
    invalid = sorted(values - set(VALID_RECORD_TYPES))
    if invalid:
        return QualityFinding(
            "Record types",
            "FAIL",
            len(invalid),
            f"Invalid record types: {', '.join(invalid)}",
        )
    return QualityFinding("Record types", "PASS", 0, "All record types are valid.")


def _check_duplicate_ids(frame: pd.DataFrame) -> QualityFinding:
    if "record_id" not in frame.columns:
        return QualityFinding(
            "Duplicate record IDs",
            "WARNING",
            0,
            "record_id is not available, so uniqueness cannot be verified.",
        )
    duplicate_count = int(frame["record_id"].dropna().duplicated().sum())
    if duplicate_count:
        return QualityFinding(
            "Duplicate record IDs",
            "FAIL",
            duplicate_count,
            "Duplicate record IDs must be resolved before publication.",
        )
    return QualityFinding("Duplicate record IDs", "PASS", 0, "Record IDs are unique.")


def _check_observation_dates(frame: pd.DataFrame) -> QualityFinding:
    observations = frame[frame["record_type"].astype(str).str.lower() == "observation"]
    parsed = pd.to_datetime(observations["observation_date"], errors="coerce")
    invalid_count = int(parsed.isna().sum())
    if invalid_count:
        return QualityFinding(
            "Observation dates",
            "FAIL",
            invalid_count,
            "Observation rows contain missing or unparseable dates.",
        )
    return QualityFinding("Observation dates", "PASS", 0, "Observation dates are parseable.")


def _check_percentage_ranges(frame: pd.DataFrame) -> QualityFinding:
    codes = frame["indicator_code"].fillna("").astype(str).str.upper()
    is_percentage = codes.apply(
        lambda code: any(token in code for token in PERCENTAGE_INDICATOR_TOKENS)
    )
    values = pd.to_numeric(frame["value_numeric"], errors="coerce")
    out_of_range = (
        is_percentage & values.notna() & ((values < MIN_PERCENT) | (values > MAX_PERCENT))
    )
    count = int(out_of_range.sum())
    if count:
        return QualityFinding(
            "Percentage ranges",
            "FAIL",
            count,
            "Percentage indicators contain values outside 0-100.",
        )
    return QualityFinding("Percentage ranges", "PASS", 0, "Percentage values are within bounds.")


def _check_source_evidence(frame: pd.DataFrame) -> QualityFinding:
    observations = frame[frame["record_type"].astype(str).str.lower() == "observation"]
    source_name = observations.get("source_name", pd.Series(index=observations.index, dtype=object))
    source_url = observations.get("source_url", pd.Series(index=observations.index, dtype=object))
    missing = source_name.fillna("").astype(str).str.strip().eq("") & source_url.fillna("").astype(
        str
    ).str.strip().eq("")
    count = int(missing.sum())
    if count:
        return QualityFinding(
            "Source evidence",
            "WARNING",
            count,
            "Some observations have neither source_name nor source_url.",
        )
    return QualityFinding("Source evidence", "PASS", 0, "Observation sources are documented.")
