from pathlib import Path

from fi_forecast.data import load_unified_data, observation_series
from fi_forecast.forecast import build_scenario_forecasts
from fi_forecast.quality import quality_summary, run_quality_checks


def test_demo_pipeline_end_to_end(demo_path: Path) -> None:
    frame = load_unified_data(demo_path)
    summary = quality_summary(run_quality_checks(frame))
    access = observation_series(frame, "ACC_OWNERSHIP")
    forecast = build_scenario_forecasts(
        access["year"].astype(int).tolist(),
        access["value_numeric"].astype(float).tolist(),
    )

    assert summary["decision"] == "PASS"
    assert len(forecast) == 9
    assert set(forecast["scenario"]) == {"Pessimistic", "Base", "Optimistic"}
