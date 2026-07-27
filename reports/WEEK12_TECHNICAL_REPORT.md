# From Analysis to a Reliable Financial Inclusion Data Product

## Executive Summary

The Week 11 project answered an important analytical question: why has Ethiopia's rapid growth in digital-finance infrastructure and registrations not translated one-for-one into unique-adult financial inclusion? Week 12 focused on a different question: can the analysis be trusted, reproduced, reviewed, and used as a professional finance-sector data product?

The improved repository introduces modular code, automated tests, CI/CD, bounded scenario forecasting, data-quality controls, Docker packaging, an upgraded dashboard, and formal model documentation. The main achievement is not a more complicated model. It is a more reliable system around the model.

## The Financial Problem

Account ownership rose from 14% in 2011 to 49% in 2024, but the latest three-year period added only 3 percentage points. At the same time, digital payments, mobile-money registrations, 4G coverage, and interoperable transaction volumes expanded rapidly. These measures describe different populations and behaviors. Treating them as interchangeable creates decision risk.

The system therefore separates:

- unique-adult account ownership;
- digital-payment usage;
- registered accounts;
- active accounts;
- transaction volumes;
- policy and product events.

## Why Reliability Matters

Finance-sector users need more than a chart. They need evidence that:

- invalid data is detected;
- calculations are repeatable;
- assumptions are visible;
- percentages cannot exceed realistic bounds;
- changes cannot be merged without automated checks;
- limitations are communicated next to results.

## Engineering Improvements

### Modular Refactoring

Core logic now lives in a typed package rather than the presentation layer. Data loading, validation, quality checks, business metrics, and forecasting can be tested independently.

### Automated Testing and CI

The test suite covers schema failures, invalid values, duplicates, source completeness, scenario ordering, forecast bounds, and business calculations. GitHub Actions runs Ruff and pytest for every push and pull request, with an 85% coverage gate.

### Bounded Forecasting

The baseline uses a logit transformation. This is appropriate for percentages because transformed forecasts remain within 0-100% after inversion. Scenario changes are explicit percentage-point adjustments, which makes them understandable to non-technical stakeholders.

### Reliability Dashboard

The Streamlit dashboard now includes a dedicated reliability view. Users can see data-quality findings before interpreting a forecast. The model card is also available in the interface.

## Business Impact

The improved system reduces four practical risks:

1. **Data risk:** invalid ranges, duplicates, and missing evidence are surfaced.
2. **Model risk:** sparse-data limitations and assumptions are visible.
3. **Operational risk:** Docker, pinned dependencies, and automated tests improve reproducibility.
4. **Communication risk:** the dashboard separates scale indicators from inclusion outcomes.

## Lessons Learned

The most portfolio-relevant lesson is that advanced work does not always mean adding a more complex algorithm. In a sparse, high-stakes setting, professionalism comes from disciplined assumptions, strong controls, reliable engineering, and honest communication.

## Next Steps

The final phase should deploy the dashboard, add screenshots to the report, run leave-one-survey-out checks, calibrate event assumptions, and incorporate more disaggregated data.
