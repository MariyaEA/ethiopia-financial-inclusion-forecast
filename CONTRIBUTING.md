# Contributing

## Development Workflow

1. Create a focused branch from `main`.
2. Install development dependencies with `pip install -r requirements-dev.txt`.
3. Add or update tests for every behavior change.
4. Run `make quality` before committing.
5. Open a pull request with a clear description, evidence, and limitations.

## Commit Style

Use short, descriptive commits:

- `docs: add week 12 gap analysis and plan`
- `refactor: modularize forecasting and validation logic`
- `test: add coverage for forecast bounds and schema rules`
- `ci: add automated lint and pytest workflow`
- `feat: add reliability controls to dashboard`

## Data Rules

- Do not commit credentials, secrets, or private datasets.
- Preserve source names, evidence notes, and confidence fields.
- Keep events pillar-neutral; represent effects through `impact_link` records.
- Do not combine supply-side registration totals with unique-adult survey outcomes.
- Do not describe event associations as causal effects without causal identification.
