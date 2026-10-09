# Insurance Distribution Intelligence

An interactive portfolio project for business development, strategic partnerships, distribution strategy, and commercial analytics.

[🚀 Launch Live Dashboard](https://fridaayp-insurance-distribution-intelligence-app-f2ueqo.streamlit.app/)

[💻 View Source Code](https://github.com/fridaayp/insurance-distribution-intelligence)

Insurance Distribution Intelligence is a Streamlit dashboard designed to explore how a distribution leader might monitor partner performance, compare premium production against targets, identify signals that merit investigation, and prioritize follow-up actions.

«Data disclaimer: The bundled dataset is entirely synthetic. Partner names, metrics, and results are fictional and must not be interpreted as actual performance from any insurer or business.»

## Business Questions

- Are distribution partners meeting premium targets?
- Which partners and channels contribute most to written premium?
- How are premium production and target attainment changing over time?
- What signals may warrant a partner performance review?
- Which follow-up actions should be considered based on transparent, configurable rules?

## Key Capabilities

- Executive KPI overview: Written premium, target attainment, leads, policy conversion, and average persistency.
- Performance monitoring: Monthly actual-versus-target trends and partner contribution analysis.
- Partner scorecards: Compare partner performance using consistent metrics.
- Rule-based alerts: Flag cumulative underperformance and sharp month-over-month premium declines for investigation.
- Decision-support recommendations: Display rule-based next steps and their rationale.
- Interactive filters: Explore results by partner, distribution channel, reporting period, and underperformance threshold.
- Exportable analysis: Download filtered data and analysis outputs as CSV.
- Quality controls: Input-data validation, unit tests, and a GitHub Actions workflow that runs tests on pushes and pull requests.

## Dataset

File: "data/synthetic_distribution_performance.csv"

The dataset contains monthly observations for 12 fictional partners across 21 months, from January 2025 to September 2026. Fields include reporting month, partner, channel, target premium, actual premium, leads, policies issued, and persistency rate.

## Metric Definitions

- Premium target attainment: Total actual premium divided by total target premium.
- Policy conversion: Total policies issued divided by total leads.
- Average persistency: Unweighted mean of row-level persistency rates in the selected sample.
- Underperformance alert: Flags a partner when cumulative premium attainment falls below the selected threshold.
- Monthly anomaly alert: Flags a premium decline of at least 30% compared with the partner's previous observed month.

Alerts are investigation prompts, not proof of cause. In a production environment, KPI definitions should be agreed with Distribution, Finance, and Actuarial stakeholders. Data lineage and quality checks should be strengthened, and persistency may need cohort- or exposure-weighted treatment depending on the business definition.

## Technology Stack

- Python
- pandas
- Streamlit
- Plotly
- unittest
- GitHub Actions

## Run Locally

Requires Python 3.10 or newer and the packages listed in "requirements.txt".

1. Clone or download this repository.
2. Open a terminal in the project folder and create a virtual environment:

   python -m venv .venv
   
3. Activate the environment.

    ### Windows PowerShell
   
   .venv\Scripts\Activate.ps1
   
   ### macOS/Linux
   
   source .venv/bin/activate

5. Install dependencies and launch the app:
   
   pip install -r requirements.txt
   streamlit run app.py

6. Open the local URL displayed in the terminal.

## Run Tests

Install the project dependencies, then run:

python -m unittest discover -s tests -v

The test suite covers core analytics behavior, data preparation, and alert logic. GitHub Actions is configured to run tests automatically on pushes and pull requests.

## Project Structure

- app.py : Streamlit dashboard
- src/analytics.py : Analytics functions
- data/synthetic_distribution_performance.csv : Synthetic dataset
- tests/test_analytics.py : Unit tests
- .github/workflows/tests.yml : Automated testing
- requirements.txt : Dependencies
- README.md : Project documentation
- LICENSE : License

## Future Improvements

Potential extensions include CSV upload with schema validation, configurable KPI definitions, partner business review exports, and additional monitoring rules. Any connection to real business data should only be added with appropriate authorization and privacy safeguards.

## Portfolio Positioning

This project demonstrates a practical combination of distribution performance analysis, KPI design, partner scorecards, transparent business rules, data validation, testing, and dashboard delivery.

It is a synthetic-data decision-support prototype, not a production insurance system. No real-world revenue uplift, savings, or business impact is claimed.
