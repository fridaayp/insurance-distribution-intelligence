"""Experimental premium forecasting for synthetic distribution data."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

FEATURES = [
    "lag_1",
    "lag_2",
    "lag_3",
    "rolling_mean_3",
    "month_number",
]


def _make_features(group: pd.DataFrame) -> pd.DataFrame:
    group = group.sort_values("month").copy()
    group["month"] = pd.to_datetime(group["month"])
    group["premium"] = group["premium_actual_idr"].astype(float)

    group["lag_1"] = group["premium"].shift(1)
    group["lag_2"] = group["premium"].shift(2)
    group["lag_3"] = group["premium"].shift(3)
    group["rolling_mean_3"] = group["premium"].shift(1).rolling(3).mean()
    group["month_number"] = group["month"].dt.month

    return group


def _model() -> RandomForestRegressor:
    return RandomForestRegressor(
        n_estimators=200,
        max_depth=4,
        min_samples_leaf=2,
        random_state=42,
    )


def evaluate_forecast(data: pd.DataFrame) -> dict:
    """Evaluate using each partner's last three observed months."""
    rows = []

    for partner, raw_group in data.groupby("partner"):
        group = (
            raw_group.groupby("month", as_index=False)["premium_actual_idr"]
            .sum()
            .sort_values("month")
        )
        features = _make_features(group).dropna(subset=FEATURES)

        if len(features) < 8:
            continue

        train = features.iloc[:-3]
        test = features.iloc[-3:]

        model = _model()
        model.fit(train[FEATURES], train["premium"])

        predictions = model.predict(test[FEATURES])

        for (_, row), prediction in zip(test.iterrows(), predictions):
            rows.append({
                "partner": partner,
                "month": row["month"],
                "actual": row["premium"],
                "ml_prediction": max(0.0, float(prediction)),
                "baseline_prediction": float(row["lag_1"]),
            })

    results = pd.DataFrame(rows)

    if results.empty:
        raise ValueError(
            "Insufficient monthly history to evaluate the forecasting model."
        )

    return {
        "predictions": results,
        "ml_mae": float(
            mean_absolute_error(results["actual"], results["ml_prediction"])
        ),
        "baseline_mae": float(
            mean_absolute_error(results["actual"], results["baseline_prediction"])
        ),
        "evaluation_months": int(results["month"].nunique()),
    }


def forecast_next_month(data: pd.DataFrame) -> pd.DataFrame:
    """Train per partner and forecast one month beyond the latest observation."""
    forecasts = []

    for partner, raw_group in data.groupby("partner"):
        group = (
            raw_group.groupby("month", as_index=False)["premium_actual_idr"]
            .sum()
            .sort_values("month")
        )
        features = _make_features(group).dropna(subset=FEATURES)

        if len(features) < 5:
            continue

        model = _model()
        model.fit(features[FEATURES], features["premium"])

        latest = features.iloc[[-1]]
        prediction = max(
            0.0,
            float(model.predict(latest[FEATURES])[0]),
        )

        forecasts.append({
            "partner": partner,
            "last_actual_month": latest["month"].iloc[0],
            "forecast_month": (
                latest["month"].iloc[0] + pd.offsets.MonthBegin(1)
            ),
            "last_actual_premium_idr": float(latest["premium"].iloc[0]),
            "forecast_premium_idr": prediction,
        })

    return pd.DataFrame(forecasts)
