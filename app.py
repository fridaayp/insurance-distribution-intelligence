from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st
import base64

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.analytics import (
    prepare_data, kpi_summary, partner_scorecard, monthly_trend,
    detect_underperformance, detect_monthly_anomalies, generate_recommendations,
)

st.set_page_config(page_title="Distribution Strategy Intelligence", page_icon="📊", layout="wide")
st.markdown("""
<style>
/* Clean, aligned sidebar navigation */
[data-testid="stSidebar"] [data-testid="stButton"] {
  width: 100%;
  margin: 0 !important;
  padding: 0 !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] > button {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  : 100% !important;
  min-height: 39px !important;
  height: 39px !important;
  padding: 0 12px !important;
  margin: 0 !important;
  border: 1px solid transparent !important;
  border-radius: 8px !important;
  background: transparent !important;
  color: #c5d5e9 !important;
  box-shadow: none !important;
  transform: none !important;
  text-align: left !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] > button > div {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  width: 100% !important;
  gap: 10px !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] > button p {
  text-align: left !important;
  font-size: 13px !important;
  font-weight: 550 !important;
  line-height: 1.25 !important;
  margin: 0 !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
  background: rgba(255,255,255,.07) !important;
  color: #fff !important;
  border-color: rgba(255,255,255,.08) !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] > button[kind="primary"] {
  background: #1e467f !important;
  color: #fff !important;
  border-color: rgba(132,177,255,.18) !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] > button[kind="primary"] p {
  color: #fff !important;
  font-weight: 700 !important;
}
/* Sidebar: sticky viewport layout, without fighting Streamlit */
[data-testid="stSidebar"] {
  position: sticky !important;
  top: 0 !important;
  align-self: flex-start !important;
  height: 100vh !important;
  min-height: 100vh !important;
  max-height: 100vh !important;
  box-sizing: border-box !important;
  background: linear-gradient(
    180deg,
    #081a30 0%,
    #102b49 58%,
    #081a2e 100%
  ) !important;
  border-right: 1px solid rgba(255,255,255,.08);
  overflow: hidden !important;
}

[data-testid="stSidebar"] > div:first-child {
  height: 100vh !important;
  max-height: 100vh !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  box-sizing: border-box !important;
  padding: 1rem .85rem 1.25rem !important;
  scrollbar-width: none !important;
}

[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {
  display: none !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
  color: #eaf2ff;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
  color: #a8bdd8;
}

[data-testid="stSidebar"] hr {
  border-color: rgba(180,205,240,.16);
  margin: .85rem 0;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > label {
  color: #9db5d4;
  font-size: .68rem;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
  margin-bottom: .55rem;
}

[data-testid="stSidebar"] div[role="radiogroup"] {
  gap: .3rem;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
  display: flex;
  align-items: center;
  min-height: 40px;
  padding: .45rem .65rem;
  margin: 0;
  border: 1px solid transparent;
  border-radius: 9px;
  color: #c5d5e9;
  font-size: .82rem;
  font-weight: 550;
}

[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
  display: none !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
  background: rgba(255,255,255,.07);
  border-color: rgba(255,255,255,.1);
  color: #fff;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
  background: linear-gradient(105deg, #2053a0, #173c77);
  border-color: rgba(132,177,255,.25);
  color: #fff;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
  color: #fff;
  font-weight: 750;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] > label,
[data-testid="stSidebar"] [data-testid="stDateInput"] > label,
[data-testid="stSidebar"] [data-testid="stSlider"] > label {
  color: #b2c5de;
  font-size: .74rem;
  font-weight: 650;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-testid="stDateInput"] input {
  background: #172f4a;
  color: #f3f7ff;
  border-color: #385574;
  border-radius: 9px;
}

[data-testid="stSidebar"] [data-testid="stSlider"] {
  padding-bottom: .25rem;
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

logo_path = ROOT / "assets" / "logo.png"
logo_base64 = base64.b64encode(
    logo_path.read_bytes()
).decode("utf-8")

with st.sidebar:
    st.html(f"""
    <div style="
        padding: 8px 0 14px;
        margin-bottom: 14px;
        border-bottom: 1px solid rgba(180,205,240,.14);
    ">
      <div style="
          display: flex;
          align-items: center;
          gap: 10px;
      ">
        <img
          src="data:image/png;base64,{logo_base64}"
          alt="Distribution Strategy Intelligence"
          style="
              width: 58px;
              height: 62px;
              object-fit: contain;
              flex: 0 0 58px;
              display: block;
          "
        />

        <div style="
            min-width: 0;
            color: #f6f9ff;
            font-size: 18px;
            font-weight: 750;
            line-height: 1.3;
            letter-spacing: -0.25px;
        ">
          <div>Distribution</div>
          <div>Strategy Intelligence</div>
        </div>
      </div>

      <div style="
          margin: 8px 0 0 68px;
          color: #9fb8d8;
          font-size: 11px;
          line-height: 1.4;
          letter-spacing: .15px;
      ">From data to decisions</div>
    </div>
    """)

    pages = [
        "Executive Overview",
        "Performance Analysis",
        "Partnership Intelligence",
        "Scenario Lab",
        "Project Portfolio & Execution",
    ]

    page_labels = {
        "Executive Overview": "⌂   Executive Overview",
        "Performance Analysis": "▥   Performance Analysis",
        "Partnership Intelligence": "♧   Partnership Intelligence",
        "Scenario Lab": "↗️   Scenario Lab",
        "Project Portfolio & Execution": "▤   Project Portfolio & Execution",
    }

    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "Executive Overview"

    for target_page in pages:
        nav_icons = {
        "Executive Overview": ":material/dashboard:",
        "Performance Analysis": ":material/analytics:",
        "Partnership Intelligence": ":material/handshake:",
        "Scenario Lab": ":material/trending_up:",
        "Project Portfolio & Execution": ":material/assignment:",
    }

    for target_page in pages:
        if st.button(
            target_page,
            key=f"nav_{target_page}",
            icon=nav_icons[target_page],
            type=(
                "primary"
                if st.session_state["selected_page"] == target_page
                else "secondary"
            ),
            use_container_width=True,
        ):
            st.session_state["selected_page"] = target_page
            st.rerun()

    page = st.session_state["selected_page"]

    st.divider()

    st.markdown(
        """
        <div style="color:#e1ebfa;font-size:11px;font-weight:800;
                    letter-spacing:.9px;margin:0 0 12px;">
          GLOBAL FILTERS
        </div>
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

    # Month-level global filter: defaults to all available data.
    month_keys = sorted(
        data["month"].dropna().dt.to_period("M").astype(str).unique().tolist()
    )

    month_labels = {
        key: pd.Period(key, freq="M").strftime("%b %Y")
        for key in month_keys
    }

    if not month_keys:
        st.error("No valid month values are available in the dataset.")
        st.stop()

    period_cols = st.columns(2, gap="small")

    with period_cols[0]:
        period_start_key = st.selectbox(
            "Period from",
            options=month_keys,
            index=0,
            format_func=lambda value: month_labels[value],
            key="period_start_month",
            help="First month included in the analysis.",
        )

    end_options = [
        key for key in month_keys
        if key >= period_start_key
    ]

    if st.session_state.get("period_end_month") not in end_options:
        st.session_state["period_end_month"] = end_options[-1]

    with period_cols[1]:
        period_end_key = st.selectbox(
            "Period to",
            options=end_options,
            format_func=lambda value: month_labels[value],
            key="period_end_month",
            help="Last month included in the analysis.",
        )

    period_start = (
        pd.Period(period_start_key, freq="M").start_time.date()
    )
    period_end = (
        pd.Period(period_end_key, freq="M").end_time.date()
    )

    dates = (period_start, period_end)

    threshold = st.slider(
        "Underperformance threshold (%)",
        min_value=50,
        max_value=110,
        value=85,
        step=5,
    ) / 100

    st.divider()

    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;padding:7px 2px;">
          <div style="width:43px;height:43px;min-width:43px;border-radius:50%;
                      background:linear-gradient(145deg,#315eb2,#203b75);
                      border:1px solid #5e8eea;display:flex;align-items:center;
                      justify-content:center;color:#fff;font-size:15px;font-weight:850;">
            FY
          </div>
          <div>
            <div style="font-size:13px;font-weight:800;color:#f5f8ff;">
              Frida Yuniar Prastika
            </div>
            <div style="font-size:10px;color:#9fb8d8;line-height:1.5;">
              Business Strategy &amp; Analytics
            </div>
          </div>
        </div>
        <div style="font-size:10px;color:#7f99b9;margin:8px 2px 0;">
          Portfolio prototype · Synthetic data
        </div>
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
    df = df[
        (df.month.dt.date >= dates[0])
        & (df.month.dt.date <= dates[1])
    ]
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
def _month_window(frame, start_period, end_period):
    start_period = pd.Period(start_period, freq="M")
    end_period = pd.Period(end_period, freq="M")
    months = frame["month"].dt.to_period("M")
    return frame.loc[
        (months >= start_period) & (months <= end_period)
    ].copy()


def _window_is_available(start_period, end_period, available_months):
    start_period = pd.Period(start_period, freq="M")
    end_period = pd.Period(end_period, freq="M")
    expected = {
        str(p) for p in pd.period_range(
            start_period, end_period, freq="M"
        )
    }
    return expected.issubset(set(available_months))


def _comparison_summary(frame):
    if frame is None or frame.empty:
        return None

    actual_value = float(frame["premium_actual_idr"].sum())
    target_value = float(frame["premium_target_idr"].sum())

    return {
        "actual": actual_value,
        "target": target_value,
        "attainment": (
            actual_value / target_value if target_value else None
        ),
        "gap": target_value - actual_value,
        "partners": int(frame["partner"].nunique()),
        "policies": int(frame["policies_issued"].sum()),
    }

# EXECUTIVE OVERVIEW V3 PATCH FOR app.py
# 1) Insert the helper functions below immediately before `if page == "Executive Overview":`.
# 2) Replace the current Executive Overview block through (but not including)
#    `elif page == "Performance Analysis":` with the section below.
# Sidebar, global filters, data loading, and other pages remain unchanged.

# ---------- HELPERS ----------
def _month_window(frame, start_period, end_period):
    months = frame["month"].dt.to_period("M")
    return frame.loc[(months >= pd.Period(start_period, freq="M")) &
                     (months <= pd.Period(end_period, freq="M"))].copy()


def _window_is_available(start_period, end_period, available_months):
    expected = {str(p) for p in pd.period_range(start_period, end_period, freq="M")}
    return expected.issubset(set(available_months))


def _comparison_summary(frame):
    if frame is None or frame.empty:
        return None
    actual_value = float(frame["premium_actual_idr"].sum())
    target_value = float(frame["premium_target_idr"].sum())
    return {
        "actual": actual_value,
        "target": target_value,
        "attainment": actual_value / target_value if target_value else None,
        "gap": target_value - actual_value,  # positive = shortfall
        "partners": int(frame["partner"].nunique()),
    }


def _comparison_delta(current, previous, metric):
    if previous is None or current.get(metric) is None or previous.get(metric) is None:
        return "N/A"
    c, p = current[metric], previous[metric]
    if metric == "attainment":
        return f"{(c - p) * 100:+.1f} pp"
    if metric == "partners":
        return f"{int(c - p):+d}"
    if metric == "gap":
        change = p - c  # positive means the shortfall narrowed
        return f"gap {'reduced' if change >= 0 else 'widened'} {money(abs(change))}"
    if p == 0:
        return "N/A"
    return f"{(c / p - 1) * 100:+.1f}%"


def _comparison_row(label, current, previous, metric):
    delta = _comparison_delta(current, previous, metric)
    if delta == "N/A":
        color, arrow = "#7b8ba1", "—"
    elif metric == "gap":
        improved = previous is not None and current["gap"] <= previous["gap"]
        color, arrow = ("#247b62", "↓") if improved else ("#bd514b", "↑")
    else:
        try:
            numeric = float(delta.split()[0].replace("%", "").replace("pp", "").replace("+", ""))
        except (ValueError, IndexError):
            numeric = 0
        color, arrow = ("#247b62", "↑") if numeric >= 0 else ("#bd514b", "↓")
    return (f'<div class="comparison-row"><span>{label}</span>'
            f'<strong style="color:{color}">{arrow} {delta}</strong></div>')


def _kpi_card(title, value, help_text, metric, current, previous_period, previous_year):
    return f'''<div class="exec-kpi" title="{help_text}">
      <div class="exec-kpi-label">{title}</div><div class="exec-kpi-value">{value}</div>
      <div class="exec-kpi-comparisons">
        {_comparison_row("vs previous period", current, previous_period, metric)}
        {_comparison_row("vs previous year", current, previous_year, metric)}
      </div></div>'''


# ---------- EXECUTIVE OVERVIEW SECTION ----------
if page == "Executive Overview":
    header(
        "Executive Overview",
        "Distribution performance, target delivery, partner contribution, and management priorities."
    )

    # Restrained navy / blue / neutral palette. Sidebar styling is untouched.
    st.markdown("""
    <style>
      /* Executive Overview — refined visual system */
.exec-kpi {
    position: relative;
    background: linear-gradient(145deg, #ffffff, #f9fbfe);
    border: 1px solid #e1e9f3;
    border-radius: 14px;
    padding: 17px 18px 13px;
    min-height: 165px;
    box-shadow: 0 4px 14px rgba(16, 35, 63, 0.045);
}

.exec-kpi:before {
    content: "";
    position: absolute;
    top: 15px;
    bottom: 15px;
    left: 0;
    width: 3px;
    border-radius: 0 4px 4px 0;
    background: #3978b8;
}

.exec-kpi-label {
    color: #647791;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.exec-kpi-value {
    color: #10233f;
    font-size: clamp(23px, 2vw, 30px);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.25;
    margin: 9px 0 14px;
    overflow-wrap: anywhere;
}

.exec-kpi-comparisons {
    border-top: 1px solid #eaf0f6;
    padding-top: 7px;
}

.comparison-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    color: #77879c;
    font-size: 10px;
    padding: 4px 0;
}

.comparison-row strong {
    font-size: 10px;
    font-weight: 800;
    text-align: right;
}

.exec-section-note {
    color: #7a8ba1;
    font-size: 11px;
    line-height: 1.5;
    margin-top: -6px;
    margin-bottom: 10px;
}

.exec-insight {
    border: 1px solid #e1e9f2;
    background: linear-gradient(135deg, #ffffff, #f9fbfe);
    border-radius: 12px;
    padding: 13px 15px;
    margin-bottom: 9px;
    box-shadow: 0 2px 8px rgba(16, 35, 63, 0.025);
}

.exec-insight-title {
    color: #183452;
    font-size: 12px;
    font-weight: 800;
    margin-bottom: 5px;
}

.exec-insight-body {
    color: #536781;
    font-size: 12px;
    line-height: 1.55;
}

.exec-table-wrap {
    border: 1px solid #e1e9f2;
    border-radius: 12px;
    overflow: hidden;
    background: #fff;
}

.exec-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
}

.exec-table th {
    background: #f3f7fb;
    color: #61748d;
    font-size: 10px;
    font-weight: 800;
    text-align: left;
    text-transform: uppercase;
    padding: 11px 10px;
    border-bottom: 1px solid #e5ebf3;
}

.exec-table td {
    padding: 10px;
    border-bottom: 1px solid #edf1f6;
    color: #344b67;
    vertical-align: middle;
}

.exec-table tr:last-child td {
    border-bottom: 0;
}

.exec-rank {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 7px;
    background: #edf4fc;
    color: #2e6fae;
    font-weight: 800;
}

.exec-bar-track {
    height: 6px;
    background: #eaf0f6;
    border-radius: 20px;
    overflow: hidden;
    min-width: 45px;
}

.exec-bar-fill {
    height: 100%;
    background: #5a91c9;
    border-radius: 20px;
}

.exec-action {
    display: flex;
    gap: 11px;
    padding: 12px 0;
    border-bottom: 1px solid #edf1f6;
}

.exec-action:last-child {
    border-bottom: 0;
}

.exec-action-number {
    flex: 0 0 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #e9f1fa;
    color: #2e6fae;
    font-weight: 800;
    font-size: 12px;
}

.exec-action-copy {
    color: #536781;
    font-size: 12px;
    line-height: 1.5;
}

.exec-action-copy strong {
    color: #183452;
}
    </style>""", unsafe_allow_html=True)

    st.caption("PORTFOLIO SNAPSHOT · CURRENT FILTER SELECTION")
    st.caption(
        f"Selected window: {pd.Period(period_start_key, freq='M').strftime('%b %Y')} — "
        f"{pd.Period(period_end_key, freq='M').strftime('%b %Y')} · {partner} · {channel}"
    )

    # Build comparison data using the same partner/channel filters as the current view.
    comparison_base = data.copy()
    if partner != "All partners":
        comparison_base = comparison_base[comparison_base["partner"] == partner]
    if channel != "All channels":
        comparison_base = comparison_base[comparison_base["channel"] == channel]

    start_p, end_p = pd.Period(period_start_key, "M"), pd.Period(period_end_key, "M")
    month_count = end_p.ordinal - start_p.ordinal + 1
    available_months = set(data["month"].dropna().dt.to_period("M").astype(str))
    pp_start, pp_end = start_p - month_count, start_p - 1
    py_start, py_end = start_p - 12, end_p - 12

    previous_period = (
        _comparison_summary(_month_window(comparison_base, pp_start, pp_end))
        if _window_is_available(pp_start, pp_end, available_months) else None
    )
    previous_year = (
        _comparison_summary(_month_window(comparison_base, py_start, py_end))
        if _window_is_available(py_start, py_end, available_months) else None
    )
    current = {
        "actual": actual,
        "attainment": attainment if target else None,
        "gap": target - actual,
        "partners": int(df["partner"].nunique()),
    }

    kpi_cols = st.columns(4, gap="medium")
    cards = [
        _kpi_card("Total Premium", money(actual), "Actual premium in the selected window.",
                  "actual", current, previous_period, previous_year),
        _kpi_card("Target Attainment", f"{attainment:.1%}", "Actual premium divided by target premium.",
                  "attainment", current, previous_period, previous_year),
        _kpi_card("Premium Gap", f"{money(abs(target-actual))} {'shortfall' if target > actual else 'surplus'}",
                  "Target minus actual premium; positive means a shortfall.",
                  "gap", current, previous_period, previous_year),
        _kpi_card("Active Partners", f"{df['partner'].nunique():,}", "Unique partners in the selected window.",
                  "partners", current, previous_period, previous_year),
    ]
    for col, card in zip(kpi_cols, cards):
        with col:
            st.markdown(card, unsafe_allow_html=True)

    st.write("")
    chart_left, chart_right = st.columns([1.55, 1], gap="medium")
    with chart_left:
        st.subheader("Premium vs target over time")
        st.markdown('<div class="exec-section-note">Monthly actual premium against target; hover for exact values.</div>', unsafe_allow_html=True)
        if not trend.empty:
            trend_view = trend.copy()
            trend_view["Actual premium"] = trend_view["premium_actual_idr"]
            trend_view["Target premium"] = trend_view["premium_target_idr"]
            fig = px.line(
                trend_view, x="month", y=["Actual premium", "Target premium"], markers=True,
                color_discrete_map={"Actual premium":"#3978B8", "Target premium":"#A8BCD4"},
                labels={"value":"Premium (IDR)", "month":"Month", "variable":""},
            )
            fig.update_traces(line=dict(width=2.7), marker=dict(size=5))
            fig.update_yaxes(tickprefix="Rp ", tickformat="~s", rangemode="tozero")
            fig.update_xaxes(tickformat="%b %Y", dtick="M2")
            fig.update_layout(hovermode="x unified", showlegend=True)
            st.plotly_chart(style(fig, 365), use_container_width=True)
        else:
            st.info("Not enough monthly data to draw the trend.")

    with chart_right:
        st.subheader("Target attainment by channel")
        st.markdown('<div class="exec-section-note">Actual premium ÷ target premium.</div>', unsafe_allow_html=True)
        channel_view = df.groupby("channel", as_index=False).agg(
            premium_actual_idr=("premium_actual_idr", "sum"),
            premium_target_idr=("premium_target_idr", "sum"),
        )
        channel_view["attainment"] = channel_view["premium_actual_idr"] / channel_view["premium_target_idr"].replace(0, float("nan"))
        channel_view = channel_view.dropna(subset=["attainment"]).sort_values("attainment")
        if not channel_view.empty:
            fig = px.bar(
                channel_view, x="attainment", y="channel", orientation="h",
                text=channel_view["attainment"].map(lambda x: f"{x:.0%}"),
                labels={"attainment":"Target attainment", "channel":""},
                color_discrete_sequence=["#3978B8"],
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.add_vline(x=1, line_dash="dash", line_color="#91A8C4", annotation_text="Target 100%")
            fig.update_xaxes(tickformat=".0%", range=[0, max(1.15, float(channel_view["attainment"].max())*1.15)])
            fig.update_layout(showlegend=False)
            st.plotly_chart(style(fig, 365), use_container_width=True)
        else:
            st.info("No channel attainment values are available for this selection.")

    # Aggregate by partner to avoid duplicate partner rows across channels.
    partner_view = df.groupby("partner", as_index=False).agg(
        premium_actual_idr=("premium_actual_idr", "sum"),
        premium_target_idr=("premium_target_idr", "sum"),
        policies_issued=("policies_issued", "sum"),
    )
    partner_view["attainment_rate"] = partner_view["premium_actual_idr"] / partner_view["premium_target_idr"].replace(0, float("nan"))
    partner_view["gap_to_target"] = partner_view["premium_target_idr"] - partner_view["premium_actual_idr"]

    table_left, table_right = st.columns(2, gap="medium")
    with table_left:
        st.subheader("Top partners by actual premium")
        st.markdown(
            '<div class="exec-section-note">'
            'Ranked by actual premium in the current selection.'
            '</div>',
            unsafe_allow_html=True,
        )

        top = partner_view.nlargest(5, "premium_actual_idr").copy()

        if not top.empty:
            top["Actual premium"] = top["premium_actual_idr"].map(money)
            top["Target attainment"] = top["attainment_rate"].map(
                lambda v: f"{v:.0%}" if pd.notna(v) else "N/A"
            )
            top = top.rename(columns={"partner": "Partner"})
            rows_html = []

            max_premium = max(
                float(v) for v in top["premium_actual_idr"]
            ) or 1

            for rank, (_, row) in enumerate(top.iterrows(), start=1):
                pct = (
                    float(row["attainment_rate"])
                    if pd.notna(row["attainment_rate"])
                    else 0
                )
                premium_width = min(
                    100,
                    max(
                        0,
                        float(row["premium_actual_idr"])
                        / max_premium * 100,
                    ),
                )
                pct_color = (
                    "#247b62" if pct >= 1
                    else "#bd514b" if pct < threshold
                    else "#536781"
                )

                rows_html.append(
                    f'<tr><td><span class="exec-rank">{rank}</span></td>'
                    f'<td><strong>{row["Partner"]}</strong></td>'
                    f'<td><strong>{money(float(row["premium_actual_idr"]))}</strong>'
                    f'<div class="exec-bar-track" style="margin-top:6px">'
                    f'<div class="exec-bar-fill" style="width:{premium_width:.1f}%"></div>'
                    f'</div></td>'
                    f'<td><strong style="color:{pct_color}">{pct:.0%}</strong></td></tr>'
                )

            st.markdown(
                '<div class="exec-table-wrap"><table class="exec-table">'
                '<thead><tr><th>#</th><th>Partner</th>'
                '<th>Actual premium</th><th>Attainment</th></tr></thead><tbody>'
                + "".join(rows_html)
                + '</tbody></table></div>',
                unsafe_allow_html=True,
            )
        else:
            st.info("No partner records in this selection.")

    with table_right:
        st.subheader("Partners requiring attention")
        st.markdown(f'<div class="exec-section-note">Rule-based screen: attainment below {threshold:.0%}.</div>', unsafe_allow_html=True)
        attention = partner_view[partner_view["attainment_rate"] < threshold].sort_values("attainment_rate").head(5).copy()
        if not attention.empty:
            attention["Target attainment"] = attention["attainment_rate"].map(
                lambda v: f"{v:.0%}" if pd.notna(v) else "N/A"
            )
            attention["Gap to target"] = attention["gap_to_target"].map(
                lambda v: money(v) if v >= 0
                else f"{money(abs(v))} surplus"
            )
            attention = attention.rename(columns={"partner": "Partner"})
            rows_html = []

            for rank, (_, row) in enumerate(attention.iterrows(), start=1):
                pct = (
                    float(row["attainment_rate"])
                    if pd.notna(row["attainment_rate"])
                    else 0
                )
                bar_width = min(100, max(0, pct * 100))
                gap = float(row["gap_to_target"])
                gap_text = (
                    money(gap) if gap >= 0
                    else f"{money(abs(gap))} surplus"
                )
                gap_color = "#bd514b" if gap > 0 else "#247b62"

                rows_html.append(
                    f'<tr><td><span class="exec-rank">{rank}</span></td>'
                    f'<td><strong>{row["Partner"]}</strong></td>'
                    f'<td><strong style="color:#bd514b">{pct:.0%}</strong>'
                    f'<div class="exec-bar-track" style="margin-top:6px">'
                    f'<div class="exec-bar-fill" style="width:{bar_width:.1f}%;'
                    f'background:#c87976"></div></div></td>'
                    f'<td><strong style="color:{gap_color}">{gap_text}</strong></td></tr>'
                )

            st.markdown(
                '<div class="exec-table-wrap"><table class="exec-table">'
                '<thead><tr><th>#</th><th>Partner</th><th>Attainment</th>'
                '<th>Gap to target</th></tr></thead><tbody>'
                + "".join(rows_html)
                + '</tbody></table></div>',
                unsafe_allow_html=True,
            )
        else:
            st.success("No partners fall below the selected threshold.")

    insight_col, action_col = st.columns([1.25, 1], gap="medium")

    insight_col, action_col = st.columns([1.25, 1], gap="medium")
    with insight_col:
        st.subheader("Key Insights")
        st.markdown('<div class="exec-section-note">What the current data indicates.</div>', unsafe_allow_html=True)
        gap_value = target - actual
        if target > 0:
            if gap_value > 0:
                st.warning(f"Portfolio attainment is **{attainment:.1%}**, with a premium shortfall of **{money(gap_value)}**.")
            else:
                st.success(f"Portfolio is above target by **{money(abs(gap_value))}** ({attainment:.1%} attainment).")
        if previous_period is not None:
            st.caption(f"Previous period: premium {_comparison_delta(current, previous_period, 'actual')}; attainment {_comparison_delta(current, previous_period, 'attainment')}.")
        else:
            st.caption("Previous period: N/A — the full comparison window is not available.")
        if previous_year is not None:
            st.caption(f"Previous year: premium {_comparison_delta(current, previous_year, 'actual')}; attainment {_comparison_delta(current, previous_year, 'attainment')}.")
        else:
            st.caption("Previous year: N/A — the full comparison window is not available.")

        if not channel_view.empty:
            strongest = channel_view.sort_values("attainment", ascending=False).iloc[0]
            st.markdown(f'<div class="exec-insight"><div class="exec-insight-title">Channel signal</div><div class="exec-insight-body"><b>{strongest["channel"]}</b> has the highest attainment at <b>{strongest["attainment"]:.0%}</b> in this selection.</div></div>', unsafe_allow_html=True)
        if not attention.empty:
            weakest = attention.iloc[0]
            st.markdown(f'<div class="exec-insight"><div class="exec-insight-title">Partner attention</div><div class="exec-insight-body"><b>{weakest["Partner"]}</b> has the lowest attainment ({weakest["attainment_rate"]:.0%}); review target, funnel, and recent activity before drawing causal conclusions.</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="exec-insight"><div class="exec-insight-title">Operational signals</div><div class="exec-insight-body">{int(under["partner"].nunique()) if not under.empty else 0} partner(s) below threshold · {len(anomalies)} monthly anomaly alert(s) · {int(df["policies_issued"].sum()):,} policies issued.</div></div>', unsafe_allow_html=True)

    with action_col:
        st.subheader("Recommended Actions")
        st.markdown(
            '<div class="exec-section-note">'
            'Rule-based prompts for management review, not causal conclusions.'
            '</div>',
            unsafe_allow_html=True,
        )

        if actions:
            action_df = pd.DataFrame(actions)
            columns = [
                c for c in [
                    "priority", "partner", "signal", "suggested_action"
                ]
                if c in action_df.columns
            ]
            action_rows = []

            for i, (_, row) in enumerate(
                action_df[columns].head(6).iterrows(), start=1
            ):
                priority = str(row.get("priority", "Review"))
                partner_name = str(row.get("partner", "Portfolio"))
                signal = str(
                    row.get("signal", "Review performance signal")
                )
                recommendation = str(
                    row.get(
                        "suggested_action",
                        "Validate the data and agree next steps."
                    )
                )

                priority_color = (
                    "#bd514b" if priority.lower() == "high"
                    else "#9a6b24" if priority.lower() == "medium"
                    else "#3978b8"
                )

                action_rows.append(
                    f'<div class="exec-action">'
                    f'<div class="exec-action-number">{i}</div>'
                    f'<div class="exec-action-copy">'
                    f'<div style="display:flex;gap:8px;'
                    f'flex-wrap:wrap;align-items:center">'
                    f'<strong>{partner_name}</strong>'
                    f'<span style="font-size:10px;font-weight:800;'
                    f'color:{priority_color};background:#f3f6fa;'
                    f'padding:3px 8px;border-radius:20px">'
                    f'{priority}</span></div>'
                    f'<div style="margin-top:5px">{signal}</div>'
                    f'<div style="margin-top:5px;color:#71829a">'
                    f'{recommendation}</div>'
                    f'</div></div>'
                )

            st.markdown(
                '<div class="exec-table-wrap" style="padding:2px 14px">'
                + "".join(action_rows)
                + '</div>',
                unsafe_allow_html=True,
            )
        else:
            st.success(
                "No rule-based actions were triggered for this selection."
            )

        if not anomalies.empty:
            st.info(
                f"{len(anomalies)} monthly premium-drop alert(s) detected. "
                "Validate the underlying records before acting."
            )

# Keep the existing `elif page == "Performance Analysis":` and every later page unchanged.

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
