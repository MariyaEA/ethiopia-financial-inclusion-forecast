# Forecasting Financial Inclusion in Ethiopia

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)](https://www.python.org/)
[![Testing](https://img.shields.io/badge/tests-pytest-0A9EDC)](https://docs.pytest.org/)
[![Dashboard](https://img.shields.io/badge/dashboard-Streamlit-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
<!-- CI_BADGE_START -->
[![CI](https://github.com/MariyaEA/ethiopia-financial-inclusion-forecast/actions/workflows/ci.yml/badge.svg)](https://github.com/MariyaEA/ethiopia-financial-inclusion-forecast/actions/workflows/ci.yml)
<!-- CI_BADGE_END -->

A reliability-focused, transparent forecasting system that helps finance-sector stakeholders understand Ethiopia's financial inclusion trajectory and explore bounded Access and Usage scenarios for 2025-2027.

> **Week 12 improvement objective:** transform the Week 11 analysis into a production-grade portfolio project built around reproducibility, automated testing, transparent forecasting, data-quality controls, and decision-ready communication.

## Business Problem

Ethiopia's digital-finance ecosystem is expanding rapidly, but growth in registrations and transaction activity does not automatically translate into broad, active, and equitable financial inclusion. The project supports three stakeholder groups:

- **Development finance institutions:** identify high-impact investment gaps and monitor inclusion outcomes.
- **Mobile money operators:** plan activation, interoperability, merchant, agent, and underserved-market initiatives.
- **National Bank of Ethiopia:** assess policy progress and identify risks related to access, active usage, trust, affordability, and inclusion gaps.

The decision problem is therefore not simply *how many accounts exist*, but whether new infrastructure and products are converting into **unique-adult Access** and **meaningful Usage**.

## Solution Overview

The project provides a transparent decision-support workflow:

1. Validate the unified financial-inclusion dataset and surface data-quality risks.
2. Separate demand-side outcomes from supply-side scale indicators.
3. Fit a simple bounded logit trend appropriate for sparse percentage data.
4. generate pessimistic, base, and optimistic scenarios with explicit adjustments.
5. Present results, assumptions, risks, and downloadable outputs in Streamlit.
6. Run automated linting and tests on every push and pull request.

The model intentionally favors explainability over complexity. With only five official account-ownership survey points between 2011 and 2024, a highly parameterized model would create false precision.

## Key Results From the Original Project

- Account ownership increased from **14% in 2011 to 49% in 2024**.
- Growth slowed to **+3 percentage points from 2021 to 2024**, compared with larger gains in earlier periods.
- 2024 digital-payment adoption is approximately **35%**, showing that usage behavior and account ownership must be analyzed separately.
- The enriched Week 11 dataset contained **65 records**: 35 observations, 11 events, 16 event-impact links, and 3 targets.
- The Week 12 version adds automated validation, scenario forecasting, test coverage, CI/CD, a model card, and finance-oriented risk controls.

## Week 12 Engineering Improvements

| Improvement | Portfolio value | Status |
|---|---|---|
| Modular typed Python package | Easier to test, review, and maintain | Complete |
| Data-quality and risk checks | Prevents silent failures and misleading outputs | Complete |
| Bounded scenario forecasting | Keeps percentage forecasts realistic and assumptions explicit | Complete |
| Automated pytest + coverage | Demonstrates correctness and regression protection | Complete |
| GitHub Actions CI | Runs linting and tests on every push/PR | Complete |
| Interactive Streamlit dashboard | Makes the business value understandable to non-technical users | Complete |
| Docker packaging | Creates a repeatable deployment path | Complete |

## Quick Start

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/ethiopia-financial-inclusion-forecast.git
cd ethiopia-financial-inclusion-forecast
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pytest
streamlit run dashboard/app.py
```

The dashboard automatically uses the first available file in this order:

1. `FI_DATA_PATH` environment variable
2. `data/processed/ethiopia_fi_unified_data.csv`
3. `data/raw/ethiopia_fi_unified_data.csv`
4. `data/demo/access_usage_demo.csv`

The included demo file is only a lightweight, documented fallback. The full Week 11 dataset should remain the primary source in the GitHub repository.

## Project Structure

```text
.
├── .github/workflows/ci.yml       # Automated linting and tests
├── dashboard/app.py               # Decision-focused Streamlit application
├── data/demo/                     # Lightweight reproducible demo data
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATA_CONTRACT.md
│   ├── MODEL_CARD.md
│   ├── WEEK12_GAP_ANALYSIS.md
│   └── WEEK12_IMPROVEMENT_PLAN.md
├── scripts/
│   ├── run_quality_report.py
│   └── set_ci_badge.py
├── src/fi_forecast/
│   ├── config.py                  # Dataclass configuration
│   ├── constants.py               # Named constants
│   ├── data.py                    # Loading and schema validation
│   ├── forecast.py                # Bounded scenario forecasts
│   ├── metrics.py                 # Business metrics
│   └── quality.py                 # Finance-oriented data controls
├── tests/                         # Unit and integration tests
├── WEEK12_INTERIM_SUBMISSION.md
├── Dockerfile
├── Makefile
└── pyproject.toml
```

## Dashboard

The Streamlit application contains five decision-oriented sections:

- **Executive Overview:** headline Access, Usage, slowdown, and target-gap metrics.
- **Indicator Explorer:** interactive time-series filtering and downloadable observations.
- **Scenario Forecasts:** bounded 2025-2027 forecasts with pessimistic/base/optimistic assumptions.
- **Reliability Controls:** validation checks for duplicates, missing evidence, range errors, and schema risks.
- **Model Card:** intended use, limitations, and safeguards against overclaiming causality.

Run locally:

```bash
streamlit run dashboard/app.py
```

Or with Docker:

```bash
docker build -t ethiopia-fi-forecast:week12 .
docker run --rm -p 8501:8501 ethiopia-fi-forecast:week12
```

## Testing and Quality

```bash
ruff check src tests dashboard scripts
pytest
```

The test suite covers schema validation, percentage bounds, business metrics, scenario ordering, forecast realism, duplicate detection, source completeness, and end-to-end demo-data loading.

After creating the GitHub remote, generate the real CI badge automatically:

```bash
python scripts/set_ci_badge.py
```

## Technical Details

### Data

The full project uses a unified schema with four record types:

- `observation`: measured indicator value;
- `event`: policy, launch, infrastructure change, market entry, or milestone;
- `impact_link`: transparent hypothesis linking an event to an indicator;
- `target`: official policy goal.

### Forecasting

The Week 12 baseline applies a logit transform to percentage outcomes, fits a linear trend in log-odds space, and transforms predictions back to percentages. This guarantees realistic bounds between 0% and 100%. Scenario adjustments are explicit percentage-point changes rather than hidden model behavior.

### Evaluation and Safeguards

- Forecasts are bounded.
- Inputs are validated before modeling.
- Scenario ordering is tested.
- The dashboard labels associations as non-causal.
- Registration, activity, account ownership, and transaction measures remain separate.
- Sparse-data limitations are displayed next to forecasts.

## Business Impact

This version reduces portfolio and decision risk by making the system:

- **reproducible:** clear dependencies, demo data, Docker, and run commands;
- **testable:** automated unit/integration tests and coverage threshold;
- **auditable:** explicit assumptions, data-quality findings, and model card;
- **usable:** interactive dashboard and downloadable forecast tables;
- **maintainable:** modular typed functions, dataclass configuration, named constants, and CI.

## Documentation

- [Week 12 interim submission](WEEK12_INTERIM_SUBMISSION.md)
- [Gap analysis](docs/WEEK12_GAP_ANALYSIS.md)
- [Improvement plan](docs/WEEK12_IMPROVEMENT_PLAN.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Data contract](docs/DATA_CONTRACT.md)
- [Model card](docs/MODEL_CARD.md)
- [Technical report draft](reports/WEEK12_TECHNICAL_REPORT.md)

## Future Improvements

- Add rolling-origin or leave-one-survey-out evaluation to the full historical pipeline.
- Calibrate event magnitudes using comparable-country evidence and expert review.
- Add disaggregated gender, region, income, and urban-rural series.
- Deploy the dashboard and add monitored data-refresh jobs.
- Add signed data snapshots and model versioning for stronger auditability.

## Author

**Mariamawit Alemu**  
Backend, Cloud, DevOps, and Data Engineering professional building reliable data products for emerging-market problems.

## License

MIT License. See [LICENSE](LICENSE).
