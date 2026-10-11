from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st
import base64
import plotly.express as px
import plotly.graph_objects as go

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

    # Month-level global filter:
    # default to Jan-Sep 2026 when those months are available.
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

    # Versioned keys initialize the new default without reusing
    # stale selections from the previous filter widgets.
    start_key = "period_start_month_v2"
    end_key = "period_end_month_v2"

    default_start = "2026-01" if "2026-01" in month_keys else month_keys[0]

    if start_key not in st.session_state:
        st.session_state[start_key] = default_start

    period_cols = st.columns(2, gap="small")

    with period_cols[0]:
        period_start_key = st.selectbox(
            "Period from",
            options=month_keys,
            format_func=lambda value: month_labels[value],
            key=start_key,
            help="First month included in the analysis.",
        )

    end_options = [
        key for key in month_keys
        if key >= period_start_key
    ]

    default_end = (
        "2026-09"
        if "2026-09" in end_options
        else end_options[-1]
    )

    if (
        end_key not in st.session_state
        or st.session_state[end_key] not in end_options
    ):
        st.session_state[end_key] = default_end

    with period_cols[1]:
        period_end_key = st.selectbox(
            "Period to",
            options=end_options,
            format_func=lambda value: month_labels[value],
            key=end_key,
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
# 1) Insert the helper functions below immediately before ` Overview":`.
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
    # =========================================================
    # EXECUTIVE OVERVIEW — VISUAL FOUNDATION
    # Sidebar, navigation, filters, and other pages unchanged.
    # =========================================================

    st.markdown("""
    <style>
    /* Page rhythm */
    .block-container {
        padding-top: 1.25rem;
        padding-bottom: 1.8rem;
        max-width: 100%;
    }

    /* Header: keep title and demo disclosure visually connected */
.eo-header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 4px;
    margin-bottom: 18px;
}

.eo-header > div:last-child {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 8px;
    width: 100%;
    min-width: 0;
}

.eo-demo-badge {
    display: inline-flex;
    align-items: center;
    flex-wrap: nowrap;
    width: fit-content;
    max-width: 100%;
}

.eo-disclaimer {
    max-width: 100%;
    margin: 0;
    text-align: left;
    white-space: normal;
    overflow-wrap: anywhere;
}

.eo-title {
    color: #102844;
    font-size: clamp(30px, 2.6vw, 36px);
    font-weight: 800;
    letter-spacing: -1.15px;
    line-height: 1.08;
    margin: 0 !important;
    padding: 0 !important;
}

.eo-subtitle {
    color: #718198;
    font-size: 12px;
    font-weight: 450;
    line-height: 1.4;
    margin-top: 0;
    padding: 0;
}

.eo-disclaimer {
    color: #657b95;
    font-size: 10px;
    line-height: 1.3;
    margin-top: 5px;
    max-width: none;
    white-space: nowrap;
    text-align: right;
    margin-left: 0;
}

/* Context bar: protect the reporting-period column */
.eo-context {
    display: grid;
    grid-template-columns: minmax(220px, 1.35fr) repeat(3, minmax(135px, 1fr));
    background: #ffffff;
    border: 1px solid #dce5ef;
    border-radius: 10px;
    margin: 0 0 18px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(16, 40, 68, 0.035);
}

.eo-context-item {
    min-width: 0;
    padding: 13px 15px;
    border-right: 1px solid #e8eef5;
}

.eo-context-value {
    color: #233d5c;
    font-size: 11px;
    font-weight: 700;
    line-height: 1.4;
    overflow-wrap: anywhere;
}

/* KPI cards: consistent height and less vertical waste */
.eo-kpi {
    background: #ffffff;
    border: 1px solid #e0e8f1;
    border-radius: 12px;
    padding: 15px 14px 12px;
    min-height: 154px;
    height: 100%;
    box-shadow: 0 2px 7px rgba(16,40,68,.025);
}

.eo-kpi-value {
    color: #102844;
    font-size: clamp(22px, 1.9vw, 29px);
    font-weight: 820;
    line-height: 1.15;
    letter-spacing: -.8px;
    overflow-wrap: anywhere;
}

.eo-kpi-note {
    color: #8492a4;
    font-size: 10px;
    line-height: 1.4;
    min-height: 14px;
    margin-bottom: 9px;
}

.eo-kpi-comparison {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    border-top: 1px solid #edf1f6;
    padding-top: 7px;
    margin-top: 6px;
    font-size: 10px;
    line-height: 1.35;
}

.eo-kpi-comparison strong {
    color: #405874;
    font-size: 10px;
    font-weight: 750;
    text-align: right;
    overflow-wrap: anywhere;
}

.eo-signal {
    margin: 10px 0 16px;
}

@media (max-width: 1100px) {
    .eo-context {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .eo-context-item:nth-child(2) {
        border-right: none;
    }

    .eo-context-item:nth-child(-n+2) {
        border-bottom: 1px solid #e8eef5;
    }
}

@media (max-width: 700px) {
    .eo-header {
        flex-direction: column;
        gap: 9px;
    }

    .eo-header > div:last-child {
    flex: 0 0 auto;
    min-width: 0;
    text-align: right;
}

    .eo-disclaimer {
        text-align: left;
        margin-left: 0;
    }

    .eo-context {
        grid-template-columns: 1fr 1fr;
    }
}

    /* Section hierarchy */
    /* Chart titles — premium executive hierarchy */
    .exec-panel-title {
        color: #102844 !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        letter-spacing: -0.55px !important;
        line-height: 1.25 !important;
        margin: 0 0 7px !important;
    }

    .exec-panel-sub {
        color: #718198 !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        line-height: 1.5 !important;
        margin: 0 0 12px !important;
    }
    .eo-section-heading {
        color: #1a3554;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin: 0 0 10px;
    }
    .eo-section-note {
        color: #8291a5;
        font-size: 10px;
        margin: -4px 0 12px;
        line-height: 1.5;
    }

    /* KPI cards */
    .eo-kpi {
        background: #ffffff;
        border: 1px solid #e0e8f1;
        border-radius: 12px;
        padding: 16px 16px 12px;
        min-height: 150px;
        box-shadow: 0 2px 7px rgba(16,40,68,.025);
    }
    .eo-kpi-label {
        color: #73869d;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: .09em;
        text-transform: uppercase;
        min-height: 14px;
    }
    .eo-kpi-value-row {
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 7px;
        margin: 11px 0 7px;
    }
    .eo-kpi-value {
        color: #102844;
        font-size: clamp(23px, 2.1vw, 31px);
        font-weight: 820;
        line-height: 1.12;
        letter-spacing: -1px;
        overflow-wrap: anywhere;
    }
    .eo-kpi-note {
        color: #8492a4;
        font-size: 10px;
        line-height: 1.45;
        min-height: 15px;
        margin-bottom: 11px;
    }
    .eo-kpi-comparison {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        border-top: 1px solid #edf1f6;
        padding-top: 7px;
        margin-top: 6px;
        font-size: 10px;
        line-height: 1.35;
    }
    .eo-kpi-comparison span {
        color: #7d8da1;
    }
    .eo-kpi-comparison strong {
        color: #405874;
        font-size: 10px;
        font-weight: 750;
        text-align: right;
    }

    /* Portfolio signal */
    .eo-signal {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 11px 14px;
        margin: 12px 0 20px;
        border: 1px solid #eadfca;
        border-left: 3px solid #b88735;
        border-radius: 8px;
        background: #fffdf8;
        color: #715a34;
        font-size: 11px;
        line-height: 1.55;
    }
    .eo-signal-label {
        color: #614820;
        font-weight: 800;
        white-space: nowrap;
    }
    .eo-signal.good {
        background: #f7fbf8;
        border-color: #dce9df;
        border-left-color: #4e8b6a;
        color: #476b55;
    }
    .eo-signal.good .eo-signal-label {
        color: #2e6847;
    }

    @media (max-width: 900px) {
        .eo-context {
            grid-template-columns: 1fr 1fr;
        }
        .eo-context-item:nth-child(2) {
            border-right: none;
        }
        .eo-context-item:nth-child(-n+2) {
            border-bottom: 1px solid #e8eef5;
        }
        .eo-header {
            flex-direction: column;
            gap: 10px;
        }
        .eo-disclaimer {
            text-align: left;
        }
    }
    /* Executive chart typography */
    .block-container h2,
    .block-container h3 {
        color: #102844 !important;
        font-weight: 750 !important;
        letter-spacing: -0.35px !important;
        line-height: 1.25 !important;
    }

    .block-container h2 {
        font-size: 23px !important;
        margin-top: 20px !important;
        margin-bottom: 6px !important;
    }

    .block-container h3 {
        font-size: 19px !important;
        margin-top: 14px !important;
        margin-bottom: 6px !important;
    }

    /* Supporting text under chart titles */
    .block-container h2 + p,
    .block-container h3 + p {
        color: #718198 !important;
        font-size: 13px !important;
        line-height: 1.5 !important;
    }

    /* Premium blue accents */
    :root {
        --eo-navy: #102844;
        --eo-blue: #2369A8;
        --eo-teal: #278C87;
        --eo-amber: #B88735;
    }
    </style>
    """, unsafe_allow_html=True)

    # HEADER — replace the generic blue info banner with a compact
    # title area and a quieter synthetic-data disclosure.
    st.markdown("""
    <div class="eo-header">
        <div>
            <h1 class="eo-title">Executive Overview</h1>
            <div class="eo-subtitle">
                Distribution performance · Target delivery · Partner contribution
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CURRENT PERIOD — use existing sidebar selections.
    start_p = pd.Period(period_start_key, freq="M")
    end_p = pd.Period(period_end_key, freq="M")
    period_length = end_p.ordinal - start_p.ordinal + 1

    st.markdown(f"""
    <div class="eo-context">
      <div class="eo-context-item">
        <div class="eo-context-label">Reporting period</div>
        <div class="eo-context-value">
          {start_p.strftime("%b %Y")} – {end_p.strftime("%b %Y")}
        </div>
      </div>
      <div class="eo-context-item">
        <div class="eo-context-label">Partner scope</div>
        <div class="eo-context-value">{partner}</div>
      </div>
      <div class="eo-context-item">
        <div class="eo-context-label">Channel scope</div>
        <div class="eo-context-value">{channel}</div>
      </div>
      <div class="eo-context-item">
        <div class="eo-context-label">Attention threshold</div>
        <div class="eo-context-value">{threshold:.0%}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI calculations — use the filtered dataframe.
    actual = float(df["premium_actual_idr"].sum())
    target = float(df["premium_target_idr"].sum())
    gap_value = target - actual
    attainment = actual / target if target > 0 else None
    active_partners = int(df["partner"].nunique())
    policies = int(df["policies_issued"].sum())

    # Comparisons are calculated from the full dataset with the same
    # partner/channel filters, but with the relevant comparison window.
    all_months = sorted(
        data["month"].dt.to_period("M").astype(str).unique().tolist()
    )

    def filtered_comparison(start_period, end_period):
        start_period = pd.Period(start_period, freq="M")
        end_period = pd.Period(end_period, freq="M")

        # Reject invalid comparison windows.
        if start_period > end_period:
            return None

        comp = _month_window(
            data,
            start_period,
            end_period,
        )

        # Apply the same scope as the selected reporting period.
        if partner != "All partners":
            comp = comp[comp["partner"] == partner]

        if channel != "All channels":
            comp = comp[comp["channel"] == channel]

        if comp.empty:
            return None

        # Confirm every calendar month has records in this scope.
        expected_months = {
            str(month)
            for month in pd.period_range(
                start_period,
                end_period,
                freq="M",
            )
        }

        observed_months = set(
            comp["month"]
            .dt.to_period("M")
            .astype(str)
            .unique()
        )

        if not expected_months.issubset(observed_months):
            return None

        return _comparison_summary(comp)

    pp_end = start_p - 1
    pp_start = pp_end - (period_length - 1)
    py_start = start_p - 12
    py_end = end_p - 12

    previous_period = filtered_comparison(pp_start, pp_end)
    previous_year = filtered_comparison(py_start, py_end)
    # Explain unavailable comparisons instead of leaving N/A unexplained.
    comparison_notes = []

    if previous_period is None:
        comparison_notes.append(
            "Previous Period is unavailable because the full "
            "comparison window is outside the available data history."
        )

    if previous_year is None:
        comparison_notes.append(
            "Previous Year is unavailable because the equivalent "
            "comparison window is incomplete."
        )

    if comparison_notes:
        st.caption(
            "Comparison note: " + " ".join(comparison_notes)
        )

    current_summary = {
        "actual": actual,
        "target": target,
        "attainment": attainment,
        "gap": gap_value,
        "partners": active_partners,
    }

    def comparison_text(current, previous, metric):
        if previous is None:
            return "N/A"

        c = current.get(metric)
        p = previous.get(metric)

        if c is None or p is None:
            return "N/A"

        if metric == "attainment":
            return f"{(c - p) * 100:+.1f} pp"

        if metric == "gap":
            if c == p:
                return "No change"
            direction = "narrowed" if c < p else "widened"
            return f"Gap {direction} · {money(abs(p - c))}"

        if p == 0:
            return "N/A"

        return f"{(c / p - 1) * 100:+.1f}%"

    def render_kpi(label, value, note, metric):
        pp = comparison_text(
            current_summary, previous_period, metric
        )
        py = comparison_text(
            current_summary, previous_year, metric
        )

        return f"""
        <div class="eo-kpi">
          <div class="eo-kpi-label">{label}</div>
          <div class="eo-kpi-value-row">
            <div class="eo-kpi-value">{value}</div>
          </div>
          <div class="eo-kpi-note">{note}</div>
          <div class="eo-kpi-comparison">
            <span>Previous Period</span><strong>{pp}</strong>
          </div>
          <div class="eo-kpi-comparison">
            <span>Previous Year</span><strong>{py}</strong>
          </div>
        </div>
        """

    st.markdown(
        '<div class="eo-section-heading">Portfolio performance</div>',
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4, gap="medium")

    with k1:
        st.markdown(render_kpi(
            "Total Premium",
            money(actual),
            "Total actual premium in the selected period.",
            "actual",
        ), unsafe_allow_html=True)

    with k2:
        st.markdown(render_kpi(
            "Target Attainment",
            f"{attainment:.1%}" if attainment is not None else "N/A",
            "Actual premium as a share of target.",
            "attainment",
        ), unsafe_allow_html=True)

    with k3:
        gap_label = (
            "Shortfall" if gap_value > 0
            else "Surplus" if gap_value < 0
            else "Target achieved"
        )
        st.markdown(render_kpi(
            "Premium Gap",
            money(abs(gap_value)),
            gap_label,
            "gap",
        ), unsafe_allow_html=True)

    with k4:
        st.markdown(render_kpi(
            "Active Partners",
            f"{active_partners:,}",
            f"{policies:,} policies issued in the selected period.",
            "partners",
        ), unsafe_allow_html=True)

    # One concise portfolio-level signal. No oversized Streamlit banner.
    if target <= 0:
        signal_text = (
            "Target premium is zero for this selection. "
            "Attainment cannot be calculated."
        )
        signal_class = ""
        signal_label = "DATA NOTE"
    elif gap_value > 0:
        signal_text = (
            f"Attainment is {attainment:.1%}, leaving "
            f"{money(gap_value)} below target. Review the partner "
            f"exceptions and channel contribution below."
        )
        signal_class = ""
        signal_label = "MANAGEMENT SIGNAL"
    elif gap_value < 0:
        signal_text = (
            f"Portfolio is above target by {money(abs(gap_value))}. "
            f"Review which channels and partners are contributing most."
        )
        signal_class = "good"
        signal_label = "PORTFOLIO SIGNAL"
    else:
        signal_text = (
            "Portfolio has achieved its premium target for this selection."
        )
        signal_class = "good"
        signal_label = "PORTFOLIO SIGNAL"

    st.markdown(
        f'<div class="eo-signal {signal_class}">'
        f'<span class="eo-signal-label">{signal_label}</span>'
        f'<span>{signal_text}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Continue with the existing section beginning:
    # # Trend and channel attainment
    # =========================================================
    # CHARTS — executive-focused visual refinement
    # =========================================================
    left, right = st.columns([1.5, 1], gap="medium")

    # Monthly premium trend
    trend_view = (
        df.assign(
            month=df["month"].dt.to_period("M").dt.to_timestamp()
        )
        .groupby("month", as_index=False)
        .agg(
            actual_premium=("premium_actual_idr", "sum"),
            target_premium=("premium_target_idr", "sum"),
        )
        .sort_values("month")
    )

    with left:
        st.markdown(
            '<div class="exec-panel-title">Premium vs Target</div>'
            '<div class="exec-panel-sub">'
            'Monthly premium delivery against target.'
            '</div>',
            unsafe_allow_html=True,
        )

        if not trend_view.empty:
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=trend_view["month"],
                y=trend_view["actual_premium"],
                name="Actual Premium",
                mode="lines+markers",
                line=dict(color="#15EEF", width=3.2),
                marker=dict(size=5, color="#1769AA"),
                hovertemplate=(
                    "%{x|%b %Y}<br>"
                    "Actual: Rp %{y:,.0f}<extra></extra>"
                ),
            ))

            fig.add_trace(go.Scatter(
                x=trend_view["month"],
                y=trend_view["target_premium"],
                name="Target Premium",
                mode="lines+markers",
                line=dict(color="#AAB8CA", width=2, dash="dot"),
                marker=dict(size=4, color="#A7BED9"),
                hovertemplate=(
                    "%{x|%b %Y}<br>"
                    "Target: Rp %{y:,.0f}<extra></extra>"
                ),
            ))

            # Keep month labels readable for short and long periods.
            month_count = len(trend_view)
            tick_interval = 1 if month_count <= 8 else (
                2 if month_count <= 18 else 3
            )

            fig.update_xaxes(
                title=None,
                tickformat="%b\n%Y",
                dtick=f"M{tick_interval}",
                showgrid=False,
                showline=True,
                linecolor="#E4EBF3",
                tickfont=dict(size=10, color="#73849A"),
                automargin=True,
            )

            fig.update_yaxes(
                title=None,
                tickprefix="Rp ",
                tickformat="~s",
                rangemode="tozero",
                gridcolor="#EDF2F7",
                zeroline=False,
                tickfont=dict(size=10, color="#73849A"),
                automargin=True,
            )

            fig.update_layout(
                height=320,
                margin=dict(l=12, r=16, t=38, b=8),
                paper_bgcolor="white",
                plot_bgcolor="white",
                hovermode="x unified",
                font=dict(
                    family="Arial, sans-serif",
                    size=11,
                    color="#526680",
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="left",
                    x=0,
                    font=dict(size=10),
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )
        else:
            st.info("No monthly trend is available for this selection.")

    # Channel target attainment
    channel_view = (
        df.groupby("channel", as_index=False)
        .agg(
            actual_premium=("premium_actual_idr", "sum"),
            target_premium=("premium_target_idr", "sum"),
        )
    )

    channel_view["attainment"] = (
        channel_view["actual_premium"]
        / channel_view["target_premium"].where(
            channel_view["target_premium"] > 0
        )
    )

    channel_view = (
        channel_view.dropna(subset=["attainment"])
        .sort_values("attainment", ascending=False)
    )

    with right:
        st.markdown(
            '<div class="exec-panel-title">Channel Target Attainment</div>'
            '<div class="exec-panel-sub">'
            'Actual premium relative to the 100% target benchmark.'
            '</div>',
            unsafe_allow_html=True,
        )

        if not channel_view.empty:
            # Reserve space beyond the longest bar for percentage labels.
            max_attainment = float(channel_view["attainment"].max())
            axis_max = max(1.12, max_attainment * 1.16)

            bar_colors = [
                "#16856B" if value >= 1.0 else
                "#155EEF" if value >= threshold else
                "#D99A2B"
                for value in channel_view["attainment"]
            ]

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=channel_view["attainment"],
                y=channel_view["channel"],
                orientation="h",
                marker=dict(
                    color=bar_colors,
                    line=dict(width=0),
                ),
                text=[
                    f"{value:.1%}"
                    for value in channel_view["attainment"]
                ],
                textposition="outside",
                textfont=dict(size=10, color="#344D6B"),
                cliponaxis=False,
                hovertemplate=(
                    "%{y}<br>Attainment: %{x:.1%}<extra></extra>"
                ),
            ))

            # 100% target reference
            fig.add_vline(
                x=1.0,
                line_dash="dash",
                line_color="#667D98",
                line_width=1.4,
            )

            fig.update_xaxes(
                title=None,
                tickformat=".0%",
                range=[0, axis_max],
                gridcolor="#EDF2F7",
                zeroline=False,
                tickfont=dict(size=9, color="#73849A"),
                automargin=True,
            )

            fig.update_yaxes(
                title=None,
                autorange="reversed",
                showgrid=False,
                tickfont=dict(size=10, color="#526680"),
                automargin=True,
            )

            fig.update_layout(
                height=320,
                showlegend=False,
                margin=dict(l=8, r=38, t=20, b=10),
                paper_bgcolor="white",
                plot_bgcolor="white",
                bargap=0.36,
                font=dict(
                    family="Arial, sans-serif",
                    size=10,
                    color="#526680",
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )
        else:
            st.info(
                "Channel attainment is unavailable because "
                "no positive targets exist in this selection."
            )

    # =========================================================
    # PARTNER DECISION INTELLIGENCE
    # Contribution ranking vs shortfall priority
    # =========================================================
    partner_view = (
        df.groupby("partner", as_index=False)
        .agg(
            premium_actual_idr=("premium_actual_idr", "sum"),
            premium_target_idr=("premium_target_idr", "sum"),
            policies_issued=("policies_issued", "sum"),
        )
    )

    portfolio_actual = partner_view["premium_actual_idr"].sum()

    partner_view["contribution_share"] = (
        partner_view["premium_actual_idr"] / portfolio_actual
        if portfolio_actual > 0
        else 0.0
    )

    partner_view["attainment_rate"] = (
        partner_view["premium_actual_idr"]
        / partner_view["premium_target_idr"].where(
            partner_view["premium_target_idr"] > 0
        )
    )

    # Positive = shortfall; negative = above target.
    partner_view["gap_to_target"] = (
        partner_view["premium_target_idr"]
        - partner_view["premium_actual_idr"]
    )

    partner_view["status"] = partner_view["attainment_rate"].apply(
        lambda value: (
            "Above target" if pd.notna(value) and value >= 1
            else "On track" if pd.notna(value) and value >= threshold
            else "Needs attention" if pd.notna(value)
            else "Target unavailable"
        )
    )

    # Rank only by actual premium contribution.
    top = (
        partner_view.sort_values(
            "premium_actual_idr", ascending=False
        )
        .head(5)
        .copy()
        .reset_index(drop=True)
    )

    # Attention queue: below threshold, with the largest absolute
    # shortfall first. This is a review priority, not a causal score.
    attention = (
        partner_view[
            (partner_view["attainment_rate"] < threshold)
            & (partner_view["gap_to_target"] > 0)
        ]
        .sort_values(
            ["gap_to_target", "attainment_rate"],
            ascending=[False, True],
        )
        .head(5)
        .copy()
    )

    table_left, table_right = st.columns([1.2, 1], gap="medium")

    with table_left:
        st.markdown(
            '<div class="exec-panel-title">Top Partners</div>'
            '<div class="exec-panel-sub">'
            'Ranked by actual premium. Contribution shows each partner’s '
            'share of selected portfolio premium.'
            '</div>',
            unsafe_allow_html=True,
        )

        if not top.empty:
            top.insert(0, "Rank", range(1, len(top) + 1))
            top["Actual Premium"] = top["premium_actual_idr"].map(money)
            top["Contribution"] = top["contribution_share"].map(
                lambda value: f"{value:.1%}"
            )
            top["Attainment"] = top["attainment_rate"].map(
                lambda value: f"{value:.1%}"
                if pd.notna(value) else "N/A"
            )

            st.dataframe(
                top[
                    [
                        "Rank", "partner", "Actual Premium",
                        "Contribution", "Attainment", "status",
                    ]
                ].rename(columns={
                    "partner": "Partner",
                    "status": "Status",
                }),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Rank": st.column_config.NumberColumn(
                        "Rank", width="small"
                    ),
                    "Partner": st.column_config.TextColumn(
                        "Partner", width="medium"
                    ),
                    "Actual Premium": st.column_config.TextColumn(
                        "Actual Premium", width="medium"
                    ),
                    "Contribution": st.column_config.TextColumn(
                        "Contribution", width="small"
                    ),
                    "Attainment": st.column_config.TextColumn(
                        "Attainment", width="small"
                    ),
                    "Status": st.column_config.TextColumn(
                        "Status", width="medium"
                    ),
                },
            )
        else:
            st.info("No partner records in this selection.")

    with table_right:
        st.markdown(
            f'<div class="exec-panel-title">Shortfall Priority</div>'
            f'<div class="exec-panel-sub">'
            f'Partners below {threshold:.0%} attainment, ordered by '
            f'largest premium shortfall.'
            f'</div>',
            unsafe_allow_html=True,
        )

        if not attention.empty:
            attention_display = attention.copy()
            attention_display["Attainment"] = (
                attention_display["attainment_rate"].map(
                    lambda value: f"{value:.1%}"
                    if pd.notna(value) else "N/A"
                )
            )
            attention_display["Premium Shortfall"] = (
                attention_display["gap_to_target"].map(money)
            )
            attention_display["Portfolio Share"] = (
                attention_display["contribution_share"].map(
                    lambda value: f"{value:.1%}"
                )
            )

            st.dataframe(
                attention_display[
                    [
                        "partner", "Attainment",
                        "Premium Shortfall", "Portfolio Share",
                    ]
                ].rename(columns={"partner": "Partner"}),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Partner": st.column_config.TextColumn(
                        "Partner", width="medium"
                    ),
                    "Attainment": st.column_config.TextColumn(
                        "Attainment", width="small"
                    ),
                    "Premium Shortfall": st.column_config.TextColumn(
                        "Premium Shortfall", width="medium"
                    ),
                    "Portfolio Share": st.column_config.TextColumn(
                        "Portfolio Share", width="small"
                    ),
                },
            )
        else:
            st.success(
                "No partner has both below-threshold attainment "
                "and a positive premium shortfall in this selection."
            )

    # =========================================================
    # DECISION LAYER — insights and action queue
    # =========================================================
    insight_col, action_col = st.columns([1, 1.15], gap="medium")

    with insight_col:
        st.markdown(
            '<div class="exec-panel-title">Key Insights</div>'
            '<div class="exec-panel-sub">'
            'The most decision-relevant signals in this selection.'
            '</div>',
            unsafe_allow_html=True,
        )

        # Identify the leading partner by portfolio contribution.
        leading_partner = (
            top.iloc[0] if not top.empty else None
        )

        if attainment is None:
            portfolio_body = (
                "Target is unavailable; portfolio attainment "
                "cannot be assessed."
            )
        elif gap_value > 0:
            portfolio_body = (
                f"Premium is {money(gap_value)} below target "
                f"({attainment:.1%} attainment)."
            )
        elif gap_value < 0:
            portfolio_body = (
                f"Premium is {money(abs(gap_value))} above target "
                f"({attainment:.1%} attainment)."
            )
        else:
            portfolio_body = (
                "Portfolio premium exactly meets target."
            )

        if leading_partner is not None:
            leading_body = (
                f"{leading_partner['partner']} contributes "
                f"{leading_partner['contribution_share']:.1%} "
                f"of portfolio premium, with "
                f"{leading_partner['attainment_rate']:.1%} "
                f"attainment."
                if pd.notna(leading_partner["attainment_rate"])
                else (
                    f"{leading_partner['partner']} contributes "
                    f"{leading_partner['contribution_share']:.1%} "
                    "of portfolio premium; target attainment is unavailable."
                )
            )
        else:
            leading_body = "No partner records in this selection."

        if not attention.empty:
            priority_partner = attention.iloc[0]
            attention_body = (
                f"{len(attention)} partner(s) are below the "
                f"{threshold:.0%} threshold. Largest shortfall: "
                f"{priority_partner['partner']} at "
                f"{money(priority_partner['gap_to_target'])}."
            )
        else:
            attention_body = (
                "No partner meets both the below-threshold "
                "and positive-shortfall criteria."
            )

        insight_items = [
            ("01", "Portfolio delivery", portfolio_body),
            ("02", "Contribution leader", leading_body),
            ("03", "Shortfall priority", attention_body),
        ]

        for number, title, body in insight_items:
            st.markdown(
                f"""
                <div class="exec-insight" style="margin-bottom:8px;">
                  <div style="display:flex;gap:10px;align-items:flex-start;">
                    <div style="
                        background:#eaf2fb;color:#245d96;
                        border-radius:7px;padding:5px 7px;
                        font-size:10px;font-weight:800;">
                      {number}
                    </div>
                    <div style="flex:1;">
                      <div class="exec-insight-title">{title}</div>
                      <div class="exec-insight-body">{body}</div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with action_col:
        st.markdown(
            '<div class="exec-panel-title">Recommended Actions</div>'
            '<div class="exec-panel-sub">'
            'Rule-based review prompts. Validate the underlying data '
            'before taking action.'
            '</div>',
            unsafe_allow_html=True,
        )

        if actions:
            action_df = pd.DataFrame(actions)

            # Keep only fields available in the existing action records.
            preferred = [
                c for c in [
                    "priority", "partner", "signal",
                    "suggested_action", "basis"
                ]
                if c in action_df.columns
            ]
            action_df = action_df[preferred].copy()

            if "suggested_action" not in action_df.columns:
                action_df["suggested_action"] = (
                    "Review partner performance and validate source data."
                )
            if "partner" not in action_df.columns:
                action_df["partner"] = "Portfolio"
            if "signal" not in action_df.columns:
                action_df["signal"] = "Management review"
            if "priority" not in action_df.columns:
                action_df["priority"] = "Review"

            # Rank actions by priority, then consolidate by partner.
            priority_rank = {
                "critical": 0,
                "high": 1,
                "medium": 2,
                "low": 3,
            }

            action_df["_rank"] = (
                action_df["priority"].astype(str).str.lower()
                .map(priority_rank).fillna(4)
            )

            action_df["_action_key"] = (
                action_df["suggested_action"]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            action_df["_rank"] = (
                action_df["priority"].astype(str).str.lower()
                .map(priority_rank).fillna(4)
            )

            # Financial impact: positive shortfall only.
            shortfall_by_partner = (
                partner_view.set_index("partner")["gap_to_target"]
                .clip(lower=0)
                .to_dict()
            )

            action_df["_shortfall"] = (
                action_df["partner"]
                .map(shortfall_by_partner)
                .fillna(0.0)
            )

            action_df["_action_key"] = (
                action_df["suggested_action"]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            action_df = (
                action_df[action_df["_action_key"].ne("")]
                .sort_values(
                    ["_rank", "_shortfall"],
                    ascending=[True, False],
                )
            )

            consolidated = []

            for partner_name, group in action_df.groupby(
                "partner", sort=False
            ):
                first = group.iloc[0]

                signals = (
                    group["signal"].fillna("")
                    .astype(str).str.strip()
                )
                signals = signals[signals.ne("")].drop_duplicates().tolist()

                bases = (
                    group["basis"].fillna("").astype(str).str.strip()
                    if "basis" in group.columns
                    else pd.Series(dtype=str)
                )
                bases = bases[bases.ne("")].drop_duplicates().tolist()

                recommended_actions = (
                    group["_action_key"].drop_duplicates().tolist()
                )

                consolidated.append({
                    "priority": first["priority"],
                    "partners": [str(partner_name)],
                    "signals": signals,
                    "actions": recommended_actions,
                    "basis": bases,
                    "_rank": int(group["_rank"].min()),
                    "_shortfall": float(
                        group["_shortfall"].max()
                    ),
                })

            consolidated.sort(
                key=lambda item: (
                    item["_rank"],
                    -item["_shortfall"],
                )
            )
            consolidated = consolidated[:3]

            if consolidated:
                for i, item in enumerate(consolidated, start=1):
                    priority = str(item["priority"]).title()

                    partner_names = item["partners"]
                    if len(partner_names) <= 2:
                        partner_label = ", ".join(partner_names)
                    else:
                        partner_label = (
                            ", ".join(partner_names[:2])
                            + f" +{len(partner_names) - 2} more"
                        )

                    signal_label = item["signals"][0] if item["signals"] else (
                        "Management review"
                    )
                    basis_items = item.get("basis", [])

                    primary_basis = (
                        basis_items[:1]
                        if basis_items else []
                    )
                    additional_basis = basis_items[1:]

                    primary_basis_html = "".join(
                        f'<li style="margin-bottom:4px;">{basis}</li>'
                        for basis in primary_basis
                    )

                    additional_basis_html = "".join(
                        f'<li style="margin-bottom:4px;">{basis}</li>'
                        for basis in additional_basis
                    )

                    additional_section_html = ""
                    if additional_basis:
                        additional_section_html = (
                            '<div style="color:#405874;font-size:11px;font-weight:700;line-height:1.5;margin-top:7px;margin-bottom:4px;">'
                        'Additional signals'
                            '</div>'
                            '<ul style="padding-left:16px;margin:4px 0 0 0;">'
                            f'{additional_basis_html}'
                            '</ul>'
                        )
                    if len(item["signals"]) > 1:
                        signal_label += (
                            f" · {len(item['signals'])} related signals"
                        )

                    # Compact, consistent priority treatment.
                    if priority in ("High", "Critical"):
                        badge_bg, badge_fg = "#fff0ef", "#a94442"
                    elif priority == "Medium":
                        badge_bg, badge_fg = "#fff7e5", "#8a641b"
                    else:
                        badge_bg, badge_fg = "#edf4fc", "#376a9e"
                    action_list_html = "".join(
                        f'<li style="margin-bottom:6px;">{action}</li>'
                        for action in item["actions"]
                    )
                    st.markdown(
                        f"""
                        <div style="
                            border:1px solid #e2eaf3;
                            border-radius:10px;
                            padding:12px 13px;
                            margin-bottom:9px;
                            background:#ffffff;">
                          <div style="
                              display:flex;
                              align-items:center;
                              justify-content:space-between;
                              gap:8px;
                              margin-bottom:7px;">
                            <span style="
                                font-size:10px;
                                font-weight:800;
                                color:#8291a5;
                                letter-spacing:.08em;">
                              ACTION {i:02d}
                            </span>
                            <span style="
                                background:{badge_bg};
                                color:{badge_fg};
                                border-radius:5px;
                                padding:4px 7px;
                                font-size:9px;
                                font-weight:800;">
                              {priority}
                            </span>
                          </div>
                          <div style="
                              color:#193655;
                              font-size:12px;
                              font-weight:800;
                              line-height:1.45;
                              margin-bottom:5px;">
                            {partner_label}
                          </div>
                          <div style="
                              color:#73849a;
                              font-size:10px;
                              line-height:1.5;
                              margin-bottom:7px;">
                            {signal_label}
                          </div>
                          <div style="
                              color:#8291a5;
                              font-size:10px;
                              line-height:1.5;
                              margin-bottom:8px;">
                            <strong style="color:#405874;font-size:11px;font-weight:700;line-height:1.5;">Primary driver</strong>
                            <ul style="padding-left:16px;margin:4px 0 0 0;">
                              {primary_basis_html}
                            </ul>
                            {additional_section_html}
                          </div>
                          <div style="
                              border-top:1px solid #e8edf3;
                              margin-top:12px;
                              padding-top:10px;
                              color:#405874;
                              font-size:11px;
                              line-height:1.6;">
                            <div style="
                                color:#193655;
                                font-size:11px;
                                font-weight:800;
                                margin-bottom:7px;">
                              Recommended actions
                            </div>
                            <ol style="padding-left:18px;margin:0;">
                              {action_list_html}
                            </ol>
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No actionable recommendations are available.")
        else:
            st.info("No rule-based actions were triggered for this selection.")

    with st.expander("Data transparency and definitions"):
        st.markdown("""
        - *Actual premium:* sum of premium in the filtered dataset.
        - *Target attainment:* actual premium divided by target premium.
        - *Premium gap:* target minus actual; positive means shortfall.
        - *Partner attention:* partner attainment below the selected threshold.
        - *Recommended actions:* rule-based prompts, not proof of cause.
        - *Data status:* synthetic demonstration data only.
        """)
        export_df = df.copy()
        export_df["month"] = export_df["month"].dt.strftime("%Y-%m-%d")
        st.download_button(
            "Download filtered data (CSV)",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name="distribution_overview_filtered.csv",
            mime="text/csv",
            use_container_width=True,
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
