import numpy as np
import pandas as pd

MULT = {"Pessimistic": 0.65, "Base": 1.0, "Optimistic": 1.35}


def build_forecast(obs, links, code, years=(2025, 2026, 2027), scenario="Base"):
    h = obs[obs.indicator_code.eq(code)].copy()
    h["year"] = h.observation_date.dt.year
    h = h.sort_values("year")
    slope, inter = np.polyfit(h.year, h.value_numeric, 1)
    fit = inter + slope * h.year
    sd = max(float(np.std(h.value_numeric - fit, ddof=1)) if len(h) > 2 else 1.5, 1.0)
    total = (
        pd.to_numeric(
            links.loc[links.related_indicator.eq(code), "impact_magnitude"], errors="coerce"
        )
        .fillna(0)
        .sum()
    )
    out = []
    for i, y in enumerate(years, 1):
        trend = inter + slope * y
        effect = float(total) * MULT.get(scenario, 1) * i / len(years)
        f = float(np.clip(trend + effect, 0, 100))
        w = 1.96 * sd * np.sqrt(1 + i / len(h))
        out.append(
            {
                "year": y,
                "indicator_code": code,
                "scenario": scenario,
                "trend_component": trend,
                "event_effect": effect,
                "forecast": f,
                "lower": max(0, f - w),
                "upper": min(100, f + w),
            }
        )
    return pd.DataFrame(out)


def all_scenarios(obs, links):
    return pd.concat(
        [
            build_forecast(obs, links, c, scenario=s)
            for s in MULT
            for c in ["ACC_OWNERSHIP", "DIGITAL_PAYMENT"]
        ],
        ignore_index=True,
    )
