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
  background: linear-gradient(
    180deg,
    #0b1930 0%,
    #102744 55%,
    #0d2039 100%
  );
  border-right: 1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] > div:first-child {
  padding: 1.15rem .9rem 1rem;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
  color: #e8effa;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
  color: #b6c5dc;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > label {
  color: #91a5c2;
  font-size: .68rem;
  font-weight: 750;
  letter-spacing: .12em;
  text-transform: uppercase;
  margin: .8rem 0 .45rem;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > div {
  gap: .3rem;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-testid="stWidgetLabel"] {
  margin-bottom: .5rem;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label {
  display: flex;
  align-items: center;
  min-height: 43px;
  padding: .55rem .7rem;
  margin: 0;
  border: 1px solid transparent;
  border-radius: 10px;
  color: #c0cee1;
  font-size: .86rem;
  font-weight: 550;
  transition: background .18s ease, border-color .18s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:hover {
  background: rgba(255,255,255,.07);
  border-color: rgba(255,255,255,.08);
  color: #fff;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
  background: linear-gradient(100deg, #214c91, #193d75);
  border-color: rgba(143,180,255,.2);
  color: #fff;
  box-shadow: 0 4px 14px rgba(0,0,0,.15);
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p {
  color: #fff;
  font-weight: 700;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] > label,
[data-testid="stSidebar"] [data-testid="stDateInput"] > label,
[data-testid="stSidebar"] [data-testid="stSlider"] > label {
  color: #aebed5;
  font-size: .75rem;
  font-weight: 600;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  background: rgba(255,255,255,.07);
  border-color: rgba(255,255,255,.12);
  border-radius: 9px;
}

[data-testid="stSidebar"] [data-testid="stDateInput"] input {
  background: rgba(255,255,255,.07);
  border-color: rgba(255,255,255,.12);
  border-radius: 9px;
}

[data-testid="stSidebar"] hr {
  border-color: rgba(255,255,255,.12);
  margin: 1rem 0;
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
    st.markdown(
        """
        <div style="padding:8px 5px 15px;">
            <div style="
                display:flex;
                align-items:center;
                gap:10px;
                margin-bottom:17px;
            ">
                <div style="
                    width:43px;
                    height:43px;
                    border-radius:12px;
                    background:linear-gradient(145deg,#35c6b0,#4387f5);
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:white;
                    font-size:25px;
                    font-weight:800;
                    box-shadow:0 5px 18px rgba(38,139,210,.22);
                ">▥</div>
                <div>
                    <div style="
                        color:#f4f7fc;
                        font-size:16px;
                        font-weight:800;
                        letter-spacing:-.4px;
                        line-height:1.25;
                    ">Distribution</div>
                    <div style="
                        color:#f4f7fc;
                        font-size:16px;
                        font-weight:800;
                        letter-spacing:-.4px;
                        line-height:1.25;
                    ">Strategy Intelligence</div>
                </div>
            </div>
            <div style="
                color:#9eb2cf;
                font-size:11px;
                line-height:1.6;
                letter-spacing:.2px;
            ">From data to decisions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    pages = [
        "Executive Overview",
        "Performance Analysis",
        "Partnership Intelligence",
        "Scenario Lab",
        "Project Portfolio & Execution",
    ]

    page_labels = {
        "Executive Overview": "◈   Executive Overview",
        "Performance Analysis": "▤   Performance Analysis",
        "Partnership Intelligence": "♧   Partnership Intelligence",
        "Scenario Lab": "◉   Scenario Lab",
        "Project Portfolio & Execution": "▣   Project Portfolio & Execution",
    }

    page = st.radio(
        "Navigation",
        pages,
        format_func=lambda value: page_labels[value],
        label_visibility="visible",
    )

    st.divider()

    st.markdown(
        """
        <div style="
            color:#dce7f7;
            font-size:12px;
            font-weight:750;
            letter-spacing:.8px;
            margin:0 0 12px 2px;
        ">GLOBAL FILTERS</div>
        """,
        unsafe_allow_html=True,
    )

    partner = st.selectbox(
        "Partner",
        ["All partners"] + sorted(data.partner.dropna().unique().tolist()),
    )

    channel = st.selectbox(
        "Distribution channel",
        ["All channels"] + sorted(data.channel.dropna().unique().tolist()),
    )

    min_date, max_date = data.month.min().date(), data.month.max().date()

    dates = st.date_input(
        "Period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    threshold = st.slider(
        "Underperformance threshold (%)",
        50, 110, 85, 5,
    ) / 100

    st.divider()

    st.markdown(
        """
        <div style="
            display:flex;
            align-items:center;
            gap:11px;
            padding:7px 2px 4px;
        ">
            <div style="
                width:39px;
                height:39px;
                flex-shrink:0;
                border-radius:50%;
                background:#263f68;
                border:1px solid #46618a;
                color:#ffffff;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:13px;
                font-weight:800;
            ">FA</div>
            <div>
                <div style="
                    color:#f4f7fc;
                    font-size:13px;
                    font-weight:750;
                ">Frida A.</div>
                <div style="
                    color:#9eb2cf;
                    font-size:10px;
                    line-height:1.5;
                ">Business Strategy & Analytics</div>
            </div>
        </div>
        <div style="
            color:#7f94b2;
            font-size:10px;
            margin:13px 2px 0;
            line-height:1.5;
        ">Portfolio prototype · Synthetic data</div>
        """,
        unsafe_allow_html=True,
    )
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
    header(
        "Scenario Lab",
        "Model illustrative growth assumptions and compare their potential premium impact."
    )

    st.caption("SCENARIO PLANNING · ASSUMPTION-DRIVEN · NOT A FORECAST")

    # --- Assumption controls ---
    st.subheader("Scenario assumptions")
    st.caption(
        "Adjust the inputs to explore alternative growth paths. "
        "All results are illustrative and use the current filtered portfolio as the baseline."
    )

    base = float(actual)
    partner_count = max(int(df["partner"].nunique()), 1)

    controls = st.columns(4, gap="medium")

    with controls[0]:
        growth = st.slider(
            "Annual growth (%)",
            min_value=0, max_value=30, value=5, step=1,
            help="Annual growth applied to both scenarios."
        ) / 100

    with controls[1]:
        uplift = st.slider(
            "Productivity uplift (%)",
            min_value=0, max_value=50, value=15, step=5,
            help="Illustrative uplift applied to baseline premium."
        ) / 100

    with controls[2]:
        new_partners = st.slider(
            "New partner equivalents",
            min_value=0, max_value=100, value=20, step=5,
            help="Illustrative number of additional partner equivalents."
        )

    with controls[3]:
        contribution = st.slider(
            "New-partner contribution (%)",
            min_value=0, max_value=60, value=30, step=5,
            help="Assumed contribution relative to current average partner premium."
        ) / 100

    years = st.slider(
        "Projection horizon",
        min_value=1, max_value=5, value=4,
        format="%d years"
    )

    # --- Scenario calculations ---
    incremental_productivity = base * uplift
    incremental_partners = (base / partner_count) * new_partners * contribution
    scenario_increment = incremental_productivity + incremental_partners

    projection_years = list(range(0, years + 1))
    projection = pd.DataFrame({
        "Year": [f"Year {i}" for i in projection_years],
        "Base case": [
            base * ((1 + growth) ** i) for i in projection_years
        ],
        "Growth scenario": [
            (base + scenario_increment) * ((1 + growth) ** i)
            for i in projection_years
        ],
    })
    projection["Incremental premium"] = (
        projection["Growth scenario"] - projection["Base case"]
    )

    base_horizon = float(projection["Base case"].iloc[-1])
    scenario_horizon = float(projection["Growth scenario"].iloc[-1])
    incremental_horizon = scenario_horizon - base_horizon
    uplift_horizon = (
        incremental_horizon / base_horizon if base_horizon else 0
    )

    st.divider()

    # --- Executive scenario summary ---
    st.subheader("Scenario impact")
    k1, k2, k3, k4 = st.columns(4, gap="medium")

    k1.metric(
        "CURRENT BASELINE",
        money(base),
        help="Actual premium in the selected filters and period."
    )
    k2.metric(
        "BASE CASE AT HORIZON",
        money(base_horizon),
        help="Baseline premium compounded by the assumed annual growth rate."
    )
    k3.metric(
        "GROWTH SCENARIO",
        money(scenario_horizon),
        help="Illustrative scenario including the selected productivity and partner assumptions."
    )
    k4.metric(
        "INCREMENTAL PREMIUM",
        money(incremental_horizon),
        delta=f"{uplift_horizon:.1%} vs. base case",
        help="Difference between the scenario and base case at the selected horizon."
    )

    st.divider()

    # --- Visual comparison ---
    left, right = st.columns([1.45, 1], gap="medium")

    with left:
        st.subheader("Premium trajectory")
        st.caption(
            "Compare the base case with the scenario over the selected horizon."
        )

        fig = px.line(
            projection,
            x="Year",
            y=["Base case", "Growth scenario"],
            markers=True,
            color_discrete_map={
                "Base case": "#9abce9",
                "Growth scenario": "#2563eb",
            },
            labels={
                "value": "Projected premium (IDR)",
                "variable": "Scenario",
                "Year": "Projection horizon",
            },
        )
        fig.update_traces(line=dict(width=3))
        st.plotly_chart(
            style(fig, 390),
            use_container_width=True
        )

    with right:
        st.subheader("Incremental premium by year")
        st.caption(
            "Illustrative difference between the scenario and the base case."
        )

        incremental_chart = projection[["Year", "Incremental premium"]].copy()
        fig = px.bar(
            incremental_chart,
            x="Year",
            y="Incremental premium",
            labels={
                "Year": "Projection horizon",
                "Incremental premium": "Incremental premium (IDR)",
            },
            color_discrete_sequence=["#39a8a0"],
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(
            style(fig, 390),
            use_container_width=True
        )

    # --- Explain the scenario drivers ---
    st.divider()
    st.subheader("Contribution assumptions")

    driver1, driver2 = st.columns(2, gap="medium")

    with driver1:
        st.markdown("*Productivity contribution*")
        st.metric(
            "Illustrative premium uplift",
            money(incremental_productivity)
        )
        st.caption(
            f"Calculated as {uplift:.0%} of the current premium baseline."
        )

    with driver2:
        st.markdown("*New-partner contribution*")
        st.metric(
            "Illustrative premium contribution",
            money(incremental_partners)
        )
        st.caption(
            f"{new_partners} partner equivalents × "
            f"{contribution:.0%} of average current partner premium."
        )

    st.divider()
    st.subheader("Projection detail")
    st.caption(
        "Values are model outputs, not guaranteed business results."
    )

    detail = projection.copy()
    for col in ["Base case", "Growth scenario", "Incremental premium"]:
        detail[col] = detail[col].map(money)

    st.dataframe(
        detail,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Interpretation note: this model applies a simplified one-time "
        "incremental premium assumption and compounds both scenarios using "
        "the same annual growth rate. It does not model costs, partner ramp-up, "
        "capacity constraints, cannibalization, persistency changes, or probability "
        "of execution. Validate assumptions before using the outputs in a business case."
    )

else:
    header(
        "Project Portfolio & Execution",
        "Monitor strategic initiatives, execution health, delivery progress, and management priorities."
    )

    st.caption("PROJECT GOVERNANCE · EXECUTION TRACKING · ILLUSTRATIVE DATA ONLY")

    projects = pd.DataFrame([
        {
            "Project": "Partner expansion",
            "Workstream": "Distribution growth",
            "Owner": "Partnerships",
            "Status": "On track",
            "Progress": 75,
            "Risk": "Medium",
            "Next milestone": "Partner shortlist",
            "Days to milestone": 14,
        },
        {
            "Project": "Product launch readiness",
            "Workstream": "Product implementation",
            "Owner": "Product",
            "Status": "At risk",
            "Progress": 48,
            "Risk": "High",
            "Next milestone": "Readiness review",
            "Days to milestone": 7,
        },
        {
            "Project": "Digital channel enablement",
            "Workstream": "Digital distribution",
            "Owner": "Digital",
            "Status": "On track",
            "Progress": 62,
            "Risk": "Medium",
            "Next milestone": "Pilot validation",
            "Days to milestone": 21,
        },
        {
            "Project": "Partner productivity",
            "Workstream": "Performance improvement",
            "Owner": "Distribution",
            "Status": "Delayed",
            "Progress": 30,
            "Risk": "High",
            "Next milestone": "Recovery plan",
            "Days to milestone": 3,
        },
        {
            "Project": "Operational efficiency",
            "Workstream": "Process improvement",
            "Owner": "Operations",
            "Status": "Completed",
            "Progress": 100,
            "Risk": "Low",
            "Next milestone": "Benefits review",
            "Days to milestone": 30,
        },
    ])

    # --- Portfolio-level indicators ---
    total_projects = len(projects)
    on_track = int((projects["Status"] == "On track").sum())
    attention = int(projects["Status"].isin(["At risk", "Delayed"]).sum())
    completed = int((projects["Status"] == "Completed").sum())
    avg_progress = float(projects["Progress"].mean())
    high_risk = int((projects["Risk"] == "High").sum())

    k1, k2, k3, k4 = st.columns(4, gap="medium")

    k1.metric("TOTAL INITIATIVES", f"{total_projects}")
    k2.metric("ON TRACK", f"{on_track}")
    k3.metric("NEEDS ATTENTION", f"{attention}")
    k4.metric("AVERAGE PROGRESS", f"{avg_progress:.0f}%")

    st.divider()

    # --- Executive project health ---
    left, right = st.columns([1.2, 1], gap="medium")

    with left:
        st.subheader("Execution progress")
        st.caption("Progress by initiative, grouped by delivery status.")

        progress_data = projects.sort_values("Progress", ascending=True)

        fig = px.bar(
            progress_data,
            x="Progress",
            y="Project",
            color="Status",
            orientation="h",
            range_x=[0, 100],
            text="Progress",
            color_discrete_map={
                "On track": "#39a8a0",
                "At risk": "#f5ad42",
                "Delayed": "#dc6b4e",
                "Completed": "#2563eb",
            },
            labels={
                "Progress": "Completion (%)",
                "Project": "Initiative",
                "Status": "Delivery status",
            },
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        st.plotly_chart(style(fig, 390), use_container_width=True)

    with right:
        st.subheader("Portfolio risk profile")
        st.caption("Number of initiatives by current illustrative risk rating.")

        risk_order = ["Low", "Medium", "High"]
        risk_data = (
            projects["Risk"]
            .value_counts()
            .reindex(risk_order, fill_value=0)
            .rename_axis("Risk")
            .reset_index(name="Projects")
        )

        fig = px.bar(
            risk_data,
            x="Risk",
            y="Projects",
            color="Risk",
            category_orders={"Risk": risk_order},
            color_discrete_map={
                "Low": "#39a8a0",
                "Medium": "#f5ad42",
                "High": "#dc6b4e",
            },
            text="Projects",
            labels={"Projects": "Initiative count"},
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style(fig, 390), use_container_width=True)

    st.divider()

    # --- Management attention queue ---
    st.subheader("Management attention queue")
    st.caption(
        "Illustrative prioritization based on delivery status, risk, "
        "and milestone proximity. Confirm ownership and actual status before acting."
    )

    priority = projects[
        projects["Status"].isin(["At risk", "Delayed"])
        | (projects["Risk"] == "High")
    ].copy()

    if not priority.empty:
        priority["Priority"] = priority.apply(
            lambda row: (
                "Critical"
                if row["Status"] == "Delayed" and row["Risk"] == "High"
                else "High"
                if row["Risk"] == "High"
                else "Monitor"
            ),
            axis=1,
        )
        priority = priority.sort_values(
            ["Days to milestone", "Progress"],
            ascending=[True, True],
        )
        st.dataframe(
            priority[
                [
                    "Project",
                    "Owner",
                    "Status",
                    "Risk",
                    "Progress",
                    "Next milestone",
                    "Days to milestone",
                    "Priority",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("No initiatives currently meet the attention-screening rules.")

    st.divider()

    # --- Editable project tracker ---
    st.subheader("Project tracker")
    st.caption(
        "Edit the sample tracker below to demonstrate portfolio monitoring. "
        "Changes remain in the current app session; download the CSV to retain a copy."
    )

    edited = st.data_editor(
        projects,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "Progress": st.column_config.ProgressColumn(
                "Progress",
                min_value=0,
                max_value=100,
                format="%d%%",
            ),
            "Days to milestone": st.column_config.NumberColumn(
                "Days to milestone",
                min_value=0,
                step=1,
            ),
        },
    )

    st.download_button(
        "Download project tracker CSV",
        edited.to_csv(index=False).encode("utf-8"),
        "project_tracker.csv",
        "text/csv",
    )

    st.divider()

    # --- Decision log ---
    st.subheader("Decision log")
    st.caption("Capture a decision, accountable owner, due date, and supporting evidence.")

    decision = st.text_area(
        "Decision or next action",
        placeholder="Describe the decision, action, dependency, or issue...",
    )

    log_col1, log_col2 = st.columns(2)

    with log_col1:
        decision_owner = st.text_input(
            "Accountable owner",
            placeholder="Role or team",
        )

    with log_col2:
        decision_due = st.date_input(
            "Target date",
            value=None,
            format="DD/MM/YYYY",
        )

    if decision.strip():
        decision_record = pd.DataFrame([{
            "Decision or next action": decision.strip(),
            "Owner": decision_owner.strip(),
            "Target date": str(decision_due) if decision_due else "",
        }])

        st.download_button(
            "Download decision log CSV",
            decision_record.to_csv(index=False).encode("utf-8"),
            "decision_log.csv",
            "text/csv",
        )

    st.info(
        "Prototype limitation: project records are illustrative examples, not "
        "live project-management data. Editing the table does not persist changes "
        "to a database or synchronize them with another system."
    )

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
