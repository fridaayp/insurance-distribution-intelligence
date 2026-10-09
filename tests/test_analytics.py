import sys
from pathlib import Path
import unittest
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.analytics import (
    prepare_data, kpi_summary, partner_scorecard, monthly_trend,
    detect_underperformance, detect_monthly_anomalies, generate_recommendations,
)

class AnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame([
            {"month":"2026-01-01","partner":"A","channel":"Bank","premium_target_idr":100,"premium_actual_idr":80,"leads":10,"policies_issued":2,"persistency_rate":0.8},
            {"month":"2026-02-01","partner":"A","channel":"Bank","premium_target_idr":100,"premium_actual_idr":40,"leads":20,"policies_issued":3,"persistency_rate":0.7},
            {"month":"2026-01-01","partner":"B","channel":"Digital","premium_target_idr":100,"premium_actual_idr":120,"leads":10,"policies_issued":4,"persistency_rate":0.9},
            {"month":"2026-02-01","partner":"B","channel":"Digital","premium_target_idr":100,"premium_actual_idr":130,"leads":10,"policies_issued":5,"persistency_rate":0.9},
        ])

    def test_kpi_summary(self):
        k = kpi_summary(self.df)
        self.assertEqual(k["premium_actual_idr"], 370)
        self.assertEqual(k["premium_target_idr"], 400)
        self.assertAlmostEqual(k["attainment_rate"], 0.925)
        self.assertEqual(k["leads"], 50)
        self.assertEqual(k["policies_issued"], 14)
        self.assertAlmostEqual(k["conversion_rate"], 14/50)

    def test_scorecard_orders_highest_premium_first(self):
        s = partner_scorecard(self.df)
        self.assertEqual(s.iloc[0]["partner"], "B")
        self.assertAlmostEqual(float(s[s.partner=="A"].iloc[0]["attainment_rate"]), 0.6)

    def test_monthly_trend(self):
        t = monthly_trend(self.df)
        self.assertEqual(len(t), 2)
        self.assertAlmostEqual(float(t.iloc[0]["premium_actual_idr"]), 200)
        self.assertAlmostEqual(float(t.iloc[1]["premium_actual_idr"]), 170)

    def test_underperformance_flag(self):
        u = detect_underperformance(self.df, 0.7)
        self.assertEqual(u["partner"].tolist(), ["A"])

    def test_anomaly_detects_drop(self):
        a = detect_monthly_anomalies(self.df, -0.3)
        self.assertIn("A", a["partner"].tolist())

    def test_recommendations_have_basis(self):
        r = generate_recommendations(self.df, 0.7)
        self.assertTrue(any(x["partner"]=="A" for x in r))
        self.assertTrue(all("basis" in x for x in r))

    def test_rejects_missing_columns(self):
        with self.assertRaises(ValueError):
            prepare_data(pd.DataFrame({"partner":["A"]}))

    def test_rejects_invalid_persistency(self):
        bad=self.df.copy()
        bad.loc[0,"persistency_rate"]=1.5
        with self.assertRaises(ValueError):
            prepare_data(bad)

if __name__ == "__main__":
    unittest.main()
