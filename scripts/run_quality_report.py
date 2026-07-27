"""Run data-quality checks from the command line."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from fi_forecast.data import load_unified_data
from fi_forecast.quality import findings_frame, quality_summary, run_quality_checks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run financial inclusion data-quality controls.")
    parser.add_argument("data_path", type=Path, help="Path to a unified CSV file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    frame = load_unified_data(args.data_path)
    findings = run_quality_checks(frame)
    print(findings_frame(findings).to_string(index=False))
    summary = quality_summary(findings)
    print(f"\nPublication decision: {summary['decision']}")
    return 1 if summary["decision"] == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
