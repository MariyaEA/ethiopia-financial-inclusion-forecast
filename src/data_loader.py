"""Loading and validation helpers for the unified financial inclusion schema."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd

REQUIRED_COLUMNS = [
    "record_id",
    "parent_id",
    "record_type",
    "category",
    "pillar",
    "indicator",
    "indicator_code",
    "indicator_direction",
    "value_numeric",
    "value_text",
    "value_type",
    "unit",
    "observation_date",
    "period_start",
    "period_end",
    "fiscal_year",
    "gender",
    "location",
    "region",
    "source_name",
    "source_type",
    "source_url",
    "confidence",
    "related_indicator",
    "relationship_type",
    "impact_direction",
    "impact_magnitude",
    "impact_estimate",
    "lag_months",
    "evidence_basis",
    "comparable_country",
    "collected_by",
    "collection_date",
    "original_text",
    "notes",
]

DATE_COLUMNS = ["observation_date", "period_start", "period_end", "collection_date"]
NUMERIC_COLUMNS = ["value_numeric", "impact_estimate", "lag_months"]
ALLOWED_RECORD_TYPES = {"observation", "event", "impact_link", "target"}


def load_unified_data(path: str | Path) -> pd.DataFrame:
    """Load a unified CSV, standardize blanks, parse dates, and check columns.

    Raises:
        FileNotFoundError: if the input file does not exist.
        ValueError: if required schema columns are absent.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Unified dataset not found: {path}")

    try:
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"Unified dataset is empty: {path}") from exc

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[REQUIRED_COLUMNS].copy()
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(df[column], errors="coerce", format="mixed")
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def load_reference_codes(path: str | Path) -> pd.DataFrame:
    """Load the categorical reference-code table."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Reference codes not found: {path}")
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    expected = {"field", "code", "description", "applies_to"}
    if not expected.issubset(df.columns):
        raise ValueError(f"Reference code file must contain: {sorted(expected)}")
    return df.replace(r"^\s*$", pd.NA, regex=True)


def split_records(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Return a copy of each record type in a dictionary."""
    return {
        record_type: df.loc[df["record_type"].eq(record_type)].copy()
        for record_type in sorted(ALLOWED_RECORD_TYPES)
    }


def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Return row-level validation issues without stopping exploratory analysis."""
    issues: List[dict] = []

    def add(mask: pd.Series, rule: str, message: str) -> None:
        for _, row in df.loc[mask, ["record_id", "record_type"]].iterrows():
            issues.append(
                {
                    "record_id": row["record_id"],
                    "record_type": row["record_type"],
                    "rule": rule,
                    "message": message,
                }
            )

    add(
        ~df["record_type"].isin(ALLOWED_RECORD_TYPES),
        "valid_record_type",
        "record_type is not in the supported code list",
    )
    add(
        df["record_id"].duplicated(keep=False),
        "unique_record_id",
        "record_id must be unique",
    )
    add(
        df["record_type"].eq("event") & df["pillar"].notna(),
        "event_pillar_blank",
        "events must remain pillar-neutral",
    )
    add(
        df["record_type"].isin(["observation", "target", "impact_link"])
        & df["pillar"].isna(),
        "pillar_required",
        "pillar is required for observations, targets, and impact links",
    )
    add(
        df["record_type"].eq("observation") & df["indicator_code"].isna(),
        "observation_indicator_code",
        "observations require indicator_code",
    )
    add(
        df["record_type"].eq("event") & df["category"].isna(),
        "event_category_required",
        "events require an event category",
    )
    add(
        df["record_type"].eq("impact_link") & df["parent_id"].isna(),
        "impact_parent_required",
        "impact links require parent_id",
    )
    add(
        df["record_type"].eq("impact_link") & df["related_indicator"].isna(),
        "impact_indicator_required",
        "impact links require related_indicator",
    )

    event_ids = set(df.loc[df["record_type"].eq("event"), "record_id"].dropna())
    bad_parent = df["record_type"].eq("impact_link") & ~df["parent_id"].isin(event_ids)
    add(
        bad_parent,
        "impact_parent_exists",
        "parent_id must refer to an event record",
    )

    return pd.DataFrame(
        issues,
        columns=["record_id", "record_type", "rule", "message"],
    )
