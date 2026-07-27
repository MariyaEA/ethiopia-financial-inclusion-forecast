import pandas as pd
import pytest

from fi_forecast.metrics import (
    activation_rate,
    annualized_change_pp,
    gap_to_target,
    latest_value,
    percentage_point_change,
    progress_to_target,
)


def test_percentage_point_change() -> None:
    assert percentage_point_change(46, 49) == 3


def test_annualized_change() -> None:
    assert annualized_change_pp(46, 49, 2021, 2024) == 1


def test_progress_and_gap_to_target() -> None:
    assert progress_to_target(49, 60) == pytest.approx(81.6667, rel=1e-4)
    assert gap_to_target(49, 60) == 11


def test_activation_rate() -> None:
    assert activation_rate(7.1, 10.8) == pytest.approx(65.7407, rel=1e-4)


def test_activation_rate_rejects_impossible_values() -> None:
    with pytest.raises(ValueError, match="cannot exceed"):
        activation_rate(11, 10)


def test_latest_value() -> None:
    frame = pd.DataFrame({"year": [2021, 2024], "value_numeric": [46, 49]})
    assert latest_value(frame) == (2024, 49.0)
