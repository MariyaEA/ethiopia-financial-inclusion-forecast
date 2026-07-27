"""Streamlit dashboard for transparent financial inclusion scenarios."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from fi_forecast.config import DEFAULT_SCENARIOS, ForecastConfig  # noqa: E402
from fi_forecast.constants import DEFAULT_TARGET_PERCENT  # noqa: E402
from fi_forecast.data import (  # noqa: E402
    available_indicator_codes,
    load_unified_data,
    observation_series,
    resolve_data_path,
)
from fi_forecast.forecast import build_scenario_forecasts  # noqa: E402
from fi_forecast.metrics import (  # noqa: E402
    annualized_change_pp,
    gap_to_target,
    latest_value,
    percentage_point_change,
    progress_to_target,
)
from fi_forecast.quality import (  # noqa: E402
    findings_frame,
    quality_summary,
    run_quality_checks,
)

ACCESS_CODE = "ACC_OWNERSHIP"
USAGE_CODE = "USG_DIGITAL_PAYMENT"


@st.cache_data(show_spinner=False)
def load_dashboard_data() -> tuple[pd.DataFrame, Path]:
    """Load the first available dataset using a deterministic priority order."""
    env_path = os.getenv("FI_DATA_PATH")
    candidates = [
        candidate
        for candidate in (
            env_path,
            PROJECT_ROOT / "data/processed/ethiopia_fi_unified_data.csv",
            PROJECT_ROOT / "data/raw/ethiopia_fi_unified_data.csv",
            PROJECT_ROOT / "data/demo/access_usage_demo.csv",
        )
        if candidate
    ]
    selected = resolve_data_path(candidates)
    return load_unified_data(selected), selected


def render_overview(frame: pd.DataFrame) -> None:
    """Render business headline metrics and interpretation."""
    st.header("Executive Overview")
    access = observation_series(frame, ACCESS_CODE)
    usage = observation_series(frame, USAGE_CODE)

    access_year, access_value = latest_value(access)
    usage_year, usage_value = latest_value(usage)
    latest_two = access.tail(2)
    slowdown = percentage_point_change(
        float(latest_two.iloc[0]["value_numeric"]),
        float(latest_two.iloc[1]["value_numeric"]),
    )
    annualized = annualized_change_pp(
        float(latest_two.iloc[0]["value_numeric"]),
        float(latest_two.iloc[1]["value_numeric"]),
        int(latest_two.iloc[0]["year"]),
        int(latest_two.iloc[1]["year"]),
    )

    columns = st.columns(4)
    columns[0].metric("Latest Access", f"{access_value:.1f}%", f"{access_year}")
    columns[1].metric("Latest Usage", f"{usage_value:.1f}%", f"{usage_year}")
    columns[2].metric("Latest Access change", f"+{slowdown:.1f} pp", f"{annualized:.1f} pp/year")
    columns[3].metric(
        "Gap to 60% target",
        f"{gap_to_target(access_value, DEFAULT_TARGET_PERCENT):.1f} pp",
        f"{progress_to_target(access_value, DEFAULT_TARGET_PERCENT):.0f}% achieved",
    )

    st.info(
        "The key decision risk is confusing rapid growth in registrations or transactions "
        "with growth in unique-adult account ownership. The dashboard keeps these measures separate."
    )

    chart = px.line(
        access,
        x="year",
        y="value_numeric",
        markers=True,
        labels={"year": "Year", "value_numeric": "Account ownership (%)"},
        title="Account ownership trajectory",
    )
    chart.update_yaxes(range=[0, 100])
    st.plotly_chart(chart, use_container_width=True)


def render_indicator_explorer(frame: pd.DataFrame) -> None:
    """Render an interactive indicator explorer."""
    st.header("Indicator Explorer")
    codes = available_indicator_codes(frame)
    selected = st.selectbox(
        "Indicator code", codes, index=codes.index(ACCESS_CODE) if ACCESS_CODE in codes else 0
    )
    series = observation_series(frame, selected)
    if series.empty:
        st.warning("No valid dated observations are available for this indicator.")
        return

    label = (
        series["indicator"].dropna().astype(str).iloc[-1]
        if series["indicator"].notna().any()
        else selected
    )
    chart = px.line(
        series,
        x="observation_date",
        y="value_numeric",
        markers=True,
        hover_data=["source_name", "confidence"],
        labels={"observation_date": "Date", "value_numeric": "Value"},
        title=label,
    )
    st.plotly_chart(chart, use_container_width=True)
    st.dataframe(
        series[
            [
                "observation_date",
                "indicator",
                "indicator_code",
                "value_numeric",
                "source_name",
                "confidence",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Download selected observations",
        data=series.to_csv(index=False).encode("utf-8"),
        file_name=f"{selected.lower()}_observations.csv",
        mime="text/csv",
    )


def render_forecasts(frame: pd.DataFrame) -> None:
    """Render bounded scenario forecasts and assumptions."""
    st.header("Scenario Forecasts")
    access = observation_series(frame, ACCESS_CODE)
    years = access["year"].astype(int).tolist()
    values = access["value_numeric"].astype(float).tolist()

    selected_names = st.multiselect(
        "Scenarios",
        options=[scenario.name for scenario in DEFAULT_SCENARIOS],
        default=[scenario.name for scenario in DEFAULT_SCENARIOS],
    )
    selected_scenarios = tuple(
        scenario for scenario in DEFAULT_SCENARIOS if scenario.name in selected_names
    )
    if not selected_scenarios:
        st.warning("Select at least one scenario.")
        return

    forecast = build_scenario_forecasts(
        years,
        values,
        scenarios=selected_scenarios,
        config=ForecastConfig(),
    )

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=access["year"],
            y=access["value_numeric"],
            mode="lines+markers",
            name="Observed Access",
        )
    )
    for scenario_name in selected_names:
        scenario_frame = forecast[forecast["scenario"] == scenario_name]
        figure.add_trace(
            go.Scatter(
                x=scenario_frame["year"],
                y=scenario_frame["forecast_percent"],
                mode="lines+markers",
                name=scenario_name,
                error_y={
                    "type": "data",
                    "symmetric": False,
                    "array": scenario_frame["upper_percent"] - scenario_frame["forecast_percent"],
                    "arrayminus": scenario_frame["forecast_percent"]
                    - scenario_frame["lower_percent"],
                    "visible": True,
                },
            )
        )
    figure.update_layout(
        title="Bounded account ownership scenarios, 2025-2027",
        xaxis_title="Year",
        yaxis_title="Account ownership (%)",
        yaxis_range=[0, 100],
    )
    st.plotly_chart(figure, use_container_width=True)

    st.caption(
        "Planning ranges are based on sparse historical data and residual variation. They should not be interpreted as fully calibrated causal confidence intervals."
    )
    st.dataframe(
        forecast.round(2),
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Download scenario forecasts",
        data=forecast.to_csv(index=False).encode("utf-8"),
        file_name="access_scenario_forecasts_2025_2027.csv",
        mime="text/csv",
    )


def render_reliability(frame: pd.DataFrame) -> None:
    """Render data-quality controls and publication decision."""
    st.header("Reliability Controls")
    findings = run_quality_checks(frame)
    summary = quality_summary(findings)

    columns = st.columns(4)
    columns[0].metric("Publication decision", str(summary["decision"]))
    columns[1].metric("Passed checks", int(summary["PASS"]))
    columns[2].metric("Warnings", int(summary["WARNING"]))
    columns[3].metric("Failed checks", int(summary["FAIL"]))

    st.dataframe(findings_frame(findings), use_container_width=True, hide_index=True)
    if summary["decision"] == "BLOCK":
        st.error("Blocking data-quality failures must be resolved before publishing forecasts.")
    elif summary["decision"] == "REVIEW":
        st.warning("Warnings require reviewer sign-off before publication.")
    else:
        st.success("All configured quality controls passed.")


def render_model_card() -> None:
    """Render intended use and model limitations."""
    st.header("Model Card")
    st.subheader("Intended use")
    st.write(
        "Explore plausible national Access scenarios, compare explicit assumptions, and support stakeholder planning discussions."
    )
    st.subheader("Not intended for")
    st.write(
        "Causal policy evaluation, individual credit decisions, or precise long-horizon forecasting."
    )
    st.subheader("Why this model")
    st.write(
        "A bounded logit trend is deliberately simple and transparent. With five official Access observations, a complex model would risk overfitting and false precision."
    )
    st.subheader("Main limitations")
    st.write(
        "Sparse and irregular survey data, limited Usage history, overlapping events, inconsistent provider definitions, and missing disaggregation."
    )
    st.subheader("Safeguards")
    st.write(
        "Bounded outputs, explicit scenarios, automated data checks, tests, visible assumptions, and non-causal language."
    )


def main() -> None:
    st.set_page_config(
        page_title="Ethiopia Financial Inclusion Forecast",
        page_icon="📊",
        layout="wide",
    )
    st.title("Ethiopia Financial Inclusion Decision System")
    st.caption(
        "Week 12 production-grade improvement: reliability, transparency, and business impact"
    )

    try:
        frame, selected_path = load_dashboard_data()
    except (FileNotFoundError, ValueError) as error:
        st.error(str(error))
        st.stop()

    with st.sidebar:
        st.subheader("Navigation")
        page = st.radio(
            "Page",
            (
                "Executive Overview",
                "Indicator Explorer",
                "Scenario Forecasts",
                "Reliability Controls",
                "Model Card",
            ),
        )
        st.divider()
        st.caption(f"Data source: `{selected_path}`")
        st.caption("Associations and scenarios are not causal claims.")

    renderers = {
        "Executive Overview": render_overview,
        "Indicator Explorer": render_indicator_explorer,
        "Scenario Forecasts": render_forecasts,
        "Reliability Controls": render_reliability,
    }
    if page == "Model Card":
        render_model_card()
    else:
        renderers[page](frame)


if __name__ == "__main__":
    main()
