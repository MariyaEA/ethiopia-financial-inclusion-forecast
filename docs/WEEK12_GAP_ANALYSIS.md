# Week 12 Gap Analysis

## Project Reviewed

**Forecasting Financial Inclusion in Ethiopia**

## Checklist

| Category | Question | Original status | Week 12 action |
|---|---|---|---|
| Code Quality | Is the code modular and well organized? | Partial | Extracted loading, metrics, forecasting, and quality logic into `src/fi_forecast/` |
| Code Quality | Are there type hints on functions? | Partial | Added type hints to all public functions |
| Code Quality | Is there a clear project structure? | Yes | Strengthened structure with docs, scripts, package, tests, CI, and deployment files |
| Testing | Are there unit tests for core functions? | Partial | Added tests for schema, metrics, forecasts, and quality controls |
| Testing | Do tests run automatically on push? | Partial | Added GitHub Actions workflow for pushes and pull requests |
| Documentation | Is the README comprehensive? | Partial | Added business problem, architecture, results, quick start, technical details, safeguards, and future work |
| Documentation | Are there docstrings on functions? | Partial | Added docstrings to public modules and functions |
| Reproducibility | Can someone else run the project? | Partial | Added pinned dependencies, demo data, Dockerfile, Makefile, and environment-path support |
| Reproducibility | Are dependencies documented? | Yes | Split runtime and development dependencies and added `pyproject.toml` |
| Visualization | Is there an interactive way to explore results? | Yes | Upgraded dashboard with reliability and model-risk views |
| Business Impact | Is the problem clearly articulated? | Yes | Reframed around finance-sector decision risk and stakeholder actions |
| Business Impact | Are success metrics defined? | Partial | Added measurable engineering and usability success criteria |

## Critical Gaps Identified

### 1. Reliability evidence was not prominent enough

Finance-sector reviewers need proof that the system fails safely and detects invalid data. The original analytical work was strong, but tests and automated checks were not yet a central portfolio feature.

### 2. Forecast logic needed stronger isolation

Forecasting and business calculations should be reusable outside notebooks and dashboards. Keeping core logic in typed modules reduces duplication and supports reliable testing.

### 3. Sparse-data risk needed a formal control

Only five official Access observations are available over thirteen years. The improved project must prevent false precision, keep forecasts bounded, and show assumptions next to outputs.

### 4. Reproducibility needed to be reviewer-friendly

A recruiter should be able to clone, install, test, and run the dashboard quickly. The repository therefore needs pinned dependencies, a demo path, Docker, and exact commands.

### 5. Documentation needed a finance-sector story

The strongest story is: **financial problem → transparent solution → reliability controls → decision impact**. Technical details should support this narrative rather than dominate it.

## Deliberate Non-Selection: SHAP

SHAP is not added simply to satisfy a checklist. The primary Access baseline is a transparent low-parameter trend model, not a high-dimensional black-box feature model. Applying SHAP would not add meaningful explanation. The project instead uses explicit scenario adjustments, model cards, traceable assumptions, and data-quality reports. SHAP can be added later if a validated feature-based model is introduced.
