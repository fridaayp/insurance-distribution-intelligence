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
        "Portfolio performance, target delivery, partner contribution, "
        "and management priorities."
    )

    st.markdown("""
    <style>
    .block-container {padding-top:1.25rem;padding-bottom:2rem}
    .exec-label {font-size:10px;font-weight:800;letter-spacing:.10em;
        color:#6b7f98;text-transform:uppercase;margin-bottom:8px}
    .exec-card {background:#fff;border:1px solid #e2eaf3;border-radius:14px;
        padding:17px 17px 12px;box-shadow:0 3px 12px rgba(16,35,63,.035);
        min-height:145px}
    .exec-value {font-size:clamp(23px,2vw,31px);font-weight:800;
        letter-spacing:-.04em;color:#102844;line-height:1.2;margin:8px 0 12px}
    .exec-note {font-size:11px;color:#73849a;line-height:1.5}
    .exec-compare {display:flex;justify-content:space-between;gap:8px;
        border-top:1px solid #edf1f6;padding-top:7px;margin-top:7px;
        font-size:10px;color:#71829a}
    .exec-compare strong {color:#344d6b;font-size:10px}
    .exec-panel {background:#fff;border:1px solid #e2eaf3;border-radius:14px;
        padding:15px;box-shadow:0 3px 12px rgba(16,35,63,.025);margin-bottom:8px}
    .exec-panel-title {font-size:15px;font-weight:800;color:#142d4b}
    .exec-panel-sub {font-size:11px;color:#71829a;margin:4px 0 12px;line-height:1.5}
    .exec-callout {padding:12px 15px;border:1px solid #f0dfb3;
        background:#fff9eb;color:#79571d;border-radius:11px;
        font-size:12px;line-height:1.6;margin:10px 0 15px}
    .exec-insight {border:1px solid #e5ecf4;background:#fbfdff;
        padding:13px;border-radius:11px;min-height:110px}
    .exec-insight-title {font-size:12px;font-weight:800;color:#193655;margin-bottom:7px}
    .exec-insight-body {font-size:11px;line-height:1.6;color:#5d7189}
    [data-testid="stPlotlyChart"] {border:1px solid #e4ebf3;
        border-radius:12px;background:#fff;padding:4px}
    [data-testid="stDataFrame"] {border:1px solid #e2eaf3;border-radius:10px}
    </style>
    """, unsafe_allow_html=True)

    # Use the already-filtered dataframe: all KPIs and visuals stay consistent.
    actual = float(df["premium_actual_idr"].sum())
    target = float(df["premium_target_idr"].sum())
    gap_value = target - actual
    attainment = actual / target if target > 0 else None
    active_partners = int(df["partner"].nunique())
    policies = int(df["policies_issued"].sum())

    available_months = sorted(
        df["month"].dt.to_period("M").astype(str).unique().tolist()
    )
    start_p = pd.Period(period_start_key, freq="M")
    end_p = pd.Period(period_end_key, freq="M")
    period_length = end_p.ordinal - start_p.ordinal + 1

    # Previous period is the same number of calendar months immediately before.
    pp_end = start_p - 1
    pp_start = pp_end - (period_length - 1)
    all_months = sorted(
        data["month"].dt.to_period("M").astype(str).unique().tolist()
    )

    def filtered_comparison(start_period, end_period):
        if not _window_is_available(start_period, end_period, all_months):
            return None
        comp = _month_window(data, start_period, end_period)
        if partner != "All partners":
            comp = comp[comp["partner"] == partner]
        if channel != "All channels":
            comp = comp[comp["channel"] == channel]
        return _comparison_summary(comp)

    current_summary = {
        "actual": actual,
        "target": target,
        "attainment": attainment,
        "gap": gap_value,
        "partners": active_partners,
    }
    previous_period = filtered_comparison(pp_start, pp_end)

    # Previous year comparison uses the matching months one year earlier.
    py_start = start_p - 12
    py_end = end_p - 12
    previous_year = filtered_comparison(py_start, py_end)

    def comparison_text(current, previous, metric):
        if previous is None or previous.get(metric) is None or current.get(metric) is None:
            return "N/A"
        c, p = current[metric], previous[metric]
        if metric == "attainment":
            return f"{(c-p)*100:+.1f} pp"
        if metric == "gap":
            if c == p:
                return "No change"
            return f"{'Gap narrowed' if c < p else 'Gap widened'} · {money(abs(p-c))}"
        if p == 0:
            return "N/A"
        return f"{(c/p-1)*100:+.1f}%"

    def kpi_card(label, value, note, metric):
        pp = comparison_text(current_summary, previous_period, metric)
        py = comparison_text(current_summary, previous_year, metric)
        return f"""
        <div class="exec-card">
          <div class="exec-label">{label}</div>
          <div class="exec-value">{value}</div>
          <div class="exec-note">{note}</div>
          <div class="exec-compare"><span>vs Previous Period</span><strong>{pp}</strong></div>
          <div class="exec-compare"><span>vs Previous Year</span><strong>{py}</strong></div>
        </div>"""

    st.markdown(
        f'<div class="exec-label">Portfolio snapshot</div>'
        f'<div class="exec-note">Selected window: '
        f'{start_p.strftime("%b %Y")} – {end_p.strftime("%b %Y")} '
        f' · {partner} · {channel}</div>',
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4, gap="medium")
    with k1:
        st.markdown(kpi_card(
            "Total Premium", money(actual),
            "Total actual premium in the selected window.", "actual"
        ), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_card(
            "Target Attainment",
            f"{attainment:.1%}" if attainment is not None else "N/A",
            "Actual premium divided by target premium.", "attainment"
        ), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_card(
            "Premium Gap", money(abs(gap_value)),
            "Shortfall" if gap_value > 0 else (
                "Surplus" if gap_value < 0 else "Target achieved"
            ), "gap"
        ), unsafe_allow_html=True)
    with k4:
        st.markdown(kpi_card(
            "Active Partners", f"{active_partners:,}",
            f"{policies:,} policies issued.", "partners"
        ), unsafe_allow_html=True)

    if target > 0 and gap_value > 0:
        st.markdown(
            f'<div class="exec-callout"><b>Management signal</b> · '
            f'Portfolio attainment is {attainment:.1%}, leaving a '
            f'{money(gap_value)} premium shortfall against target. '
            f'Prioritize the largest addressable partner gaps.</div>',
            unsafe_allow_html=True,
        )
    elif target > 0:
        st.success(
            f"Portfolio is at or above target by {money(abs(gap_value))}."
            if gap_value < 0 else "Portfolio has achieved its premium target."
        )
    else:
        st.warning("Target is zero for this selection; attainment cannot be calculated.")

    # Trend and channel attainment
    left, right = st.columns([1.55, 1], gap="medium")
    trend_view = (
        df.groupby(df["month"].dt.to_period("M").dt.to_timestamp(), as_index=False)
        .agg(
            premium_actual_idr=("premium_actual_idr", "sum"),
            premium_target_idr=("premium_target_idr", "sum"),
        )
        .rename(columns={"month": "month"})
    )
    # The groupby timestamp column is named after the original Series; normalize it.
    if "month" not in trend_view.columns:
        trend_view = trend_view.rename(columns={trend_view.columns[0]: "month"})

    with left:
        st.markdown(
            '<div class="exec-panel-title">Premium vs target over time</div>'
            '<div class="exec-panel-sub">Monthly actual premium against target.</div>',
            unsafe_allow_html=True,
        )
        if not trend_view.empty:
            fig = px.line(
                trend_view, x="month",
                y=["premium_actual_idr", "premium_target_idr"],
                markers=True,
                color_discrete_map={
                    "premium_actual_idr": "#1769aa",
                    "premium_target_idr": "#9bbce0",
                },
                labels={
                    "month": "Month", "value": "Premium (IDR)",
                    "variable": "", "premium_actual_idr": "Actual premium",
                    "premium_target_idr": "Target premium",
                },
            )
            fig.update_traces(line=dict(width=2.5), marker=dict(size=5))
            fig.update_xaxes(tickformat="%b %Y", dtick="M2")
            fig.update_yaxes(tickprefix="Rp ", tickformat="~s", rangemode="tozero")
            fig.update_layout(hovermode="x unified", height=325)
            st.plotly_chart(style(fig, 325), use_container_width=True)
        else:
            st.info("No monthly trend is available for this selection.")

    channel_view = (
        df.groupby("channel", as_index=False)
        .agg(
            premium_actual_idr=("premium_actual_idr", "sum"),
            premium_target_idr=("premium_target_idr", "sum"),
        )
    )
    channel_view["attainment"] = (
        channel_view["premium_actual_idr"]
        / channel_view["premium_target_idr"].replace(0, float("nan"))
    )
    channel_view = channel_view.dropna(subset=["attainment"]).sort_values("attainment")

    with right:
        st.markdown(
            '<div class="exec-panel-title">Target attainment by channel</div>'
            '<div class="exec-panel-sub">Dashed line marks 100% of target.</div>',
            unsafe_allow_html=True,
        )
        if not channel_view.empty:
            fig = px.bar(
                channel_view, x="attainment", y="channel", orientation="h",
                text=channel_view["attainment"].map(lambda v: f"{v:.0%}"),
                labels={"attainment": "Target attainment", "channel": ""},
                color_discrete_sequence=["#347fc4"],
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            max_value = max(1.1, float(channel_view["attainment"].max()) * 1.15)
            fig.update_xaxes(tickformat=".0%", range=[0, max_value])
            fig.add_vline(x=1, line_dash="dash", line_color="#7c91ab", line_width=1.4)
            fig.update_layout(showlegend=False, height=325, margin=dict(l=8,r=30,t=20,b=12))
            st.plotly_chart(style(fig, 325), use_container_width=True)
        else:
            st.info("Channel attainment unavailable because target is zero.")

    # Partner ranking and review queue
    partner_view = (
        df.groupby("partner", as_index=False)
        .agg(
            premium_actual_idr=("premium_actual_idr", "sum"),
            premium_target_idr=("premium_target_idr", "sum"),
            policies_issued=("policies_issued", "sum"),
        )
    )
    partner_view["attainment_rate"] = (
        partner_view["premium_actual_idr"]
        / partner_view["premium_target_idr"].replace(0, float("nan"))
    )
    partner_view["gap_to_target"] = (
        partner_view["premium_target_idr"] - partner_view["premium_actual_idr"]
    )

    table_left, table_right = st.columns(2, gap="medium")
    with table_left:
        st.markdown(
            '<div class="exec-panel-title">Top partners by actual premium</div>'
            '<div class="exec-panel-sub">Ranked by premium contribution; attainment remains visible.</div>',
            unsafe_allow_html=True,
        )
        top = partner_view.nlargest(5, "premium_actual_idr").copy()
        if not top.empty:
            top["Rank"] = range(1, len(top)+1)
            top["Actual Premium"] = top["premium_actual_idr"].map(money)
            top["Attainment"] = top["attainment_rate"].map(
                lambda v: f"{v:.1%}" if pd.notna(v) else "N/A"
            )
            st.dataframe(
                top[["Rank", "partner", "Actual Premium", "Attainment"]].rename(
                    columns={"partner": "Partner"}
                ),
                use_container_width=True, hide_index=True,
                column_config={
                    "Rank": st.column_config.NumberColumn(width="small"),
                    "Partner": st.column_config.TextColumn(width="medium"),
                },
            )
        else:
            st.info("No partner records in this selection.")

    with table_right:
        st.markdown(
            f'<div class="exec-panel-title">Partners requiring attention</div>'
            f'<div class="exec-panel-sub">Attainment below {threshold:.0%}; review context before action.</div>',
            unsafe_allow_html=True,
        )
        attention = partner_view[
            partner_view["attainment_rate"] < threshold
        ].sort_values("attainment_rate", na_position="last").head(5).copy()
        if not attention.empty:
            attention["Attainment"] = attention["attainment_rate"].map(
                lambda v: f"{v:.1%}" if pd.notna(v) else "N/A"
            )
            attention["Gap to Target"] = attention["gap_to_target"].map(
                lambda v: money(v) if v >= 0 else f"{money(abs(v))} surplus"
            )
            st.dataframe(
                attention[["partner", "Attainment", "Gap to Target"]].rename(
                    columns={"partner": "Partner"}
                ),
                use_container_width=True, hide_index=True,
            )
        else:
            st.success("No partners are below the selected threshold.")

    # Separate observations from actions to avoid repeating the same message.
    insight_col, action_col = st.columns([1.05, 1], gap="medium")
    with insight_col:
        st.markdown(
            '<div class="exec-panel-title">Key Insights</div>'
            '<div class="exec-panel-sub">What the current selection tells us.</div>',
            unsafe_allow_html=True,
        )
        best_channel = (
            channel_view.sort_values("attainment", ascending=False).iloc[0]
            if not channel_view.empty else None
        )
        worst_partner = (
            attention.sort_values("attainment_rate", na_position="last").iloc[0]
            if not attention.empty else None
        )
        insight_cols = st.columns(2, gap="small")
        with insight_cols[0]:
            if attainment is not None:
                body = (
                    f"Premium is {money(gap_value)} below target."
                    if gap_value > 0 else "Premium target has been achieved."
                )
            else:
                body = "Target is unavailable for this selection."
            st.markdown(
                f'<div class="exec-insight"><div class="exec-insight-title">Portfolio delivery</div>'
                f'<div class="exec-insight-body">{body}</div></div>',
                unsafe_allow_html=True,
            )
        with insight_cols[1]:
            body = (
                f'{best_channel["channel"]} leads channel attainment at '
                f'{best_channel["attainment"]:.1%}.'
                if best_channel is not None else "No valid channel comparison is available."
            )
            st.markdown(
                f'<div class="exec-insight"><div class="exec-insight-title">Channel leader</div>'
                f'<div class="exec-insight-body">{body}</div></div>',
                unsafe_allow_html=True,
            )
        if worst_partner is not None:
            st.caption(
                f"Review signal: {worst_partner['partner']} has the lowest attainment "
                f"among partners below threshold ({worst_partner['attainment_rate']:.1%})."
            )

    with action_col:
        st.markdown(
            '<div class="exec-panel-title">Recommended Actions</div>'
            '<div class="exec-panel-sub">Rule-based prompts for management review, not causal conclusions.</div>',
            unsafe_allow_html=True,
        )
        if actions:
            action_df = pd.DataFrame(actions)
            cols = [c for c in ["priority", "partner", "signal", "suggested_action"] if c in action_df.columns]
            action_df = action_df[cols].head(5).rename(columns={
                "priority": "Priority", "partner": "Partner",
                "signal": "Signal", "suggested_action": "Recommended action",
            })
            st.dataframe(
                action_df, use_container_width=True, hide_index=True,
                column_config={
                    "Priority": st.column_config.TextColumn(width="small"),
                    "Partner": st.column_config.TextColumn(width="medium"),
                    "Signal": st.column_config.TextColumn(width="medium"),
                    "Recommended action": st.column_config.TextColumn(width="large"),
                },
            )
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
    # Keep the existing Performance Analysis block below this line unchanged.

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
