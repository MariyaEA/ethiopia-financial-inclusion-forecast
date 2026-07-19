"""Reusable transformations for Task 1 and Task 2 exploratory analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd


def record_summary(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Produce compact count tables used in the dataset overview."""
    return {
        "record_type": df["record_type"].value_counts(dropna=False).rename_axis("record_type").reset_index(name="count"),
        "pillar": df["pillar"].fillna("(blank / event-neutral)").value_counts().rename_axis("pillar").reset_index(name="count"),
        "source_type": df["source_type"].fillna("(missing)").value_counts().rename_axis("source_type").reset_index(name="count"),
        "confidence": df["confidence"].fillna("(missing)").value_counts().rename_axis("confidence").reset_index(name="count"),
    }


def indicator_coverage(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize temporal coverage and sparsity for observation indicators."""
    obs = df.loc[df["record_type"].eq("observation")].copy()
    obs["year"] = obs["observation_date"].dt.year
    coverage = (
        obs.groupby(["indicator_code", "indicator"], dropna=False)
        .agg(
            observations=("record_id", "count"),
            first_year=("year", "min"),
            last_year=("year", "max"),
            unique_years=("year", "nunique"),
            confidence_modes=("confidence", lambda x: ", ".join(sorted(set(x.dropna().astype(str))))),
        )
        .reset_index()
        .sort_values(["unique_years", "indicator_code"], ascending=[True, True])
    )
    return coverage


def temporal_coverage_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Create indicator-by-year observation counts for a coverage heatmap."""
    obs = df.loc[df["record_type"].eq("observation")].copy()
    obs["year"] = obs["observation_date"].dt.year
    matrix = pd.crosstab(obs["indicator_code"], obs["year"])
    return matrix.sort_index()


def account_ownership_series(df: pd.DataFrame) -> pd.DataFrame:
    """Return the national, all-gender Global Findex access trajectory."""
    series = df.loc[
        df["record_type"].eq("observation")
        & df["indicator_code"].eq("ACC_OWNERSHIP")
        & df["gender"].fillna("all").eq("all")
        & df["location"].fillna("national").eq("national"),
        ["observation_date", "value_numeric", "confidence", "source_name"],
    ].copy()
    series["year"] = series["observation_date"].dt.year
    return series.dropna(subset=["year", "value_numeric"]).sort_values("year")


def growth_rates(series: pd.DataFrame) -> pd.DataFrame:
    """Calculate percentage-point and annualized changes between survey years."""
    out = series[["year", "value_numeric"]].copy().reset_index(drop=True)
    out["years_elapsed"] = out["year"].diff()
    out["change_pp"] = out["value_numeric"].diff()
    out["annualized_pp"] = out["change_pp"] / out["years_elapsed"]
    out["period"] = out["year"].shift(1).astype("Int64").astype(str) + "-" + out["year"].astype("Int64").astype(str)
    return out.dropna(subset=["change_pp"])


def observation_series(df: pd.DataFrame, indicator_code: str) -> pd.DataFrame:
    """Return all dated observations for a named indicator."""
    out = df.loc[
        df["record_type"].eq("observation") & df["indicator_code"].eq(indicator_code),
        ["observation_date", "value_numeric", "indicator", "gender", "location", "source_name", "confidence"],
    ].copy()
    out["year"] = out["observation_date"].dt.year
    return out.sort_values("observation_date")


def joined_impact_links(df: pd.DataFrame) -> pd.DataFrame:
    """Join impact links to their neutral parent events through parent_id."""
    links = df.loc[df["record_type"].eq("impact_link")].copy()
    events = df.loc[df["record_type"].eq("event"), ["record_id", "indicator", "category", "observation_date"]].copy()
    events = events.rename(
        columns={
            "record_id": "event_id",
            "indicator": "event_name",
            "category": "event_category",
            "observation_date": "event_date",
        }
    )
    return links.merge(events, left_on="parent_id", right_on="event_id", how="left", validate="many_to_one")


def impact_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Create an event-indicator matrix using impact estimates where available."""
    joined = joined_impact_links(df)
    joined["matrix_value"] = joined["impact_estimate"].fillna(0)
    return joined.pivot_table(
        index="event_name",
        columns="related_indicator",
        values="matrix_value",
        aggfunc="sum",
        fill_value=0,
    )


def pairwise_indicator_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """Compute exploratory pairwise correlations and overlap counts by year.

    With sparse irregular series, correlations with fewer than three overlapping years
    are retained only to demonstrate why statistical conclusions are not reliable.
    """
    obs = df.loc[df["record_type"].eq("observation")].copy()
    obs = obs.loc[obs["gender"].fillna("all").eq("all")]
    obs["year"] = obs["observation_date"].dt.year
    yearly = obs.pivot_table(index="year", columns="indicator_code", values="value_numeric", aggfunc="mean")

    rows: list[dict] = []
    columns = list(yearly.columns)
    for i, left in enumerate(columns):
        for right in columns[i + 1 :]:
            pair = yearly[[left, right]].dropna()
            if len(pair) >= 2:
                rows.append(
                    {
                        "indicator_a": left,
                        "indicator_b": right,
                        "overlap_years": len(pair),
                        "pearson_r": pair[left].corr(pair[right]),
                    }
                )
    if not rows:
        return pd.DataFrame(columns=["indicator_a", "indicator_b", "overlap_years", "pearson_r"])
    return pd.DataFrame(rows).sort_values(["overlap_years", "pearson_r"], ascending=[False, False])


def normalized_gap(registered: float, active: float) -> dict[str, float]:
    """Return activity and inactivity rates from registered and active counts."""
    if registered <= 0:
        raise ValueError("registered must be greater than zero")
    activity_rate = active / registered * 100
    return {
        "registered": registered,
        "active": active,
        "activity_rate": activity_rate,
        "inactive_share": 100 - activity_rate,
    }
