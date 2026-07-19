# Forecasting Financial Inclusion in Ethiopia

Week 11 interim submission for the 10 Academy KAIM challenge. This repository completes:

- **Task 1:** Data Exploration and Enrichment
- **Task 2:** Exploratory Data Analysis

The analysis tracks Ethiopia's two core Global Findex dimensions:

- **Access:** account ownership and the ability to enter the financial system
- **Usage:** digital-payment adoption and meaningful transaction behavior

## Interim Deliverables

- Unified starter dataset converted to CSV and loaded successfully
- Reference codes loaded and used for schema validation
- Enriched dataset with 8 documented additions
- Reproducible enrichment script
- Executed EDA notebook with visualizations
- Account ownership trajectory and growth-rate analysis
- Mobile-money and digital-payment usage analysis
- Registered-versus-active gap analysis
- Infrastructure and event timeline analysis
- Event-to-indicator impact matrix
- Interim report with key insights and limitations
- Unit tests and GitHub Actions workflow

## Repository Structure

```text
ethiopia-fi-forecast-interim/
├── .github/workflows/unittests.yml
├── data/
│   ├── raw/
│   │   ├── ethiopia_fi_unified_data.csv
│   │   └── reference_codes.csv
│   └── processed/
│       ├── enrichment_records.csv
│       ├── ethiopia_fi_enriched.csv
│       ├── indicator_coverage.csv
│       ├── impact_links_joined.csv
│       └── record_summary.csv
├── notebooks/
│   ├── 01_data_exploration_and_eda.ipynb
│   └── README.md
├── src/
│   ├── data_loader.py
│   ├── eda.py
│   └── enrichment.py
├── scripts/build_enriched_data.py
├── tests/test_data_loader.py
├── reports/
│   ├── figures/
│   └── interim_report.md
├── docs/SCHEMA_DESIGN.md
├── data_enrichment_log.md
├── SUBMISSION_GUIDE.md
├── requirements.txt
└── .gitignore
```

## Unified Schema

Every record uses the same columns, but `record_type` determines how a row is interpreted:

| record_type | Meaning | category | pillar | parent_id |
|---|---|---|---|---|
| observation | Measured value | blank | required | blank |
| target | Official goal | blank | required | blank |
| event | Neutral policy/product/infrastructure event | required | **blank** | blank |
| impact_link | Modeled event-to-indicator relationship | blank | required | event record ID |

Events are intentionally not assigned to a pillar. Their effects are represented through one or more `impact_link` rows joined by `parent_id`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Rebuild the Enriched Dataset

```bash
python scripts/build_enriched_data.py
```

## Run the Notebook

```bash
jupyter notebook notebooks/01_data_exploration_and_eda.ipynb
```

The submitted notebook is already executed and contains outputs. Re-running it regenerates figures and processed summary tables.

## Run Tests

```bash
pytest -q
```

## Main Data Sources

- World Bank Global Findex
- National Bank of Ethiopia
- EthSwitch
- Ethio Telecom
- Safaricom Ethiopia
- Fayda National ID Program
- ITU/A4AI and GSMA research included in the starter dataset

Source URLs for every new record are documented in `data_enrichment_log.md` and in the dataset itself.

## Important Analytical Cautions

- The Global Findex series has only five account-ownership survey points.
- Operator account counts can include duplicate, inactive, or multi-provider accounts and should not be treated as unique adults.
- Many indicators have only one observation, making formal correlations unreliable.
- Event impact estimates are hypotheses for Task 3, not proven causal effects.
- Approximate figures are marked with medium confidence.

