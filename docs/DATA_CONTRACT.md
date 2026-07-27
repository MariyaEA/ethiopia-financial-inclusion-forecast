# Data Contract

## Purpose

The data contract prevents silent schema drift and preserves the distinction between observed outcomes, events, modeled links, and targets.

## Minimum Required Columns

| Column | Type | Rule |
|---|---|---|
| `record_type` | string | One of `observation`, `event`, `impact_link`, `target` |
| `pillar` | string/null | Required for observations and targets; blank for events |
| `indicator` | string/null | Human-readable indicator name |
| `indicator_code` | string/null | Stable machine-readable code for observations/targets |
| `value_numeric` | numeric/null | Required for measured observations used in analysis |
| `observation_date` | date/null | Required for measured observations used in time series |

## Recommended Evidence Columns

- `record_id`
- `source_name`
- `source_url`
- `confidence`
- `category`
- `parent_id`
- `related_indicator`
- `impact_direction`
- `impact_magnitude`
- `lag_months`
- `evidence_basis`
- `original_text`
- `collected_by`
- `collection_date`
- `notes`

## Record Rules

### Observation

- `pillar`, `indicator_code`, `value_numeric`, and `observation_date` are required.
- Percentage indicators must stay between 0 and 100.
- Source evidence and confidence should be recorded.

### Event

- `category` is required.
- `pillar` should remain blank because one event can influence multiple dimensions.

### Impact Link

- `parent_id` must reference an event.
- The affected pillar and indicator belong on the link.
- Direction, magnitude, lag, evidence, and confidence should be explicit.

### Target

- `pillar`, `indicator_code`, target value, and target date should be provided.

## Publication Gate

A release should be blocked when:

- required columns are missing;
- percentage values are outside 0-100;
- duplicate record IDs are present;
- observation dates cannot be parsed;
- record types are invalid.

Missing source evidence should generate a warning and require reviewer sign-off.
