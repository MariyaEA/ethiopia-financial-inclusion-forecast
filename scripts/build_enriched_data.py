"""Command-line entry point for rebuilding the Task 1 enriched dataset."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.enrichment import build_enriched_dataset, enrichment_frame

RAW = ROOT / "data" / "raw" / "ethiopia_fi_unified_data.csv"
OUT = ROOT / "data" / "processed" / "ethiopia_fi_enriched.csv"
ADDITIONS = ROOT / "data" / "processed" / "enrichment_records.csv"

if __name__ == "__main__":
    additions = enrichment_frame()
    additions.to_csv(ADDITIONS, index=False)
    enriched = build_enriched_dataset(RAW, OUT)
    print(f"Wrote {len(additions)} enrichment records to {ADDITIONS}")
    print(f"Wrote {len(enriched)} total records to {OUT}")
