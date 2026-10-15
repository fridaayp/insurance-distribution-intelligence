import unittest
from pathlib import Path

import pandas as pd

from src.ml.forecasting import evaluate_forecast, forecast_next_month


DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "synthetic_distribution_performance.csv"
)


class TestForecasting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pd.read_csv(DATA_PATH, parse_dates=["month"])

    def test_forecast_is_after_latest_actual_month(self):
        forecasts = forecast_next_month(self.data)

        self.assertFalse(forecasts.empty)
        self.assertTrue(
            (forecasts["forecast_month"] > forecasts["last_actual_month"]).all()
        )

    def test_forecast_values_are_non_negative(self):
        forecasts = forecast_next_month(self.data)

        self.assertTrue((forecasts["forecast_premium_idr"] >= 0).all())

    def test_forecast_has_one_row_per_partner(self):
        forecasts = forecast_next_month(self.data)

        self.assertEqual(
            forecasts["partner"].nunique(),
            len(forecasts),
        )

    def test_evaluation_compares_ml_with_baseline(self):
        result = evaluate_forecast(self.data)

        self.assertGreater(result["evaluation_months"], 0)
        self.assertGreaterEqual(result["ml_mae"], 0)
        self.assertGreaterEqual(result["baseline_mae"], 0)
        self.assertFalse(result["predictions"].empty)


if __name__ == "__main__":
    unittest.main()
