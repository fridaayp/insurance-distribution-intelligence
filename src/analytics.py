"""Pure analytics for Insurance Distribution Intelligence.

All ratios are decimals (e.g. 0.95 means 95%).
The bundled data is synthetic and is not representative of any real insurer.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = {
    "month", "partner", "channel", "premium_target_idr",
    "premium_actual_idr", "leads", "policies_issued", "persistency_rate",
}
NUMERIC_COLUMNS = [
    "premium_target_idr", "premium_actual_idr", "leads", "policies_issued",
    "persistency_rate",
]
NON_NEGATIVE_COLUMNS = [
    "premium_target_idr", "premium_actual_idr", "leads", "policies_issued",
]


def validate_data(df: pd.DataFrame) -> None:
    """Validate required fields and basic data integrity before analysis."""
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    if df.empty:
        raise ValueError("Dataset is empty")

    for col in ("partner", "channel"):
        if df[col].isna().any() or df[col].astype(str).str.strip().eq("").any():
            raise ValueError(f"Column {col} cannot contain blank values")

    parsed_month = pd.to_datetime(df["month"], errors="coerce")
    if parsed_month.isna().any():
        raise ValueError("Column month must contain valid dates")

    for col in NUMERIC_COLUMNS:
        values = pd.to_numeric(df[col], errors="coerce")
        if values.isna().any():
            raise ValueError(f"Column {col} must contain numeric values")
        if not np.isfinite(values.astype(float)).all():
            raise ValueError(f"Column {col} must contain finite numeric values")

    for col in NON_NEGATIVE_COLUMNS:
        if (pd.to_numeric(df[col]) < 0).any():
            raise ValueError(f"Column {col} cannot contain negative values")

    persistency = pd.to_numeric(df["persistency_rate"])
    if ((persistency < 0) | (persistency > 1)).any():
        raise ValueError("persistency_rate must be between 0 and 1")


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    validate_data(df)
    out = df.copy()
    out["month"] = pd.to_datetime(out["month"], errors="raise")
    for col in NUMERIC_COLUMNS:
        out[col] = pd.to_numeric(out[col])
    out["attainment_rate"] = (
        out["premium_actual_idr"]
        / out["premium_target_idr"].replace(0, float("nan"))
    )
    out["conversion_rate"] = (
        out["policies_issued"] / out["leads"].replace(0, float("nan"))
    )
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
        # Unweighted row-level mean: interpret cautiously until cohort exposure
        # counts are available in the dataset.
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
    g["attainment_rate"] = (
        g["premium_actual_idr"]
        / g["premium_target_idr"].replace(0, float("nan"))
    )
    g["conversion_rate"] = (
        g["policies_issued"] / g["leads"].replace(0, float("nan"))
    )
    total_premium = g["premium_actual_idr"].sum()
    g["premium_share"] = (
        g["premium_actual_idr"] / total_premium if total_premium else 0.0
    )
    return g.sort_values("premium_actual_idr", ascending=False).reset_index(drop=True)


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    d = prepare_data(df)
    g = d.groupby("month", as_index=False).agg(
        premium_target_idr=("premium_target_idr", "sum"),
        premium_actual_idr=("premium_actual_idr", "sum"),
        leads=("leads", "sum"),
        policies_issued=("policies_issued", "sum"),
    )
    g["attainment_rate"] = (
        g["premium_actual_idr"]
        / g["premium_target_idr"].replace(0, float("nan"))
    )
    g["conversion_rate"] = (
        g["policies_issued"] / g["leads"].replace(0, float("nan"))
    )
    g["premium_mom_change"] = g["premium_actual_idr"].pct_change()
    return g


def detect_underperformance(df: pd.DataFrame, threshold: float = 0.85) -> pd.DataFrame:
    """Flag partner/channel scorecards below the configured attainment threshold."""
    if not 0 <= threshold <= 2:
        raise ValueError("threshold must be between 0 and 2")
    score = partner_scorecard(df)
    return score[score["attainment_rate"] < threshold].copy().sort_values(
        "attainment_rate"
    )


def detect_monthly_anomalies(
    df: pd.DataFrame, drop_threshold: float = -0.30
) -> pd.DataFrame:
    """Flag partner-month premium drops versus the immediately prior calendar month."""
    if not -1 <= drop_threshold <= 0:
        raise ValueError("drop_threshold must be between -1 and 0")

    d = prepare_data(df)
    partner_month = (
        d.groupby(["partner", "month"], as_index=False)
        .agg(premium_actual_idr=("premium_actual_idr", "sum"))
        .sort_values(["partner", "month"])
    )

    # Compare only consecutive calendar months, not merely consecutive observations.
    partner_month["previous_month"] = (
        partner_month.groupby("partner")["month"].shift(1)
    )
    partner_month["previous_premium"] = (
        partner_month.groupby("partner")["premium_actual_idr"].shift(1)
    )

    consecutive = (
        partner_month["month"].dt.to_period("M")
        - partner_month["previous_month"].dt.to_period("M")
    ).eq(1)

    partner_month["partner_mom_change"] = (
        partner_month["premium_actual_idr"] / partner_month["previous_premium"] - 1
    ).where(consecutive & partner_month["previous_premium"].gt(0))

    flagged = partner_month[
        partner_month["partner_mom_change"] <= drop_threshold
    ].copy()

    return flagged.sort_values("partner_mom_change").reset_index(drop=True)


def generate_recommendations(
    df: pd.DataFrame, attainment_threshold: float = 0.85
) -> list[dict]:
    """Generate transparent rule-based actions, not causal conclusions."""
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
                "suggested_action": (
                    "Review funnel by product and branch; agree a 30-day "
                    "recovery plan with the partner."
                ),
                "basis": (
                    "Rule: cumulative actual premium / target is below "
                    "the configured threshold."
                ),
            })
        if row["persistency_rate"] < 0.78:
            recs.append({
                "priority": "Medium",
                "partner": row["partner"],
                "signal": f"Average persistency is {row['persistency_rate']:.0%}",
                "suggested_action": (
                    "Review early-lapse cohorts and onboarding/servicing "
                    "handoffs before increasing acquisition spend."
                ),
                "basis": (
                    "Rule: unweighted mean row-level persistency is below 78%; "
                    "investigate before inferring a cause."
                ),
            })

    anomalies = detect_monthly_anomalies(d)
    for _, row in anomalies.iterrows():
        recs.append({
            "priority": "High",
            "partner": row["partner"],
            "signal": (
                f"Total partner premium changed {row['partner_mom_change']:.0%} "
                f"vs previous month ({row['month']:%b %Y})"
            ),
            "suggested_action": (
                "Validate source data and investigate campaign, product, "
                "staffing, and operational changes."
            ),
            "basis": (
                "Rule: aggregated partner-month premium declined by at least "
                "30%; this is an alert, not a causal explanation."
            ),
        })
    order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(recs, key=lambda r: (order[r["priority"]], r["partner"], r["signal"]))
