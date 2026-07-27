# B9W12 Interim Submission

**Challenge:** Improve your previous week's projects  
**Selected project:** Forecasting Financial Inclusion in Ethiopia  
**Repository:** `ethiopia-financial-inclusion-forecast`  
**Author:** Mariamawit Alemu  
**Week:** 22-28 July 2026

## 1. Selected Project and Justification

I selected **Forecasting Financial Inclusion in Ethiopia** because it is the strongest match for the Week 12 finance-sector objective. The project addresses a real national decision problem, combines data engineering, analysis, forecasting, and dashboard development, and requires the reliability and transparency that finance stakeholders expect.

The project is also a strong capstone because its central challenge is not only predictive accuracy. It must prevent misleading comparisons between unique adults, registered accounts, active accounts, and transactions; communicate uncertainty honestly; and make each forecast traceable to observed evidence or an explicit assumption.

## 2. Business Problem Summary

Selam Analytics is developing a decision-support system for development finance institutions, mobile money operators, and the National Bank of Ethiopia. Stakeholders need to understand what drives financial inclusion, how policies and product launches may influence outcomes, and how Ethiopia's Access and Usage indicators may evolve from 2025 to 2027.

The main risk is that rapid growth in registrations, connectivity, and transaction volumes can be mistaken for broad inclusion. Account ownership increased from 46% in 2021 to only 49% in 2024. The system must therefore distinguish scale from meaningful inclusion and present uncertainty without overstating causal impact.

## 3. What Was Accomplished in the Original Project

The Week 11 project completed:

- schema validation for observations, events, impact links, and targets;
- data enrichment with documented evidence and confidence ratings;
- exploratory analysis of Access, Usage, infrastructure, gender, activity, and event timing;
- event-indicator association modeling;
- bounded scenario forecasts for 2025-2027;
- an interactive Streamlit dashboard;
- a final report communicating findings, limitations, and recommendations.

The enriched dataset contained 65 records: 35 observations, 11 events, 16 impact links, and 3 targets.

## 4. Gap Analysis Summary

The original project demonstrated strong analytical coverage, but the Week 12 review identified portfolio-critical engineering gaps:

- core logic was not fully isolated into typed, reusable modules;
- tests did not yet cover the most important business and validation rules;
- automated quality checks on push were limited;
- the dashboard needed a clearer reliability and model-risk section;
- setup, data contracts, and deployment instructions needed to be more reproducible;
- assumptions and intended model use needed a formal model card.

The detailed checklist is available in [`docs/WEEK12_GAP_ANALYSIS.md`](docs/WEEK12_GAP_ANALYSIS.md).

## 5. Prioritized Improvements and Time Estimates

| Priority | Improvement | Estimated effort | Reason |
|---:|---|---:|---|
| 1 | Refactor core loading, metrics, forecasting, and quality logic into a typed package | 5 hours | Reduces maintenance risk and makes behavior testable |
| 2 | Add at least 10 unit/integration tests with an 85% coverage gate | 4 hours | Proves correctness of the most important rules |
| 3 | Configure GitHub Actions for linting and tests on pushes and pull requests | 2 hours | Prevents regressions and gives visible proof of reliability |
| 4 | Upgrade Streamlit with scenario controls, risk checks, model card, and downloads | 5 hours | Makes the project useful to finance stakeholders |
| 5 | Rewrite documentation and add Docker-based reproducibility | 4 hours | Makes the repository reviewable and runnable by employers |

## 6. Work Completed for This Interim

- Created a modular `fi_forecast` package with type hints and dataclass configuration.
- Added named constants instead of hidden magic numbers.
- Added schema validation and a finance-oriented data-quality report.
- Added bounded logit forecasting and explicit scenario adjustments.
- Added automated tests for validation, metrics, quality controls, and forecasts.
- Added GitHub Actions CI with linting, testing, and an 85% coverage requirement.
- Added a decision-focused Streamlit dashboard.
- Added Docker, Makefile, data contract, model card, architecture, and run instructions.
- Added a lightweight demo dataset so the repository can be reviewed without private or large files.

## 7. Day-by-Day Plan

| Date | Planned work | Evidence in repository |
|---|---|---|
| Wed 22 Jul | Select project, review feedback, complete gap analysis | `WEEK12_INTERIM_SUBMISSION.md`, `docs/WEEK12_GAP_ANALYSIS.md` |
| Thu 23 Jul | Refactor data loading, configuration, metrics, and forecasting | `src/fi_forecast/` |
| Fri 24 Jul | Add tests and validation controls | `tests/`, `src/fi_forecast/quality.py` |
| Sat 25 Jul | Configure CI/CD and coverage gate | `.github/workflows/ci.yml`, `pyproject.toml` |
| Sun 26 Jul | Upgrade dashboard and prepare progress evidence | `dashboard/app.py`, `docs/` |
| Mon 27 Jul | Improve documentation, Docker, and technical report | `README.md`, `Dockerfile`, `reports/` |
| Tue 28 Jul | Final quality check, screenshots, deployment, and submission | GitHub Actions, dashboard screenshots, final links |

## 8. Success Metrics

The Week 12 improvement is considered successful when:

- all tests pass locally and in GitHub Actions;
- coverage is at least 85%;
- the dashboard runs from a clean environment;
- forecast outputs remain between 0% and 100%;
- invalid schemas and out-of-range percentages are detected;
- the README enables a reviewer to run the project in under 10 minutes;
- business assumptions, limitations, and non-causal interpretation are visible.

## 9. Interim Submission Statement

This repository demonstrates original improvement work beyond the Week 11 analysis. It contains a structured gap analysis, prioritized plan, refactored implementation, automated quality controls, tests, CI/CD, an interactive dashboard, and professional documentation. The work is organized on the `week12-improvements` branch and is ready for review through a pull request into `main`.
