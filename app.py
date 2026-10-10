from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.analytics import (
    prepare_data, kpi_summary, partner_scorecard, monthly_trend,
    detect_underperformance, detect_monthly_anomalies, generate_recommendations,
)

st.set_page_config(page_title="Insurance Distribution Intelligence", page_icon="📊", layout="wide")
st.title("Insurance Distribution Intelligence")
st.caption("Partnership distribution performance, partner scorecards, and transparent action signals.")
st.info("Portfolio demo using synthetic data only. Figures are fictional and must not be interpreted as actual insurer performance.")

@st.cache_data
def load_data():
    return pd.read_csv(ROOT / "data" / "synthetic_distribution_performance.csv")

raw = load_data()
data = prepare_data(raw)
with st.sidebar:
    st.header("Filters")
    partners = ["All partners"] + sorted(data["partner"].unique().tolist())
    selected_partner = st.selectbox("Partner", partners)
    channels = ["All channels"] + sorted(data["channel"].unique().tolist())
    selected_channel = st.selectbox("Distribution channel", channels)
    min_month = data["month"].min().date()
    max_month = data["month"].max().date()
    date_range = st.date_input("Period", value=(min_month, max_month), min_value=min_month, max_value=max_month)
    threshold = st.slider("Underperformance threshold (%)", min_value=50, max_value=110, value=85, step=5) / 100
    st.caption("Threshold applies to cumulative premium attainment. Alerts are rules for investigation, not proof of cause.")

filtered = data.copy()
if selected_partner != "All partners":
    filtered = filtered[filtered["partner"] == selected_partner]
if selected_channel != "All channels":
    filtered = filtered[filtered["channel"] == selected_channel]
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[(filtered["month"].dt.date >= date_range[0]) & (filtered["month"].dt.date <= date_range[1])]
if filtered.empty:
    st.warning("No records match the selected filters. Widen the period or change filters.")
    st.stop()

k = kpi_summary(filtered)
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Premium written", f"Rp {k['premium_actual_idr']/1e9:,.2f}B")
c2.metric("Target attainment", f"{k['attainment_rate']:.1%}")
c3.metric("Leads", f"{k['leads']:,}")
c4.metric("Policy conversion", f"{k['conversion_rate']:.1%}")
c5.metric("Mean row persistency", f"{k['persistency_rate']:.1%}")

# Executive insights based on the active filters
st.subheader("Executive Insights")

insight_score = partner_scorecard(filtered)
premium_gap = (
    k["premium_actual_idr"] - k["premium_target_idr"]
)

underperforming = detect_underperformance(filtered, threshold)
below_target = underperforming["partner"].nunique()

if not insight_score.empty:
    top_partner = insight_score.iloc[0]
    top_partner_name = top_partner["partner"]
    top_partner_premium = top_partner["premium_actual_idr"]
else:
    top_partner_name = "No partner data"
    top_partner_premium = 0.0

i1, i2, i3 = st.columns(3)

i1.metric(
    "Premium gap vs target",
    f"Rp {premium_gap / 1e9:+,.2f}B",
)

i2.metric(
    "Partners below threshold",
    below_target,
)

i3.metric(
    "Top partner by premium",
    top_partner_name,
    help="Partner with the highest cumulative actual premium in the current selection.",
)

if premium_gap < 0:
    st.warning(
        "Premium is below target for the current selection. "
        "Review partner-level gaps and action signals."
    )
elif premium_gap > 0:
    st.success(
        "Premium is above target for the current selection."
    )
else:
    st.info("Premium is exactly on target.")

st.divider()
left,right = st.columns([1.5,1])
trend = monthly_trend(filtered)
with left:
    st.subheader("Premium vs target over time")
    long = trend.melt(id_vars="month", value_vars=["premium_actual_idr","premium_target_idr"], var_name="series", value_name="premium")
    long["series"] = long["series"].map({"premium_actual_idr":"Actual premium","premium_target_idr":"Target premium"})
    fig = px.line(long, x="month", y="premium", color="series", markers=True, labels={"month":"Month","premium":"Premium (IDR)","series":"Measure"})
    fig.update_layout(legend_title_text="", margin=dict(l=5,r=5,t=20,b=5))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Partner contribution")
    score = partner_scorecard(filtered)
    fig2 = px.bar(score.sort_values("premium_actual_idr"), x="premium_actual_idr", y="partner", color="channel", orientation="h", labels={"premium_actual_idr":"Premium (IDR)","partner":"Partner","channel":"Channel"})
    fig2.update_layout(legend_title_text="", margin=dict(l=5,r=5,t=20,b=5))
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Partner scorecard")
score = partner_scorecard(filtered)
score_display = score.copy()
score_display["Target attainment"] = score_display["attainment_rate"].map(lambda x:f"{x:.1%}")
score_display["Conversion"] = score_display["conversion_rate"].map(lambda x:f"{x:.1%}")
score_display["Persistency"] = score_display["persistency_rate"].map(lambda x:f"{x:.1%}")
score_display["Premium share"] = score_display["premium_share"].map(lambda x:f"{x:.1%}")
score_display["Actual premium (IDR)"] = score_display["premium_actual_idr"].map(lambda x:f"Rp {x:,.0f}")
score_display["Target premium (IDR)"] = score_display["premium_target_idr"].map(lambda x:f"Rp {x:,.0f}")
st.dataframe(score_display[["partner","channel","Actual premium (IDR)","Target premium (IDR)","Target attainment","leads","policies_issued","Conversion","Persistency","Premium share"]], use_container_width=True, hide_index=True)

st.subheader("Action signals")
st.caption("Rule-based alerts help prioritize investigation. They do not establish causality or replace partner discussions.")
recs = generate_recommendations(filtered, threshold)
if recs:
    recdf = pd.DataFrame(recs)
    st.dataframe(recdf, use_container_width=True, hide_index=True)
else:
    st.success("No rules triggered for this filter and threshold. Continue routine monitoring.")
under = detect_underperformance(filtered, threshold)
anoms = detect_monthly_anomalies(filtered)
with st.expander(f"Underlying alerts · {len(under)} underperforming scorecards · {len(anoms)} monthly anomaly flags"):
    if not under.empty:
        st.markdown("**Below target-attainment threshold**")
        st.dataframe(under[["partner","channel","attainment_rate","premium_actual_idr","premium_target_idr"]], hide_index=True, use_container_width=True)
    if not anoms.empty:
        st.markdown("**Large month-on-month premium drops**")
        show = anoms[["month", "partner", "premium_actual_idr", "partner_mom_change"]].copy()
        show["month"] = show["month"].dt.strftime("%Y-%m")
        show["partner_mom_change"] = show["partner_mom_change"].map(lambda x:f"{x:.1%}")
        st.dataframe(show, hide_index=True, use_container_width=True)

st.subheader("Download filtered data")
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered records (CSV)", data=csv, file_name="distribution_performance_filtered.csv", mime="text/csv")
st.download_button("Download partner scorecard (CSV)", data=score.to_csv(index=False).encode("utf-8"), file_name="partner_scorecard.csv", mime="text/csv")

with st.expander("Data dictionary and methodology"):
    st.markdown("""
    - **Premium attainment** = sum of actual premium / sum of target premium.
    - **Policy conversion** = total policies issued / total leads.
    - **Average persistency** = simple average of row-level persistency values; use weighted or cohort-based persistency for production reporting.
    - **Monthly anomaly** = partner's premium declines by at least 30% versus the previous month in the selected period.
    - **Synthetic data** = generated solely for this demo. No real insurer, customer, or partner performance is represented.
    """)
