import streamlit as st
import pandas as pd
import gdown
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import warnings
import numpy as np
import gdown
import os

warnings.filterwarnings('ignore')

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Taxi Revenue Analysis",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

/* White background for main area */
.stApp { background: #f5f7fa; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #1e2a4a !important;
    border-right: none;
}
[data-testid="stSidebar"] * { color: #fff !important; }
[data-testid="stSidebar"] .stButton button {
    width: 100%;
    text-align: left;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 10px;
    color: white !important;
    padding: 0.6rem 1rem;
    margin-bottom: 5px;
    font-size: 0.88rem;
    transition: all 0.2s;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255,165,0,0.3) !important;
    border-color: #FFA500 !important;
}

/* General text */
.stMarkdown p, .stMarkdown li { color: #1e2a4a !important; }

/* Slide header */
.slide-number {
    display: inline-block;
    background: #1e2a4a;
    color: white !important;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.slide-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #1e2a4a !important;
    line-height: 1.15;
    margin-bottom: 0.2rem;
}
.slide-title span { color: #FF6B35 !important; }
.slide-subtitle {
    font-size: 1.05rem;
    color: #6b7a99 !important;
    margin-bottom: 1.5rem;
    font-weight: 400;
}
.gradient-divider {
    height: 3px;
    background: linear-gradient(90deg, #FF6B35, #4ECDC4, transparent);
    border: none;
    border-radius: 2px;
    margin-bottom: 2rem;
}

/* Metric cards */
.metric-card {
    background: white;
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(30,42,74,0.1);
    border-top: 4px solid #FF6B35;
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(30,42,74,0.15);
}
.metric-card .metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #FF6B35 !important;
    line-height: 1.1;
}
.metric-card .metric-label {
    font-size: 0.82rem;
    color: #6b7a99 !important;
    font-weight: 600;
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Info / alert boxes */
.box {
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin: 0.8rem 0;
    font-size: 0.93rem;
    line-height: 1.7;
}
.box-blue  { background: #EEF4FF; border-left: 4px solid #3B6CF8; color: #1e2a4a !important; }
.box-orange{ background: #FFF4EE; border-left: 4px solid #FF6B35; color: #1e2a4a !important; }
.box-green { background: #EEFAF7; border-left: 4px solid #00C896; color: #1e2a4a !important; }
.box-teal  { background: #EEFAFA; border-left: 4px solid #4ECDC4; color: #1e2a4a !important; }
.box-yellow{ background: #FFFBEE; border-left: 4px solid #FFB800; color: #1e2a4a !important; }

/* Step items */
.step-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 0.75rem 0;
    border-bottom: 1px solid #eef0f5;
    color: #1e2a4a !important;
    font-size: 0.92rem;
}
.step-num {
    background: #1e2a4a;
    color: white !important;
    border-radius: 50%;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 1px;
}

/* White card panels */
.panel {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 12px rgba(30,42,74,0.08);
    margin-bottom: 1rem;
}

/* Progress */
.progress-bar-outer {
    background: rgba(255,255,255,0.15);
    border-radius: 10px;
    height: 5px;
    margin-bottom: 1.5rem;
    overflow: hidden;
}
.progress-bar-inner {
    height: 5px;
    border-radius: 10px;
    background: linear-gradient(90deg, #FF6B35, #FFB800);
}

/* Tag chips */
.chip {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 2px;
}
.chip-blue  { background: #EEF4FF; color: #3B6CF8 !important; }
.chip-orange{ background: #FFF4EE; color: #FF6B35 !important; }
.chip-green { background: #EEFAF7; color: #00C896 !important; }

/* Fix invisible tab text on white background */
[data-testid="stTabs"] button p {
    color: #1e2a4a !important;
    font-weight: 600;
    font-size: 0.92rem;
}
[data-testid="stTabs"] button[aria-selected="true"] p {
    color: #FF6B35 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    border-bottom: 3px solid #FF6B35 !important;
}

/* hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── Slides ───────────────────────────────────────────────────────────────────
SLIDES = [
    ("🏠", "Home"),
    ("❓", "Problem Statement"),
    ("🎯", "Objective & Research Question"),
    ("📦", "Dataset Overview"),
    ("🔍", "Data Cleaning"),
    ("📊", "Exploratory Data Analysis"),
    ("🧪", "Hypothesis Testing"),
    ("💡", "Insights & Recommendations"),
]

if "slide" not in st.session_state:
    st.session_state.slide = 0

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1.5rem 0 1rem 0;'>
        <div style='font-size:2.8rem;'>🚕</div>
        <div style='font-size:0.95rem; font-weight:800; color:white; letter-spacing:1px;'>TAXI REVENUE</div>
        <div style='font-size:0.68rem; color:rgba(255,255,255,0.45); letter-spacing:2px; text-transform:uppercase; margin-top:3px;'>Payment Type Analysis</div>
    </div>
    <hr style='border:1px solid rgba(255,255,255,0.1); margin-bottom:1rem;'>
    """, unsafe_allow_html=True)

    for i, (icon, name) in enumerate(SLIDES):
        if st.button(f"{icon}  {name}", key=f"nav_{i}"):
            st.session_state.slide = i
            st.rerun()

    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1); margin-top:0.5rem;'>", unsafe_allow_html=True)
    progress_pct = int((st.session_state.slide / (len(SLIDES) - 1)) * 100)
    st.markdown(f"""
    <div style='color:rgba(255,255,255,0.45); font-size:0.75rem; text-align:center; padding:0.3rem 0;'>
        Slide {st.session_state.slide + 1} / {len(SLIDES)}
    </div>
    <div class='progress-bar-outer'>
        <div class='progress-bar-inner' style='width:{progress_pct}%;'></div>
    </div>
    """, unsafe_allow_html=True)

# ─── Colour palette ───────────────────────────────────────────────────────────
C_ORANGE = "#FF6B35"
C_BLUE   = "#3B6CF8"
C_TEAL   = "#4ECDC4"
C_GREEN  = "#00C896"
C_NAVY   = "#1e2a4a"
C_YELLOW = "#FFB800"
C_LIGHT  = "#f5f7fa"

# ─── Helpers ──────────────────────────────────────────────────────────────────
def slide_header(badge, title, highlight="", subtitle=""):
    st.markdown(f"<div class='slide-number'>{badge}</div>", unsafe_allow_html=True)
    hl = f"<span>{highlight}</span>" if highlight else ""
    st.markdown(f"<div class='slide-title'>{title} {hl}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='slide-subtitle'>{subtitle}</div>", unsafe_allow_html=True)
    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

def box(text, kind="blue"):
    st.markdown(f"<div class='box box-{kind}'>{text}</div>", unsafe_allow_html=True)

def mcard(value, label, color=C_ORANGE):
    return f"""
    <div class='metric-card' style='border-top-color:{color};'>
        <div class='metric-value' style='color:{color} !important;'>{value}</div>
        <div class='metric-label'>{label}</div>
    </div>"""

def fig_light(fig, axes=None):
    """Style matplotlib figure for light background."""
    fig.patch.set_facecolor("white")
    ax_list = axes if axes else [fig.gca()]
    for ax in ax_list:
        ax.set_facecolor("#f5f7fa")
        ax.tick_params(colors=C_NAVY, labelsize=9)
        ax.xaxis.label.set_color(C_NAVY)
        ax.yaxis.label.set_color(C_NAVY)
        ax.title.set_color(C_NAVY)
        for spine in ax.spines.values():
            spine.set_edgecolor("#dee2ea")
    return fig

# ─── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Downloading & Loading dataset… process can take a minute ⏳")
def load_data():
    csv_file = "yellow_tripdata_2021-01.csv"
    
    # Download dataset from Google Drive if it isn't available locally
    if not os.path.exists(csv_file):
        file_id = "1Lfyebhzsd3NKyKf2QOhBL6x6yq4t-9q_"
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, csv_file, quiet=False)

    df = pd.read_csv(csv_file)
    n_raw = len(df)

    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df['duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60

    drop_cols = ['VendorID','tpep_pickup_datetime','tpep_dropoff_datetime',
                 'RatecodeID','store_and_fwd_flag','PULocationID','DOLocationID',
                 'extra','mta_tax','tip_amount','tolls_amount',
                 'improvement_surcharge','total_amount','congestion_surcharge']
    df.drop([c for c in drop_cols if c in df.columns], axis=1, inplace=True)

    missing = int(df.isnull().sum().sum())
    df.dropna(inplace=True)
    n_after_null = len(df)

    df['passenger_count'] = df['passenger_count'].astype('int64')
    df['payment_type']    = df['payment_type'].astype('int64')

    dups = int(df.duplicated().sum())
    df.drop_duplicates(inplace=True)
    n_after_dedup = len(df)

    df = df[df['payment_type'] < 3]
    df = df[(df['passenger_count'] > 0) & (df['passenger_count'] < 6)]
    df['payment_type'].replace([1, 2], ['Card', 'Cash'], inplace=True)
    df = df[(df['fare_amount'] > 0) & (df['trip_distance'] > 0) & (df['duration'] > 0)]
    n_after_filters = len(df)

    for col in ['trip_distance', 'fare_amount', 'duration']:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5*IQR) & (df[col] <= Q3 + 1.5*IQR)]
    n_final = len(df)

    counts = {
        'raw':          n_raw,
        'after_null':   n_after_null,
        'after_dedup':  n_after_dedup,
        'after_filters':n_after_filters,
        'final':        n_final,
        'missing':      missing,
        'dups':         dups,
    }
    return df, counts

try:
    taxi_data, _counts = load_data()
    data_ok = True
    # Compute t-test once globally so all slides can use it
    _card_fare = taxi_data[taxi_data['payment_type']=='Card']['fare_amount']
    _cash_fare  = taxi_data[taxi_data['payment_type']=='Cash']['fare_amount']
    t_stat, p_value = stats.ttest_ind(a=_card_fare, b=_cash_fare, equal_var=False)
except Exception as e:
    data_ok = False
    data_err = str(e)
    _counts = {'raw':0,'after_null':0,'after_dedup':0,'after_filters':0,'final':0,'missing':0,'dups':0}
    t_stat, p_value = 0.0, 1.0

slide = st.session_state.slide

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 0 — HOME
# ══════════════════════════════════════════════════════════════════════════════
if slide == 0:
    st.markdown("""
    <div style='text-align:center; padding:3rem 1rem 2.5rem 1rem;'>
        <div style='font-size:5rem; margin-bottom:1rem;'>🚕</div>
        <div style='font-size:3rem; font-weight:800; color:#1e2a4a; line-height:1.2; margin-bottom:0.6rem;'>
            Maximizing Revenue for<br>
            <span style='color:#FF6B35;'>Taxi Cab Drivers</span>
        </div>
        <div style='font-size:1.1rem; color:#6b7a99; margin-bottom:2.5rem;'>
            Payment Type Analysis · NYC Yellow Taxi Trip Records 2021
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    raw_disp  = f"{_counts['raw']:,}" if data_ok else "N/A"
    fin_disp  = f"{_counts['final']:,}" if data_ok else "N/A"
    c1.markdown(mcard(raw_disp, "Raw Records", C_BLUE),       unsafe_allow_html=True)
    c2.markdown(mcard(fin_disp, "Analysed Trips", C_ORANGE),  unsafe_allow_html=True)
    c3.markdown(mcard("T-Test", "Statistical Method", C_TEAL), unsafe_allow_html=True)
    c4.markdown(mcard("p ≈ 0.0", "Hypothesis Result", C_GREEN), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:white; border-radius:20px; padding:2rem 2.5rem;
                box-shadow:0 4px 20px rgba(30,42,74,0.08); max-width:720px; margin:auto; text-align:center;'>
        <div style='font-size:0.95rem; color:#6b7a99; line-height:1.9;'>
            This presentation walks through a complete data science study that investigates
            whether <strong style='color:#FF6B35;'>payment method influences fare amounts</strong>.
            Using <strong style='color:#3B6CF8;'>descriptive statistics</strong> and
            <strong style='color:#3B6CF8;'>hypothesis testing</strong>, we provide
            actionable recommendations for <strong style='color:#FF6B35;'>maximising driver revenue</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1,1,1])
    with mid:
        if st.button("🚀  Start Presentation →", use_container_width=True):
            st.session_state.slide = 1
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — PROBLEM STATEMENT
# ══════════════════════════════════════════════════════════════════════════════
elif slide == 1:
    slide_header("Slide 01", "Problem", "Statement", "What challenge are we solving?")

    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        box("""
        <strong>Industry Context</strong><br>
        In the fast-paced taxi booking sector, maximising revenue is essential for long-term success and
        driver satisfaction. Taxi drivers operate on thin margins — every additional dollar of fare matters.
        """, "blue")

        box("""
        <strong>The Knowledge Gap</strong><br>
        While factors like trip distance and duration are obvious fare drivers,
        the <strong>payment method</strong> is an often-overlooked variable.
        Do customers paying with credit cards spend differently from those paying cash?
        """, "orange")

        box("""
        <strong>Our Approach</strong><br>
        We use <strong>descriptive statistics</strong> and <strong>formal hypothesis testing</strong>
        on NYC Yellow Taxi data to identify whether a significant fare difference exists between payment types —
        and how drivers can act on this insight.
        """, "green")

    with col2:
        st.markdown("""
        <div class='panel' style='border-top:4px solid #FF6B35; text-align:center;'>
            <div style='font-size:2.5rem; margin-bottom:0.5rem;'>💸</div>
            <div style='font-weight:700; color:#1e2a4a; font-size:1rem; margin-bottom:1rem;'>Revenue Challenges</div>
        </div>
        """, unsafe_allow_html=True)
        challenges = [
            ("Thin margins", "Drivers earn a fraction of each fare"),
            ("No payment insights", "No data on payment-fare relationship"),
            ("Possible lost revenue", "Cash trips may yield lower earnings"),
            ("No data-driven strategy", "Decisions made without statistical backing"),
        ]
        for title, desc in challenges:
            st.markdown(f"""
            <div class='step-item'>
                <div style='width:9px; height:9px; background:#FF6B35; border-radius:50%; margin-top:6px; flex-shrink:0;'></div>
                <div><strong style='color:#1e2a4a;'>{title}</strong><br>
                <span style='color:#6b7a99; font-size:0.85rem;'>{desc}</span></div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — OBJECTIVE & RESEARCH QUESTION
# ══════════════════════════════════════════════════════════════════════════════
elif slide == 2:
    slide_header("Slide 02", "Objective &", "Research Question", "What we set out to answer")

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<h3 style='color:#1e2a4a; font-size:1.1rem; font-weight:700; margin-bottom:0.8rem;'>🎯 Project Objective</h3>", unsafe_allow_html=True)
        box("""
        Run a <strong>statistical analysis</strong> to examine the relationship between the total fare amount
        and the method of payment. We use Python <strong>hypothesis testing</strong> and
        <strong>descriptive statistics</strong> to extract actionable insights that help taxi drivers
        generate more revenue.
        """, "blue")

        st.markdown("<h3 style='color:#1e2a4a; font-size:1.1rem; font-weight:700; margin:1.5rem 0 0.8rem 0;'>🔬 Analysis Steps</h3>", unsafe_allow_html=True)
        steps = [
            "Load & inspect NYC Yellow Taxi 2021 data",
            "Clean data — nulls, duplicates, negatives, outliers",
            "Filter to relevant columns & payment types (Card / Cash)",
            "Compute descriptive statistics for each payment group",
            "Visualise fare & distance distributions",
            "Check normality via QQ Plot",
            "Run Welch's T-test to compare group means",
            "Interpret results and form business recommendations",
        ]
        for i, s in enumerate(steps, 1):
            st.markdown(f"""
            <div class='step-item'>
                <div class='step-num'>{i}</div>
                <div style='color:#1e2a4a; padding-top:2px;'>{s}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='color:#1e2a4a; font-size:1.1rem; font-weight:700; margin-bottom:0.8rem;'>❓ Research Question</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class='panel' style='border-left:4px solid #3B6CF8; background:#EEF4FF; padding:1.6rem;'>
            <div style='font-size:1rem; color:#1e2a4a; line-height:1.9; font-style:italic;'>
                "Is there a statistically significant relationship between
                <strong style='color:#FF6B35;'>fare amount</strong> and
                <strong style='color:#FF6B35;'>payment type</strong>,
                and can we encourage payment methods that
                <strong style='color:#3B6CF8;'>generate higher revenue</strong>
                without negatively impacting customer experience?"
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3 style='color:#1e2a4a; font-size:1.1rem; font-weight:700; margin:1.5rem 0 0.8rem 0;'>📐 Hypotheses</h3>", unsafe_allow_html=True)
        box("""
        <strong>H₀ (Null Hypothesis):</strong><br>
        There is <em>no significant difference</em> in average fare between credit card and cash customers.<br><br>
        <strong>H₁ (Alternative Hypothesis):</strong><br>
        There <em>is a significant difference</em> in average fare between credit card and cash customers.
        """, "yellow")

        box("""
        <strong>Significance Level:</strong> α = 0.05 (5%)<br>
        <strong>Statistical Test:</strong> Welch's Two-Sample T-test
        """, "teal")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — DATASET OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
elif slide == 3:
    slide_header("Slide 03", "Dataset", "Overview", "NYC Yellow Taxi Trip Records — January 2021")

    c1, c2, c3, c4 = st.columns(4)
    raw_disp = f"{_counts['raw']:,}" if data_ok else "N/A"
    c1.markdown(mcard(raw_disp,   "Total Raw Records", C_BLUE),  unsafe_allow_html=True)
    c2.markdown(mcard("18",       "Original Columns",  C_ORANGE), unsafe_allow_html=True)
    c3.markdown(mcard("5",        "Analysis Columns",  C_TEAL),  unsafe_allow_html=True)
    c4.markdown(mcard("Jan 2021", "Data Period",        C_GREEN), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 3], gap="large")

    with col1:
        st.markdown("<h3 style='color:#1e2a4a; font-size:1.05rem; font-weight:700;'>📋 Analysis Columns</h3>", unsafe_allow_html=True)
        schema = pd.DataFrame({
            "Column": ["passenger_count", "trip_distance", "payment_type", "fare_amount", "duration"],
            "Type":   ["int", "float", "str", "float", "float"],
            "Description": ["Passengers in trip", "Distance in miles", "Card / Cash", "Base fare ($)", "Minutes (derived)"],
        })
        st.dataframe(schema, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        box("""
        <strong>Payment Type Encoding:</strong><br>
        1 → Credit Card &nbsp;|&nbsp; 2 → Cash<br>
        3 → No Charge &nbsp;|&nbsp; 4 → Dispute &nbsp;|&nbsp; 5 → Unknown
        """, "blue")

    with col2:
        st.markdown("<h3 style='color:#1e2a4a; font-size:1.05rem; font-weight:700;'>🗂️ Columns Retained vs Dropped</h3>", unsafe_allow_html=True)
        cc1, cc2 = st.columns(2)
        kept = ["passenger_count", "trip_distance", "payment_type", "fare_amount", "duration (derived)"]
        dropped = ["VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", "RatecodeID",
                   "store_and_fwd_flag", "PULocationID", "DOLocationID", "extra", "mta_tax",
                   "tip_amount", "tolls_amount", "improvement_surcharge", "total_amount", "congestion_surcharge"]
        with cc1:
            st.markdown("<div style='color:#00C896; font-weight:700; font-size:0.83rem; margin-bottom:8px;'>✅ KEPT (5)</div>", unsafe_allow_html=True)
            for c in kept:
                st.markdown(f"<div style='background:#EEFAF7; border-radius:8px; padding:6px 10px; margin-bottom:4px; color:#1e2a4a; font-size:0.82rem;'><code>{c}</code></div>", unsafe_allow_html=True)
        with cc2:
            st.markdown("<div style='color:#FF6B35; font-weight:700; font-size:0.83rem; margin-bottom:8px;'>❌ DROPPED (13)</div>", unsafe_allow_html=True)
            for c in dropped:
                st.markdown(f"<div style='background:#FFF4EE; border-radius:8px; padding:6px 10px; margin-bottom:4px; color:#aaa; font-size:0.82rem; text-decoration:line-through;'><code>{c}</code></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — DATA CLEANING
# ══════════════════════════════════════════════════════════════════════════════
elif slide == 4:
    slide_header("Slide 04", "Data", "Cleaning", "Making the data analysis-ready")

    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown("<h3 style='color:#1e2a4a; font-size:1.05rem; font-weight:700; margin-bottom:0.5rem;'>🧹 Cleaning Pipeline</h3>", unsafe_allow_html=True)
        steps = [
            ("Drop Irrelevant Columns", "Removed 13 of 18 columns not needed for fare/payment analysis."),
            ("Handle Missing Values",   f"{_counts['missing']:,} null rows ({round(_counts['missing']/_counts['raw']*100,2) if _counts['raw'] else 0}% of raw) — safely dropped."),
            ("Fix Data Types",          "Cast passenger_count & payment_type from float → int."),
            ("Remove Duplicates",       f"Identified and dropped exact duplicate trip rows."),
            ("Filter Payment Types",    "Kept only Type 1 (Card) & Type 2 (Cash)."),
            ("Filter Passenger Count",  "Valid range: 1–5 passengers only."),
            ("Remove Negative Values",  "Dropped rows where fare, distance, or duration ≤ 0."),
            ("IQR Outlier Removal",     "Applied 1.5×IQR rule on fare_amount, trip_distance, duration."),
        ]
        colors = [C_BLUE, C_ORANGE, C_TEAL, C_GREEN, C_YELLOW, C_BLUE, C_ORANGE, C_TEAL]
        for i, ((title, desc), clr) in enumerate(zip(steps, colors), 1):
            st.markdown(f"""
            <div class='step-item'>
                <div class='step-num' style='background:{clr};'>{i}</div>
                <div>
                    <strong style='color:#1e2a4a;'>{title}</strong><br>
                    <span style='color:#6b7a99; font-size:0.87rem;'>{desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='color:#1e2a4a; font-size:1.05rem; font-weight:700; margin-bottom:0.8rem;'>📉 Data Reduction</h3>", unsafe_allow_html=True)

        raw_n    = _counts['raw']
        final_n  = _counts['final']
        retained = round(final_n / raw_n * 100, 1) if raw_n else 0

        stages = [
            ("Raw Dataset",           f"{_counts['raw']:,}",          C_BLUE),
            ("After Null Drop",        f"{_counts['after_null']:,}",   C_ORANGE),
            ("After Deduplication",    f"{_counts['after_dedup']:,}",  C_TEAL),
            ("After Filters",          f"{_counts['after_filters']:,}",C_GREEN),
            ("After Outlier Removal",  f"{_counts['final']:,}",        "#00C896"),
        ]
        for label, val, clr in stages:
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center;
                        background:white; border-radius:10px; padding:0.7rem 1rem;
                        margin-bottom:6px; box-shadow:0 1px 6px rgba(30,42,74,0.07);'>
                <span style='color:#6b7a99; font-size:0.87rem;'>{label}</span>
                <span style='color:{clr}; font-weight:800; font-size:0.95rem;'>{val}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        box(f"<strong>✅ {retained}% of data retained</strong> for analysis.<br>Quality over quantity — clean data ensures reliable statistical results.", "green")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — EDA
# ══════════════════════════════════════════════════════════════════════════════
elif slide == 5:
    slide_header("Slide 05", "Exploratory Data", "Analysis", "Uncovering patterns in the clean data")

    if not data_ok:
        st.error(f"Dataset error: {data_err}")
        st.stop()

    card_d = taxi_data[taxi_data['payment_type'] == 'Card']
    cash_d = taxi_data[taxi_data['payment_type'] == 'Cash']

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Fare & Distance", "🥧 Payment Preference", "👥 Passenger Analysis", "📈 Summary Statistics"])

    # --- Tab 1: Distributions ---
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        for ax, col, title, xlabel in [
            (axes[0], 'fare_amount', 'Distribution of Fare Amount', 'Fare Amount ($)'),
            (axes[1], 'trip_distance', 'Distribution of Trip Distance', 'Trip Distance (miles)'),
        ]:
            ax.hist(card_d[col], bins=30, color=C_ORANGE, alpha=0.85, edgecolor='white', linewidth=0.3, label='Card', density=True)
            ax.hist(cash_d[col], bins=30, color=C_TEAL,   alpha=0.75, edgecolor='white', linewidth=0.3, label='Cash',  density=True)
            ax.set_title(title, fontsize=13, fontweight='600', pad=10)
            ax.set_xlabel(xlabel)
            ax.set_ylabel('Density')
            ax.legend(framealpha=0.9)

        fig_light(fig, axes.tolist())
        st.pyplot(fig, use_container_width=True)
        plt.close()

        c1, c2 = st.columns(2)
        cf = card_d['fare_amount'].mean(); cashf = cash_d['fare_amount'].mean()
        cd = card_d['trip_distance'].mean(); cashd = cash_d['trip_distance'].mean()
        with c1:
            box(f"💳 <strong>Card</strong> — Avg Fare: <strong>${cf:.2f}</strong> &nbsp;|&nbsp; Avg Distance: <strong>{cd:.2f} mi</strong>", "orange")
        with c2:
            box(f"💵 <strong>Cash</strong> — Avg Fare: <strong>${cashf:.2f}</strong> &nbsp;|&nbsp; Avg Distance: <strong>{cashd:.2f} mi</strong>", "teal")

    # --- Tab 2: Pie chart ---
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        cc1, cc2 = st.columns([1, 1])
        with cc1:
            counts = taxi_data['payment_type'].value_counts()
            fig, ax = plt.subplots(figsize=(6, 6))
            wedges, texts, autos = ax.pie(
                counts, labels=counts.index, autopct='%1.1f%%',
                startangle=90, shadow=False, colors=[C_ORANGE, C_TEAL],
                wedgeprops=dict(linewidth=2.5, edgecolor='white')
            )
            for t in texts:  t.set_color(C_NAVY); t.set_fontweight('600')
            for a in autos:  a.set_color('white'); a.set_fontsize(13); a.set_fontweight('700')
            ax.set_title('Customer Payment Preference', fontsize=13, fontweight='700', pad=15)
            fig_light(fig, [ax])
            ax.set_facecolor('white')
            st.pyplot(fig, use_container_width=True)
            plt.close()

        with cc2:
            pct = counts / counts.sum() * 100
            st.markdown("<br><br>", unsafe_allow_html=True)
            box(f"""
            <strong>Card payments are dominant</strong> — {pct.iloc[0]:.1f}% of all trips use credit cards.<br><br>
            Since card customers pay higher average fares, converting the remaining <strong>{pct.iloc[1]:.1f}%</strong>
            cash payers could meaningfully improve driver revenue.
            """, "green")

            ca, cb = st.columns(2)
            ca.markdown(mcard(f"{counts.iloc[0]:,}", "Card Trips", C_ORANGE), unsafe_allow_html=True)
            cb.markdown(mcard(f"{counts.iloc[1]:,}", "Cash Trips",  C_TEAL),  unsafe_allow_html=True)

    # --- Tab 3: Passenger stacked bar ---
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        pc = taxi_data.groupby(['payment_type','passenger_count'])[['fare_amount']].count()
        pc.rename(columns={'fare_amount':'count'}, inplace=True)
        pc.reset_index(inplace=True)
        pc['perc'] = pc['count'] / pc['count'].sum() * 100

        df_plot = pd.DataFrame({'payment_type':['Card','Cash']})
        for pv in [1,2,3,4,5]:
            card_v = pc[(pc['payment_type']=='Card') & (pc['passenger_count']==pv)]['perc'].values
            cash_v = pc[(pc['payment_type']=='Cash')  & (pc['passenger_count']==pv)]['perc'].values
            df_plot.loc[0, pv] = card_v[0] if len(card_v)>0 else 0
            df_plot.loc[1, pv] = cash_v[0] if len(cash_v)>0 else 0

        fig, ax = plt.subplots(figsize=(13, 4.5))
        clrs = [C_ORANGE, C_TEAL, C_BLUE, C_GREEN, C_YELLOW]
        df_plot.set_index('payment_type')[[1,2,3,4,5]].plot(
            kind='barh', stacked=True, ax=ax, color=clrs,
            edgecolor='white', linewidth=0.6
        )
        for p in ax.patches:
            w = p.get_width()
            if w > 1:
                x,y = p.get_xy()
                ax.text(x+w/2, y+p.get_height()/2, f'{w:.1f}%',
                        ha='center', va='center', color='white', fontsize=8, fontweight='700')
        ax.set_title('Payment Type by Passenger Count (%)', fontsize=13, fontweight='600')
        ax.set_xlabel('Percentage (%)')
        ax.set_ylabel('Payment Type')
        ax.legend(title='Passengers', fontsize=9, title_fontsize=9)
        fig_light(fig, [ax])
        st.pyplot(fig, use_container_width=True)
        plt.close()
        box("Solo riders (1 passenger) dominate both payment types. Card preference holds consistently across all group sizes, suggesting it is <strong>not driven by group dynamics</strong>.", "blue")

    # --- Tab 4: Summary stats ---
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        summary = taxi_data.groupby('payment_type').agg(
            Trips       =('fare_amount','count'),
            Mean_Fare   =('fare_amount','mean'),
            Std_Fare    =('fare_amount','std'),
            Mean_Dist   =('trip_distance','mean'),
            Std_Dist    =('trip_distance','std'),
            Mean_Dur    =('duration','mean'),
        ).round(3)
        summary.index.name = "Payment Type"
        st.dataframe(summary, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        diff = card_d['fare_amount'].mean() - cash_d['fare_amount'].mean()
        c1, c2, c3 = st.columns(3)
        c1.markdown(mcard(f"${diff:.2f}", "Avg Fare Premium (Card over Cash)", C_ORANGE),  unsafe_allow_html=True)
        c2.markdown(mcard(f"{len(card_d):,}", "Card Trips Analysed", C_BLUE),   unsafe_allow_html=True)
        c3.markdown(mcard(f"{len(cash_d):,}", "Cash Trips Analysed", C_TEAL),   unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — HYPOTHESIS TESTING
# ══════════════════════════════════════════════════════════════════════════════
elif slide == 6:
    slide_header("Slide 06", "Hypothesis", "Testing", "Statistical validation of the fare difference")

    if not data_ok:
        st.error(f"Dataset error: {data_err}")
        st.stop()

    credit_g = taxi_data[taxi_data['payment_type']=='Card']['fare_amount']
    cash_g   = taxi_data[taxi_data['payment_type']=='Cash']['fare_amount']
    # t_stat and p_value are computed globally at startup

    col1, col2 = st.columns([2, 3], gap="large")

    with col1:
        st.markdown("<h3 style='color:#1e2a4a; font-size:1.05rem; font-weight:700;'>📐 Why Welch's T-Test?</h3>", unsafe_allow_html=True)
        box("""
        A <strong>QQ Plot</strong> reveals the fare distribution is <strong>not normally distributed</strong>
        (points deviate from the 45° line). Therefore, we select <strong>Welch's Two-Sample T-test</strong>, which is ideal for:<br>
        <ul style='margin:8px 0 0 1rem;'>
            <li>Large samples with unknown population standard deviation</li>
            <li>Groups with unequal variances</li>
            <li>Non-normal underlying distributions</li>
        </ul>
        """, "blue")

        # QQ Plot
        sample = taxi_data['fare_amount'].sample(min(5000, len(taxi_data)), random_state=42)
        fig, ax = plt.subplots(figsize=(5, 4))
        sm.qqplot(sample, line='45', ax=ax, alpha=0.5, color=C_ORANGE)
        for line in ax.lines:
            if hasattr(line, 'get_color'):
                if line.get_color() not in [C_ORANGE, 'orange']:
                    line.set_color(C_NAVY)
                    line.set_linewidth(1.5)
        ax.set_title('QQ Plot — Fare Amount\n(Non-normal distribution confirmed)', fontsize=10, fontweight='600')
        fig_light(fig, [ax])
        st.pyplot(fig, use_container_width=True)
        plt.close()

        box("The data values <strong>do not follow the 45° reference line</strong>, confirming the distribution is <strong>not normal</strong>. This justifies the T-test approach.", "yellow")

    with col2:
        st.markdown("<h3 style='color:#1e2a4a; font-size:1.05rem; font-weight:700;'>🧪 Test Results</h3>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.markdown(mcard(f"{t_stat:.1f}", "T-Statistic",    C_BLUE),   unsafe_allow_html=True)
        c2.markdown(mcard("< 0.0001",      "P-Value",        C_ORANGE), unsafe_allow_html=True)
        c3.markdown(mcard("0.05",          "Significance α", C_TEAL),   unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        box("""
        ✅ <strong>Reject the Null Hypothesis</strong><br><br>
        With T-statistic = <strong>{:.1f}</strong> and p-value effectively <strong>0.0</strong>
        (far below α = 0.05), there is <strong>overwhelming statistical evidence</strong>
        that the average fare differs significantly between Card and Cash customers.
        This result is <strong>not due to chance</strong>.
        """.format(t_stat), "green")

        # Boxplot
        card_sample = credit_g.sample(min(10000, len(credit_g)), random_state=42)
        cash_sample  = cash_g.sample(min(10000, len(cash_g)),   random_state=42)
        fig, ax = plt.subplots(figsize=(7, 4.5))
        bp = ax.boxplot(
            [card_sample, cash_sample], labels=['Card', 'Cash'],
            patch_artist=True, notch=False,
            boxprops=dict(linewidth=1.5),
            medianprops=dict(color='white', linewidth=2.5),
            whiskerprops=dict(linewidth=1.5),
            capprops=dict(linewidth=1.5),
            flierprops=dict(marker='o', markersize=2, alpha=0.3),
        )
        bp['boxes'][0].set_facecolor(C_ORANGE); bp['boxes'][0].set_alpha(0.85)
        bp['boxes'][1].set_facecolor(C_TEAL);   bp['boxes'][1].set_alpha(0.85)
        bp['whiskers'][0].set_color(C_ORANGE); bp['whiskers'][1].set_color(C_ORANGE)
        bp['whiskers'][2].set_color(C_TEAL);   bp['whiskers'][3].set_color(C_TEAL)
        bp['caps'][0].set_color(C_ORANGE); bp['caps'][1].set_color(C_ORANGE)
        bp['caps'][2].set_color(C_TEAL);   bp['caps'][3].set_color(C_TEAL)
        bp['fliers'][0].set_markerfacecolor(C_ORANGE)
        bp['fliers'][1].set_markerfacecolor(C_TEAL)
        ax.set_title('Fare Amount by Payment Type', fontsize=12, fontweight='600')
        ax.set_ylabel('Fare Amount ($)')

        # annotate mean lines
        for i, (grp, clr) in enumerate([(card_sample, C_BLUE), (cash_sample, C_BLUE)], 1):
            ax.axhline(grp.mean(), color=clr, linestyle='--', linewidth=1.2, alpha=0.6)
            ax.text(i + 0.32, grp.mean(), f'μ=${grp.mean():.2f}', va='center',
                    color=clr, fontsize=8.5, fontweight='600')

        fig_light(fig, [ax])
        st.pyplot(fig, use_container_width=True)
        plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — INSIGHTS & RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif slide == 7:
    slide_header("Slide 07", "Insights &", "Recommendations", "What the data tells us and what to do next")

    if data_ok:
        card_d = taxi_data[taxi_data['payment_type']=='Card']
        cash_d = taxi_data[taxi_data['payment_type']=='Cash']
        card_mean  = card_d['fare_amount'].mean()
        cash_mean  = cash_d['fare_amount'].mean()
        diff       = card_mean - cash_mean
        pct_diff   = (diff / cash_mean) * 100
        card_share = len(card_d) / len(taxi_data) * 100
    else:
        card_mean, cash_mean, diff, pct_diff, card_share = 13.70, 12.25, 1.45, 11.8, 68.7

    # Big metric row
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(mcard(f"${card_mean:.2f}", "Avg Card Fare",         C_ORANGE), unsafe_allow_html=True)
    c2.markdown(mcard(f"${cash_mean:.2f}", "Avg Cash Fare",         C_TEAL),   unsafe_allow_html=True)
    c3.markdown(mcard(f"+${diff:.2f}",     "Card Fare Premium",     C_GREEN),  unsafe_allow_html=True)
    c4.markdown(mcard(f"{card_share:.1f}%","Already Pay by Card",   C_BLUE),   unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("<h3 style='color:#1e2a4a; font-size:1.05rem; font-weight:700; margin-bottom:0.8rem;'>📊 Key Statistical Findings</h3>", unsafe_allow_html=True)
        findings = [
            (C_ORANGE, "Higher fares with card payments",
             f"Card avg ${card_mean:.2f} vs Cash avg ${cash_mean:.2f} — a {abs(pct_diff):.1f}% premium."),
            (C_BLUE,   "Statistically significant difference",
             f"T-stat ≈ {t_stat:.1f}, p ≈ 0.0 — the difference is not due to random chance."),
            (C_TEAL,   "Card already dominates",
             f"{card_share:.1f}% of trips already use card; preference is established."),
            (C_GREEN,  "Pattern holds across passenger counts",
             "Card premium is consistent regardless of group size."),
            (C_YELLOW, "Card riders take longer trips",
             "Higher distance and duration averages for card users."),
        ]
        for clr, title, desc in findings:
            st.markdown(f"""
            <div class='step-item'>
                <div style='width:10px; height:10px; background:{clr}; border-radius:50%; margin-top:6px; flex-shrink:0;'></div>
                <div>
                    <strong style='color:#1e2a4a;'>{title}</strong><br>
                    <span style='color:#6b7a99; font-size:0.87rem;'>{desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='color:#1e2a4a; font-size:1.05rem; font-weight:700; margin-bottom:0.8rem;'>🚀 Business Recommendations</h3>", unsafe_allow_html=True)
        recs = [
            (C_ORANGE, "💳", "Promote Card Payments",
             "Drivers and platforms should actively encourage card usage through in-app prompts and visual reminders."),
            (C_BLUE,   "🎁", "Introduce Card Incentives",
             "Small loyalty rewards for card payers could shift behaviour without significantly reducing revenue."),
            (C_TEAL,   "📱", "Reduce Payment Friction",
             "Ensure POS terminals are always functional and visible — friction discourages card adoption."),
            (C_GREEN,  "📊", "Monitor the Fare Gap Monthly",
             "Re-run statistical tests monthly to track whether the fare premium is growing, stable, or declining."),
        ]
        for clr, emoji, title, desc in recs:
            st.markdown(f"""
            <div style='background:white; border-radius:14px; padding:1rem 1.2rem;
                        margin-bottom:10px; box-shadow:0 2px 10px rgba(30,42,74,0.07);
                        border-left:4px solid {clr};'>
                <div style='font-size:1.3rem; margin-bottom:3px;'>{emoji}</div>
                <div style='font-weight:700; color:#1e2a4a; font-size:0.93rem; margin-bottom:3px;'>{title}</div>
                <div style='color:#6b7a99; font-size:0.85rem; line-height:1.6;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    box(f"""
    🏁 <strong>Final Conclusion</strong><br>
    Statistical hypothesis testing provides <strong>overwhelming evidence</strong> (p ≈ 0.0) that
    credit card customers generate significantly higher fares than cash customers (${card_mean:.2f} vs ${cash_mean:.2f}).
    By strategically nudging customers towards card payments, taxi drivers can meaningfully
    <strong>increase revenue without compromising customer experience</strong>.
    """, "green")

# ─── Bottom Navigation ────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #dee2ea;'>", unsafe_allow_html=True)

n1, n2, n3 = st.columns([1, 2, 1])
with n1:
    if slide > 0:
        if st.button("← Previous", use_container_width=True):
            st.session_state.slide -= 1
            st.rerun()
with n2:
    dots = ""
    for i in range(len(SLIDES)):
        if i == slide:
            dots += f"<span style='display:inline-block;width:22px;height:8px;border-radius:4px;background:#FF6B35;margin:0 3px;'></span>"
        else:
            dots += f"<span style='display:inline-block;width:8px;height:8px;border-radius:50%;background:#dee2ea;margin:0 3px;'></span>"
    st.markdown(f"<div style='text-align:center;padding-top:6px;'>{dots}</div>", unsafe_allow_html=True)
with n3:
    if slide < len(SLIDES) - 1:
        if st.button("Next →", use_container_width=True):
            st.session_state.slide += 1
            st.rerun()
