# Week 12 Improvement Plan

## Goal

Transform the Week 11 financial-inclusion project into a production-grade portfolio piece that demonstrates reliability, maintainability, transparency, and business impact to finance-sector employers.

## Priorities

### Priority 1: Modular Engineering Foundation — 5 hours

**Work**

- Create a typed Python package under `src/fi_forecast/`.
- Use dataclasses for forecast and scenario configuration.
- Replace magic numbers with named constants.
- Extract reusable data, metric, forecasting, and quality functions.

**Outcome**

The project becomes easier to review, test, extend, and deploy.

### Priority 2: Testing and Automated Quality — 4 hours

**Work**

- Add unit and integration tests for core business rules.
- Add an 85% coverage threshold.
- Add Ruff linting.
- Configure GitHub Actions for pushes and pull requests.

**Outcome**

The repository provides visible, repeatable evidence of correctness.

### Priority 3: Finance-Oriented Reliability Controls — 3 hours

**Work**

- Detect missing columns, invalid record types, out-of-range percentages, duplicate IDs, and missing source evidence.
- Display findings in the dashboard.
- Document how failed checks should block publication.

**Outcome**

Stakeholders can see when the system is safe to use and when the data needs review.

### Priority 4: Decision-Ready Dashboard — 5 hours

**Work**

- Add executive metrics and target gaps.
- Add indicator exploration and downloadable data.
- Add scenario forecasts and uncertainty display.
- Add reliability controls and model-card content.

**Outcome**

Non-technical reviewers can understand the problem, result, assumptions, and risk in one application.

### Priority 5: Professional Documentation and Reproducibility — 4 hours

**Work**

- Rewrite the README around business value and quick review.
- Add architecture, data contract, model card, and technical report.
- Add Docker and Makefile workflows.

**Outcome**

The repository becomes a complete portfolio artifact rather than a collection of notebooks.

## Definition of Done

- `ruff check` passes.
- `pytest` passes with at least 85% coverage.
- GitHub Actions is green.
- Dashboard starts with the full dataset or included demo fallback.
- Forecasts remain within 0-100%.
- Scenario assumptions are explicit.
- Model limitations are visible.
- Repository contains clear evidence of Week 12 contributions.
