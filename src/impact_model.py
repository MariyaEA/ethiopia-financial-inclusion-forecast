def association_matrix(x):
    return x.pivot_table(
        index="parent_id",
        columns="related_indicator",
        values="impact_magnitude",
        aggfunc="sum",
        fill_value=0,
    )


def validate_telebirr_effect(obs):
    s = obs[obs.indicator_code.eq("MOBILE_MONEY_ACCOUNT")].copy()
    s["year"] = s.observation_date.dt.year
    a = float(s.loc[s.year.eq(2021), "value_numeric"].iloc[0])
    b = float(s.loc[s.year.eq(2024), "value_numeric"].iloc[0])
    return {"pre_2021": a, "post_2024": b, "observed_change_pp": b - a}
