from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def valid_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "record_id": ["A", "B", "C"],
            "record_type": ["observation", "event", "target"],
            "pillar": ["Access", None, "Access"],
            "indicator": ["Account ownership", "Policy launch", "Target"],
            "indicator_code": ["ACC_OWNERSHIP", None, "ACC_OWNERSHIP"],
            "value_numeric": [49.0, None, 60.0],
            "observation_date": ["2024-12-31", None, "2025-12-31"],
            "source_name": ["Findex", "Regulator", "Strategy"],
            "source_url": ["source-a", "source-b", "source-c"],
            "confidence": ["high", "high", "high"],
        }
    )


@pytest.fixture
def demo_path() -> Path:
    return Path("data/demo/access_usage_demo.csv")
