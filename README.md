# Insurance Distribution Intelligence

**A portfolio project for senior business development, partnership, strategy, and distribution roles.**

An executable analytics dashboard that explores partner-level distribution performance, target attainment, lead-to-policy conversion, persistency, and rule-based action signals.

> **Important:** all bundled data is synthetic and generated for demonstration. It does not represent a real insurer, customers, partners, or actual business results.

## What it demonstrates
- Business KPI design for partner distribution
- Monthly trend and target-vs-actual analysis
- Partner scorecards and contribution analysis
- Transparent rule-based underperformance and anomaly alerts
- Action recommendations with explicit rules/basis
- Data validation, tests, CSV exports, and CI test workflow

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser. Use the sidebar to filter partner, channel, and period.

## Run tests

```bash
pip install pandas
python -m unittest discover -s tests -v
```

## Dataset
`data/synthetic_distribution_performance.csv` contains monthly observations for 12 fictional partners across 21 months (January 2025–September 2026). Fields include month, partner, channel, target premium, actual premium, leads, policies issued, and persistency rate.

## Metric definitions
- **Premium attainment:** sum(actual premium) / sum(target premium)
- **Conversion:** total policies issued / total leads
- **Average persistency:** unweighted mean of row-level persistency rates in the filtered sample
- **Underperformance alert:** cumulative partner attainment below the configurable threshold
- **Monthly anomaly alert:** partner premium drops by at least 30% vs its previous observed month

Alerts are investigation prompts, not causal conclusions. For a production system, validate definitions with Finance/Actuarial/Distribution stakeholders, add data lineage, and use cohort-weighted persistency where appropriate.

## Project structure
```text
app.py
src/analytics.py
data/synthetic_distribution_performance.csv
tests/test_analytics.py
.github/workflows/tests.yml
requirements.txt
```

## Roadmap
1. Add CSV upload with schema validation.
2. Add partner-level monthly targets and configurable KPI definitions.
3. Add exportable partner business review pack.
4. Add a documented deployment (e.g. Streamlit Community Cloud).
5. Add privacy-safe real-data adapter only when authorized data access is available.

## Portfolio framing
Describe this as a **synthetic-data prototype** demonstrating analytics design and decision support. Do not claim simulated uplift, savings, or revenue as real-world impact.
