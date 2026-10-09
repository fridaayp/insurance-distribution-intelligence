"""Pure analytics for Insurance Distribution Intelligence.

All ratios are returned as decimals (e.g. 0.95 means 95%).
The bundled data is synthetic and is not representative of any real insurer.
"""
from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = {
    "month", "partner", "channel", "premium_target_idr",
    "premium_actual_idr", "leads", "policies_issued", "persistency_rate"
}

def validate_data(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    if df.empty:
        raise ValueError("Dataset is empty")
    for col in ["premium_target_idr", "premium_actual_idr", "leads", "policies_issued"]:
        if (pd.to_numeric(df[col], errors="coerce").isna()).any():
            raise ValueError(f"Column {col} must contain numeric values")
        if (pd.to_numeric(df[col]) < 0).any():
            raise ValueError(f"Column {col} cannot contain negative values")

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    validate_data(df)
    out = df.copy()
    out["month"] = pd.to_datetime(out["month"], errors="raise")
    out["premium_target_idr"] = pd.to_numeric(out["premium_target_idr"])
    out["premium_actual_idr"] = pd.to_numeric(out["premium_actual_idr"])
    out["leads"] = pd.to_numeric(out["leads"])
    out["policies_issued"] = pd.to_numeric(out["policies_issued"])
    out["persistency_rate"] = pd.to_numeric(out["persistency_rate"])
    if ((out["persistency_rate"] < 0) | (out["persistency_rate"] > 1)).any():
        raise ValueError("persistency_rate must be between 0 and 1")
    out["attainment_rate"] = out["premium_actual_idr"] / out["premium_target_idr"].replace(0, float("nan"))
    out["conversion_rate"] = out["policies_issued"] / out["leads"].replace(0, float("nan"))
    return out

def kpi_summary(df: pd.DataFrame) -> dict:
    d = prepare_data(df)
    target = d["premium_target_idr"].sum()
    actual = d["premium_actual_idr"].sum()
    leads = d["leads"].sum()
    policies = d["policies_issued"].sum()
    return {
        "premium_actual_idr": float(actual),
        "premium_target_idr": float(target),
        "attainment_rate": float(actual / target) if target else 0.0,
        "leads": int(leads),
        "policies_issued": int(policies),
        "conversion_rate": float(policies / leads) if leads else 0.0,
        "persistency_rate": float(d["persistency_rate"].mean()),
        "partner_count": int(d["partner"].nunique()),
    }

def partner_scorecard(df: pd.DataFrame) -> pd.DataFrame:
    d = prepare_data(df)
    g = d.groupby(["partner", "channel"], as_index=False).agg(
        premium_target_idr=("premium_target_idr", "sum"),
        premium_actual_idr=("premium_actual_idr", "sum"),
        leads=("leads", "sum"),
        policies_issued=("policies_issued", "sum"),
        persistency_rate=("persistency_rate", "mean"),
    )
    g["attainment_rate"] = g["premium_actual_idr"] / g["premium_target_idr"].replace(0, float("nan"))
    g["conversion_rate"] = g["policies_issued"] / g["leads"].replace(0, float("nan"))
    g["premium_share"] = g["premium_actual_idr"] / g["premium_actual_idr"].sum()
    return g.sort_values("premium_actual_idr", ascending=False).reset_index(drop=True)

def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    d = prepare_data(df)
    g = d.groupby("month", as_index=False).agg(
        premium_target_idr=("premium_target_idr", "sum"),
        premium_actual_idr=("premium_actual_idr", "sum"),
        leads=("leads", "sum"),
        policies_issued=("policies_issued", "sum"),
    )
    g["attainment_rate"] = g["premium_actual_idr"] / g["premium_target_idr"].replace(0, float("nan"))
    g["conversion_rate"] = g["policies_issued"] / g["leads"].replace(0, float("nan"))
    g["premium_mom_change"] = g["premium_actual_idr"].pct_change()
    return g

def detect_underperformance(df: pd.DataFrame, threshold: float = 0.85) -> pd.DataFrame:
    """Flag partner scorecards below the selected premium-target attainment threshold."""
    if not 0 <= threshold <= 2:
        raise ValueError("threshold must be between 0 and 2")
    score = partner_scorecard(df)
    return score[score["attainment_rate"] < threshold].copy().sort_values("attainment_rate")

def detect_monthly_anomalies(df: pd.DataFrame, drop_threshold: float = -0.30) -> pd.DataFrame:
    """Flag a partner-month when actual premium falls beyond threshold vs its prior month."""
    if not -1 <= drop_threshold <= 0:
        raise ValueError("drop_threshold must be between -1 and 0")
    d = prepare_data(df).sort_values(["partner", "month"]).copy()
    d["partner_mom_change"] = d.groupby("partner")["premium_actual_idr"].pct_change()
    return d[d["partner_mom_change"] <= drop_threshold].copy().sort_values("partner_mom_change")

def generate_recommendations(df: pd.DataFrame, attainment_threshold: float = 0.85) -> list[dict]:
    """Generate transparent rule-based actions; these are prompts, not causal conclusions."""
    d = prepare_data(df)
    score = partner_scorecard(d)
    recs = []
    for _, row in score.iterrows():
        attainment = row["attainment_rate"]
        if pd.notna(attainment) and attainment < attainment_threshold:
            recs.append({
                "priority": "High",
                "partner": row["partner"],
                "signal": f"Premium attainment is {attainment:.0%}",
                "suggested_action": "Review funnel by product and branch; agree a 30-day recovery plan with the partner.",
                "basis": "Rule: cumulative actual premium / target is below the configured threshold.",
            })
        if row["persistency_rate"] < 0.78:
            recs.append({
                "priority": "Medium",
                "partner": row["partner"],
                "signal": f"Average persistency is {row['persistency_rate']:.0%}",
                "suggested_action": "Review early-lapse cohorts and onboarding/servicing handoffs before increasing acquisition spend.",
                "basis": "Rule: mean row-level persistency is below 78%; investigate before inferring a cause.",
            })
    anomalies = detect_monthly_anomalies(d)
    for _, row in anomalies.iterrows():
        recs.append({
            "priority": "High",
            "partner": row["partner"],
            "signal": f"Premium changed {row['partner_mom_change']:.0%} vs previous month ({row['month']:%b %Y})",
            "suggested_action": "Validate source data and investigate campaign, product, staffing, and operational changes.",
            "basis": "Rule: month-on-month premium decline is 30% or more; this is an alert, not a causal explanation.",
        })
    order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(recs, key=lambda r: (order[r["priority"]], r["partner"], r["signal"]))
