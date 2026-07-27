# Model Card: Bounded Financial Inclusion Scenario Forecaster

## Model Summary

The baseline model forecasts percentage outcomes with a linear trend in log-odds space. Predictions are transformed back to percentage space, which ensures outputs remain between 0% and 100%.

## Intended Use

- Explore plausible Access scenarios for 2025-2027.
- Compare pessimistic, base, and optimistic assumptions.
- Support stakeholder discussion and planning.
- Communicate the consequence of recent slowdown and target gaps.

## Not Intended For

- Causal estimation of policy or product effects.
- Automated allocation of funding without expert review.
- Individual-level credit or eligibility decisions.
- Precise long-horizon forecasting.

## Training Data

The Access baseline uses five official account-ownership observations for 2011, 2014, 2017, 2021, and 2024. The full repository contains additional observations, events, links, and targets for contextual analysis.

## Method

1. Convert percentage values to proportions.
2. Clip extreme values to safe numerical bounds.
3. Apply the logit transform.
4. Fit a linear trend against year.
5. Predict log-odds for 2025-2027.
6. Transform back to percentage space.
7. Apply explicit scenario adjustments in percentage points.

## Evaluation

The project tests:

- valid output bounds;
- scenario ordering;
- deterministic forecasts;
- data-schema validity;
- business-metric correctness.

A future release should add leave-one-survey-out validation and compare the trend with alternative bounded baselines.

## Main Limitations

- Only five official Access observations are available.
- Survey points are irregularly spaced.
- Usage history is much sparser than Access history.
- Events overlap with policy and macroeconomic changes.
- Provider registrations may include inactive or duplicate accounts.
- National averages can hide gender, regional, income, and urban-rural gaps.

## Risk Controls

- Bound predictions to 0-100%.
- Display scenarios rather than a single definitive number.
- Keep assumptions visible.
- Preserve different indicator definitions.
- Label event relationships as associations.
- Require human review before policy or investment use.

## Ethical Considerations

The model should not be used to claim that progress is equitable without disaggregated evidence. Growth in national averages may still leave women, rural populations, low-income adults, or other groups behind.
