# Changelog

## [0.2.0] - 2026-07-27

### Added

- Typed `fi_forecast` package with dataclass configuration.
- Bounded logit trend forecasting and explicit scenario adjustments.
- Data-quality controls for schema, duplicates, range errors, and evidence completeness.
- Streamlit dashboard with executive, trends, forecasts, reliability, and model-card sections.
- Unit and integration tests with an 85% coverage threshold.
- GitHub Actions CI for Python 3.10 and 3.11.
- Dockerfile, Makefile, architecture, data contract, model card, and Week 12 documentation.
- Demo dataset for reproducible review.

### Changed

- Refocused project communication around finance-sector reliability, transparency, and decision risk.
- Replaced implicit assumptions with named configuration values and explicit scenario definitions.

### Safeguards

- Forecasts are constrained to valid percentage bounds.
- Registration, active-account, account-ownership, and transaction measures remain separate.
- Event relationships are labeled as associations rather than causal estimates.
