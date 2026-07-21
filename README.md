# Forecasting Financial Inclusion in Ethiopia

Complete 10 Academy KAIM Week 11 repository covering data enrichment, EDA, event-impact modeling, 2025–2027 forecasts, Streamlit dashboard, tests, and GitHub Actions.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
streamlit run dashboard/app.py
```

## Unified schema
- `observation`: measured value
- `event`: dated milestone; pillar blank
- `impact_link`: event-indicator relationship using `parent_id`
- `target`: analytical or policy benchmark

## Notebooks
1. `01_data_exploration_eda.ipynb`
2. `02_event_impact_modeling.ipynb`
3. `03_forecasting_2025_2027.ipynb`

## Dashboard
Metric cards, interactive trends, channel comparison, association heatmap, scenario forecasts with intervals, and progress toward benchmarks.

## Author
Mariamawit Ewnetu Alemu
