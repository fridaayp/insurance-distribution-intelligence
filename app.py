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

st.set_page_config(page_title="Distribution Strategy Intelligence", page_icon="📊", layout="wide")
st.markdown("""
<style>
:root {
  --navy: #10233f;
  --blue: #2563eb;
  --ink: #172b49;
  --muted: #687a93;
  --line: #e4ebf4;
}
.stApp {
  background: radial-gradient(ellipse at 10% 0%, #e8f1ff 0%, transparent 32%), #f3f6fb;
  color: var(--ink);
}
.block-container {
  max-width: 1560px;
  padding-top: 1.4rem;
  padding-bottom: 3rem;
}
[data-testid="stSidebar"] {
  background: linear-gradient(165deg, #0d1d34, #132d4d 58%, #1a426a);
  border-right: 1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] * { color: #f5f8fc; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  padding: 9px 11px;
  border: 1px solid transparent;
  border-radius: 10px;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(255,255,255,.09);
  border-color: rgba(255,255,255,.12);
}
h1 {
  color: #122844;
  font-size: 2.15rem;
  font-weight: 780;
  letter-spacing: -.045em;
}
h2 { color: #183452; font-weight: 720; }
h3 { color: #25405f; font-weight: 700; }
[data-testid="stMetric"] {
  background: linear-gradient(145deg, #fff, #fbfdff);
  border: 1px solid var(--line);
  padding: 18px 19px;
  border-radius: 16px;
  box-shadow: 0 5px 18px rgba(25,53,88,.045);
  min-height: 112px;
}
[data-testid="stMetricLabel"] {
  color: var(--muted);
  font-size: .83rem;
  font-weight: 650;
}
[data-testid="stMetricValue"] {
  color: #142b49;
  font-weight: 780;
  letter-spacing: -.035em;
}
[data-testid="stPlotlyChart"] {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 8px;
  box-shadow: 0 5px 18px rgba(25,53,88,.035);
}
[data-testid="stDataFrame"],
[data-testid="stTable"] {
  border: 1px solid var(--line);
  border-radius: 13px;
  overflow: hidden;
}
[data-testid="stTabs"] button[role="tab"] {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 9px 9px 0 0;
  padding: 10px 15px;
  font-weight: 650;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  background: #eaf1ff;
  color: #1d4ed8;
  border-color: #c9d9fb;
}
.stButton > button,
.stDownloadButton > button {
  border-radius: 10px;
  border: 1px solid #d7e2f0;
  font-weight: 650;
  padding: .55rem .9rem;
  transition: all .15s ease;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
  border-color: #8fb2f2;
  transform: translateY(-1px);
}
[data-testid="stAlert"] { border-radius: 12px; }
hr { border-color: #e0e8f2; }
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv(ROOT / "data" / "synthetic_distribution_performance.csv")

raw = load_data()
data = prepare_data(raw)

with st.sidebar:
    st.markdown("# ▥ Distribution")
    st.markdown("## Strategy Intelligence")
    st.caption("From data to decisions")
    page = st.radio("NAVIGATION", [
        "Executive Overview", "Performance Analysis", "Partnership Intelligence",
        "Scenario Lab", "Project Portfolio & Execution",
    ])
    st.divider()
    st.markdown("### Global filters")
    partner = st.selectbox("Partner", ["All partners"] + sorted(data.partner.dropna().unique().tolist()))
    channel = st.selectbox("Distribution channel", ["All channels"] + sorted(data.channel.dropna().unique().tolist()))
    min_date, max_date = data.month.min().date(), data.month.max().date()
    dates = st.date_input("Period", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    threshold = st.slider("Underperformance threshold (%)", 50, 110, 85, 5) / 100
    st.divider()
    st.caption("Independent portfolio prototype • synthetic data only")

df = data.copy()
if partner != "All partners":
    df = df[df.partner == partner]
if channel != "All channels":
    df = df[df.channel == channel]
if isinstance(dates, (tuple, list)) and len(dates) == 2:
    df = df[(df.month.dt.date >= dates[0]) & (df.month.dt.date <= dates[1])]
if df.empty:
    st.warning("No records match the selected filters. Widen the period or change filters.")
    st.stop()

k = kpi_summary(df)
score = partner_scorecard(df)
trend = monthly_trend(df)
under = detect_underperformance(df, threshold)
anomalies = detect_monthly_anomalies(df)
actions = generate_recommendations(df, threshold)
actual = float(k["premium_actual_idr"])
target = float(k["premium_target_idr"])
gap = actual - target
attainment = float(k["attainment_rate"])

def money(x):
    return f"Rp {x/1e9:,.2f}B"

def style(fig, height=330):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        margin=dict(l=14, r=18, t=44, b=16),
        font=dict(
            family="Arial, sans-serif",
            color="#526680",
            size=12,
        ),
        title_font=dict(size=15, color="#1b3554"),
        hoverlabel=dict(
            bgcolor="#10233f",
            font_color="#ffffff",
            bordercolor="#10233f",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(255,255,255,0)",
            font=dict(size=11),
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="#e5ebf3",
        tickfont=dict(color="#71829a", size=10),
    )
    fig.update_yaxes(
        gridcolor="#edf2f8",
        zerolinecolor="#edf2f8",
        tickfont=dict(color="#71829a", size=10),
    )
    return fig

def header(title, subtitle):
    st.title(title)
    st.caption(subtitle)
    st.info("Portfolio demo using synthetic data only. Figures are fictional and do not represent actual insurer performance.")

def score_display(frame):
    out = frame.copy()
    for col, label in [("attainment_rate","Target attainment"),("conversion_rate","Conversion"),
                       ("persistency_rate","Persistency"),("premium_share","Premium share")]:
        if col in out.columns:
            out[label] = out[col].map(lambda v: f"{v:.1%}")
    return out

if page == "Executive Overview":
    header(
        "Executive Overview",
        "A unified view of distribution performance, partnership growth, and execution signals."
    )

    st.caption("PORTFOLIO SNAPSHOT · CURRENT FILTER SELECTION")

    a, b, c, d = st.columns(4, gap="medium")

    a.metric(
        "TOTAL PREMIUM",
        money(actual),
        help="Total actual premium for the selected period and filters."
    )
    b.metric(
        "ACTIVE PARTNERS",
        f"{df.partner.nunique():,}",
        help="Unique partners represented in the filtered data."
    )
    c.metric(
        "POLICIES ISSUED",
        f"{int(df.policies_issued.sum()):,}",
        help="Total policies issued in the current selection."
    )
    d.metric(
        "TARGET ATTAINMENT",
        f"{attainment:.1%}",
        help="Total actual premium divided by total target premium."
    )

    st.divider()
    left,right = st.columns([1.45,1])
    with left:
        st.subheader("Premium vs target over time")
        t = trend.melt(id_vars="month", value_vars=["premium_actual_idr","premium_target_idr"],
                       var_name="series", value_name="premium")
        t["series"] = t.series.map({"premium_actual_idr":"Actual premium","premium_target_idr":"Target premium"})
        fig = px.line(t, x="month", y="premium", color="series", markers=True,
                      color_discrete_map={"Actual premium":"#2563eb","Target premium":"#9abce9"})
        st.plotly_chart(style(fig), use_container_width=True)
    with right:
        st.subheader("Partner contribution")
        ch = df.groupby("partner", as_index=False).premium_actual_idr.sum().sort_values("premium_actual_idr").tail(10)
        fig = px.bar(ch, x="premium_actual_idr", y="partner", orientation="h",
                     labels={"premium_actual_idr":"Premium (IDR)","partner":"Partner"})
        st.plotly_chart(style(fig), use_container_width=True)
    a,b,c = st.columns(3)
    a.metric("Premium gap vs target", money(gap))
    a.caption("Actual premium minus target premium")
    b.metric("Partners below threshold", int(under.partner.nunique()) if not under.empty else 0)
    c.metric("Monthly anomaly alerts", len(anomalies))
    left, right = st.columns([1, 1], gap="medium")

    with left:
        st.subheader("Key Insights")
        st.caption("What the current selection tells us")

        if target > 0:
            if attainment < 1:
                st.warning(
                    f"Premium is {money(abs(gap))} below target. "
                    f"Attainment stands at {attainment:.1%}."
                )
            else:
                st.success(
                    f"Premium is {money(gap)} above target. "
                    f"Attainment stands at {attainment:.1%}."
                )

        st.markdown(
            f"""
            <div style="background:#ffffff;border:1px solid #e4ebf4;
            border-radius:14px;padding:16px;margin:10px 0;">
                <div style="font-size:12px;color:#687a93;font-weight:700;">
                    PARTNER COVERAGE
                </div>
                <div style="font-size:25px;color:#172b49;font-weight:750;">
                    {df.partner.nunique():,}
                </div>
                <div style="font-size:13px;color:#687a93;">
                    unique partners in the current selection
                </div>
            </div>
            <div style="background:#ffffff;border:1px solid #e4ebf4;
            border-radius:14px;padding:16px;margin:10px 0;">
                <div style="font-size:12px;color:#687a93;font-weight:700;">
                    MONTHLY ANOMALY ALERTS
                </div>
                <div style="font-size:25px;color:#172b49;font-weight:750;">
                    {len(anomalies):,}
                </div>
                <div style="font-size:13px;color:#687a93;">
                    rule-based alerts requiring investigation
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.subheader("Priority Actions")
        st.caption("Rule-based follow-up signals · not causal conclusions")

        if actions:
            action_df = pd.DataFrame(actions)
            st.dataframe(
                action_df,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.success(
                "No rule-based actions triggered for the current selection."
            )

        if not under.empty:
            st.warning(
                f"{under.partner.nunique()} partner(s) are below "
                "the selected attainment threshold. Review their scorecards."
            )

        if not anomalies.empty:
            st.info(
                f"{len(anomalies)} monthly premium-drop alert(s) detected. "
                "Validate the underlying records before taking action."
            )

elif page == "Performance Analysis":
    header("Performance Analysis", "Explore detailed performance metrics across partners, channels, and product outcomes.")
    tabs = st.tabs(["Premium", "New Business", "Productivity", "Persistency", "Channel Mix"])
    with tabs[0]:
        a,b,c = st.columns(3)
        a.metric("Actual premium", money(actual)); b.metric("Target premium", money(target)); c.metric("Gap to target", money(gap))
        t = trend.melt(id_vars="month", value_vars=["premium_actual_idr","premium_target_idr"], var_name="series", value_name="premium")
        t["series"] = t.series.map({"premium_actual_idr":"Actual","premium_target_idr":"Target"})
        st.plotly_chart(style(px.line(t,x="month",y="premium",color="series",markers=True)), use_container_width=True)
    with tabs[1]:
        leads = int(df.leads.sum()); policies = int(df.policies_issued.sum())
        a,b,c = st.columns(3); a.metric("Leads",f"{leads:,}"); b.metric("Policies issued",f"{policies:,}")
        c.metric("Policy conversion",f"{policies/leads:.1%}" if leads else "N/A")
        g = df.groupby("channel",as_index=False).agg(leads=("leads","sum"),policies=("policies_issued","sum"))
        st.plotly_chart(style(px.bar(g.melt(id_vars="channel",var_name="measure",value_name="count"),
                                         x="channel",y="count",color="measure",barmode="group")),use_container_width=True)
    with tabs[2]:
        g = df.groupby(["partner","channel"],as_index=False).agg(leads=("leads","sum"),policies=("policies_issued","sum"))
        g["policies_per_100_leads"] = g.policies / g.leads.where(g.leads.ne(0)) * 100
        st.plotly_chart(style(px.bar(g.sort_values("policies_per_100_leads").tail(15),x="policies_per_100_leads",y="partner",
                                     color="channel",orientation="h"),420),use_container_width=True)
        st.dataframe(g.sort_values("policies_per_100_leads",ascending=False),use_container_width=True,hide_index=True)
    with tabs[3]:
        g=df.groupby("channel",as_index=False).persistency_rate.mean()
        st.plotly_chart(style(px.bar(g,x="persistency_rate",y="channel",orientation="h"),300),use_container_width=True)
        st.caption("Simple mean of row-level persistency values; not cohort-based or weighted.")
    with tabs[4]:
        g=df.groupby("channel",as_index=False).premium_actual_idr.sum()
        g["share"]=g.premium_actual_idr/g.premium_actual_idr.sum()
        fig=px.bar(g.sort_values("share"),x="share",y="channel",orientation="h")
        fig.update_xaxes(tickformat=".0%")
        st.plotly_chart(style(fig,300),use_container_width=True)

elif page == "Partnership Intelligence":
    header(
        "Partnership Intelligence",
        "Evaluate partner performance, identify attention areas, and prioritize engagement."
    )

    below_count = int(under["partner"].nunique()) if not under.empty else 0
    top_partner = (
        score.sort_values("premium_actual_idr", ascending=False).iloc[0]
        if not score.empty else None
    )

    a, b, c, d = st.columns(4, gap="medium")
    a.metric("PARTNERS IN VIEW", f"{df['partner'].nunique():,}")
    b.metric("BELOW THRESHOLD", f"{below_count:,}")
    c.metric("ANOMALY ALERTS", f"{len(anomalies):,}")
    d.metric(
        "TOP PARTNER",
        str(top_partner["partner"]) if top_partner is not None else "N/A"
    )

    st.divider()

    left, right = st.columns([1.2, 1], gap="medium")

    with left:
        st.subheader("Partner performance matrix")
        st.caption(
            "Premium vs. target attainment. Bubble size represents leads; "
            "use hover to inspect individual partners."
        )

        fig = px.scatter(
            score,
            x="premium_actual_idr",
            y="attainment_rate",
            size="leads",
            color="channel",
            hover_name="partner",
            labels={
                "premium_actual_idr": "Actual premium (IDR)",
                "attainment_rate": "Target attainment",
                "leads": "Leads",
                "channel": "Channel",
            },
            color_discrete_sequence=[
                "#2563eb", "#39a8a0", "#f5ad42", "#8b9bb4"
            ],
        )
        fig.add_hline(
            y=1,
            line_dash="dash",
            line_color="#64748b",
            annotation_text="100% target"
        )
        fig.add_hline(
            y=threshold,
            line_dash="dot",
            line_color="#dc6b4e",
            annotation_text=f"{threshold:.0%} threshold"
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(style(fig, 410), use_container_width=True)

    with right:
        st.subheader("Top partners by premium")
        st.caption("Ranked by total actual premium in the selected filters.")

        top = score.nlargest(10, "premium_actual_idr").sort_values(
            "premium_actual_idr", ascending=True
        )
        fig = px.bar(
            top,
            x="premium_actual_idr",
            y="partner",
            color="channel",
            orientation="h",
            labels={
                "premium_actual_idr": "Actual premium (IDR)",
                "partner": "Partner",
                "channel": "Channel",
            },
            color_discrete_sequence=[
                "#2563eb", "#39a8a0", "#f5ad42", "#8b9bb4"
            ],
        )
        st.plotly_chart(style(fig, 410), use_container_width=True)

    st.divider()
    st.subheader("Partner scorecard")
    st.caption(
        "Use this table to compare premium, attainment, conversion, "
        "persistency, and contribution across partners."
    )

    display = score_display(score)
    preferred = [
        "partner", "channel", "premium_actual_idr", "premium_target_idr",
        "attainment_rate", "conversion_rate", "persistency_rate", "premium_share"
    ]
    columns = [col for col in preferred if col in display.columns]
    st.dataframe(
        display[columns],
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    st.subheader("Partners requiring review")
    st.caption(
        "Rule-based screening only. Validate the context with partner owners "
        "before making commercial decisions."
    )

    if not under.empty:
        st.dataframe(
            under,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success(
            "No partner scorecards are below the selected attainment threshold."
        )

elif page == "Scenario Lab":
    header("Scenario Lab", "Adjust assumptions to compare illustrative premium scenarios—not a forecast.")
    left,right=st.columns([1,1.5])
    with left:
        growth=st.slider("Annual premium growth (%)",0,30,5)/100
        new_partners=st.slider("New partner equivalents",0,100,20,5)
        uplift=st.slider("Productivity increase (%)",0,50,15)/100
        contribution=st.slider("New-partner contribution (%)",0,60,30)/100
        years=st.slider("Projection horizon (years)",1,5,4)
    base=actual
    partner_count=max(int(df.partner.nunique()),1)
    increment=base*uplift+(base/partner_count)*new_partners*contribution
    projection=pd.DataFrame({"Year":list(range(2026,2027+years)),
        "Base case":[base*(1+growth)**i for i in range(years+1)],
        "Scenario":[(base+increment)*(1+growth)**i for i in range(years+1)]})
    with right:
        st.subheader("Projected premium")
        st.plotly_chart(style(px.line(projection,x="Year",y=["Base case","Scenario"],markers=True),360),use_container_width=True)
    a,b,c=st.columns(3)
    a.metric("Base case at horizon",money(projection["Base case"].iloc[-1]))
    b.metric("Scenario at horizon",money(projection["Scenario"].iloc[-1]))
    c.metric("Incremental premium",money(projection["Scenario"].iloc[-1]-projection["Base case"].iloc[-1]))
    st.caption("Illustrative arithmetic only. This is not a business forecast or ROI guarantee.")

else:
    header("Project Portfolio & Execution", "Track strategic initiatives, progress, milestones, and execution risks.")
    st.caption("Illustrative sample projects only; no real internal project status is represented.")
    projects=pd.DataFrame([
        {"Project":"Partner expansion","Workstream":"Distribution growth","Status":"On track","Progress":75,"Risk":"Medium","Next milestone":"Partner shortlist"},
        {"Project":"Product launch readiness","Workstream":"Product implementation","Status":"At risk","Progress":48,"Risk":"High","Next milestone":"Readiness review"},
        {"Project":"Digital channel enablement","Workstream":"Digital distribution","Status":"On track","Progress":62,"Risk":"Medium","Next milestone":"Pilot validation"},
        {"Project":"Partner productivity","Workstream":"Performance improvement","Status":"Delayed","Progress":30,"Risk":"High","Next milestone":"Recovery plan"},
        {"Project":"Operational efficiency","Workstream":"Process improvement","Status":"Completed","Progress":100,"Risk":"Low","Next milestone":"Benefits review"},
    ])
    a,b,c,d=st.columns(4)
    a.metric("Total projects",len(projects)); b.metric("On track",int((projects.Status=="On track").sum()))
    c.metric("At risk / delayed",int(projects.Status.isin(["At risk","Delayed"]).sum()))
    d.metric("Completed",int((projects.Status=="Completed").sum()))
    left,right=st.columns([1.2,1])
    with left:
        st.subheader("Project tracker")
        edited=st.data_editor(projects,use_container_width=True,hide_index=True,num_rows="dynamic")
        st.download_button("Download project tracker CSV",edited.to_csv(index=False).encode("utf-8"),"project_tracker.csv","text/csv")
    with right:
        st.subheader("Project progress")
        st.plotly_chart(style(px.bar(projects.sort_values("Progress"),x="Progress",y="Project",color="Status",orientation="h",range_x=[0,100]),380),use_container_width=True)
    st.subheader("Decision log")
    note=st.text_area("Record a decision or next action",placeholder="Decision, owner, due date, evidence...")
    if note.strip():
        st.download_button("Download decision note",note.encode("utf-8"),"decision_log.txt","text/plain")

st.divider()
with st.expander("Data dictionary & methodology"):
    st.markdown("""
    - **Premium attainment** = total actual premium / total target premium.
    - **Policy conversion** = total policies issued / total leads.
    - **Productivity** = policies issued per partner; channel productivity uses policies per 100 leads.
    - **Persistency** = simple mean of row-level persistency values, not cohort-based or weighted.
    - **Monthly anomaly** = rule-based premium decline versus the immediately preceding calendar month.
    - **Synthetic data** = generated solely for this portfolio prototype; no actual insurer, customer, or partner performance is represented.
    """)
st.download_button("Download filtered data (CSV)",df.to_csv(index=False).encode("utf-8"),
                   "distribution_performance_filtered.csv","text/csv")
