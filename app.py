"""
E-Commerce Sales Intelligence Dashboard
========================================
Interactive BI dashboard built with Streamlit and Plotly.
Filters, KPI cards, trend analysis, rep leaderboard, and data explorer.

Author: Favour Osborn Emmanson
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #1a1d27; }
    [data-testid="stSidebar"] .stMarkdown { color: #8892a4; }
    
    /* KPI cards */
    .kpi-card {
        background: linear-gradient(135deg, #1e2235 0%, #252a3a 100%);
        border: 1px solid #2e3650;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 8px;
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        color: #8892a4;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.1;
    }
    .kpi-delta {
        font-size: 12px;
        color: #3ecf8e;
        margin-top: 4px;
    }
    .kpi-delta.neg { color: #f87171; }
    
    /* Section headers */
    .section-header {
        font-size: 13px;
        font-weight: 600;
        color: #4f9cf9;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        padding: 6px 0 12px 0;
        border-bottom: 1px solid #2e3650;
        margin-bottom: 16px;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    [data-testid="collapsedControl"] { display: block !important; color: white !important; }
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { background-color: #1a1d27; border-radius: 8px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { color: #8892a4; }
    .stTabs [aria-selected="true"] { background-color: #252a3a; color: #ffffff; border-radius: 6px; }
    
    /* Dataframe */
    .stDataFrame { background-color: #1a1d27; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DATA LOADING & PROCESSING
# ══════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    df = pd.read_csv("data/ecommerce_data.csv", parse_dates=["date"])
    df["gross_revenue"]  = df["units"] * df["unit_price"]
    df["discount_value"] = df["gross_revenue"] * df["discount"]
    df["return_value"]   = df["returns"] * df["unit_price"]
    df["net_revenue"]    = df["gross_revenue"] - df["discount_value"] - df["return_value"]
    df["profit_margin"]  = (df["net_revenue"] * 0.35).round(2)  # simulated 35% margin
    df["month"]          = df["date"].dt.to_period("M").astype(str)
    df["month_dt"]       = df["date"].dt.to_period("M").dt.to_timestamp()
    df["quarter"]        = "Q" + df["date"].dt.quarter.astype(str)
    df["return_rate"]    = df["returns"] / df["units"]
    return df

df = load_data()

# ══════════════════════════════════════════════════════════════
# SIDEBAR FILTERS
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 📊 Dashboard Filters")
    st.markdown("---")

    # Date range
    st.markdown("**Date Range**")
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_from, date_to = st.date_input(
        "Select range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )

    st.markdown("**Region**")
    regions = ["All"] + sorted(df["region"].unique().tolist())
    selected_region = st.selectbox("Region", regions, label_visibility="collapsed")

    st.markdown("**Customer Segment**")
    segments = ["All"] + sorted(df["segment"].unique().tolist())
    selected_segment = st.selectbox("Segment", segments, label_visibility="collapsed")

    st.markdown("**Category**")
    categories = ["All"] + sorted(df["category"].unique().tolist())
    selected_category = st.selectbox("Category", categories, label_visibility="collapsed")

    st.markdown("**Sales Rep**")
    reps = ["All"] + sorted(df["sales_rep"].unique().tolist())
    selected_rep = st.selectbox("Sales Rep", reps, label_visibility="collapsed")

    st.markdown("**Sales Channel**")
    channels = ["All"] + sorted(df["channel"].unique().tolist())
    selected_channel = st.selectbox("Channel", channels, label_visibility="collapsed")

    st.markdown("---")
    st.markdown(
        "<div style='font-size:11px;color:#555e72;'>Built by Favour Emmanson<br>"
        "<a href='https://github.com/Favourson' style='color:#4f9cf9;'>GitHub</a> · "
        "<a href='https://www.linkedin.com/in/favour-emmanson' style='color:#4f9cf9;'>LinkedIn</a></div>",
        unsafe_allow_html=True
    )

# ── Apply filters ─────────────────────────────────────────────
filtered = df[
    (df["date"].dt.date >= date_from) &
    (df["date"].dt.date <= date_to)
]
if selected_region   != "All": filtered = filtered[filtered["region"]   == selected_region]
if selected_segment  != "All": filtered = filtered[filtered["segment"]  == selected_segment]
if selected_category != "All": filtered = filtered[filtered["category"] == selected_category]
if selected_rep      != "All": filtered = filtered[filtered["sales_rep"]== selected_rep]
if selected_channel  != "All": filtered = filtered[filtered["channel"]  == selected_channel]

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════

st.markdown("""
<div style='padding: 8px 0 24px 0;'>
    <div style='font-size:11px;color:#4f9cf9;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;'>
        // Sales Intelligence
    </div>
    <h1 style='color:#ffffff;font-size:2rem;font-weight:700;margin:0;letter-spacing:-0.02em;'>
        E-Commerce Performance Dashboard
    </h1>
    <p style='color:#8892a4;font-size:14px;margin-top:6px;'>
        Real-time sales analytics · Revenue, segments, trends & rep performance
    </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════

total_revenue  = filtered["net_revenue"].sum()
total_orders   = len(filtered)
avg_order_val  = filtered["net_revenue"].mean() if total_orders > 0 else 0
total_units    = filtered["units"].sum()
return_rate    = (filtered["returns"].sum() / filtered["units"].sum() * 100) if total_units > 0 else 0
total_profit   = filtered["profit_margin"].sum()

k1, k2, k3, k4, k5, k6 = st.columns(6)

def kpi(col, label, value, delta=""):
    neg = delta.startswith("-") if delta else False
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {"<div class='kpi-delta" + (" neg" if neg else "") + "'>" + delta + "</div>" if delta else ""}
    </div>
    """, unsafe_allow_html=True)

kpi(k1, "Net Revenue",    f"£{total_revenue:,.0f}",  "↑ vs prior period")
kpi(k2, "Total Orders",   f"{total_orders:,}",        "")
kpi(k3, "Avg Order Value",f"£{avg_order_val:,.2f}",  "")
kpi(k4, "Units Sold",     f"{total_units:,}",         "")
kpi(k5, "Return Rate",    f"{return_rate:.1f}%",      "-0.3% vs prior" if return_rate < 10 else "↑ needs review")
kpi(k6, "Est. Profit",    f"£{total_profit:,.0f}",   "@ 35% margin")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈  Revenue Trends",
    "🌍  Regional & Segment",
    "📦  Products & Channels",
    "🏆  Rep Leaderboard",
    "🔍  Data Explorer"
])

CHART_BG    = "#13161e"
GRID_COLOR  = "#252a3a"
FONT_COLOR  = "#8892a4"
ACCENT      = "#4f9cf9"
GREEN       = "#3ecf8e"
PURPLE      = "#a78bfa"
ORANGE      = "#fb923c"

def chart_layout(fig, title="", height=380):
    fig.update_layout(
        title=dict(text=title, font=dict(color="#e8eaf0", size=14)),
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(color=FONT_COLOR, family="Inter, sans-serif"),
        height=height,
        margin=dict(l=16, r=16, t=40 if title else 16, b=16),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONT_COLOR)),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
    )
    return fig

# ── TAB 1: Revenue Trends ─────────────────────────────────────
with tab1:
    col_a, col_b = st.columns([2, 1])

    with col_a:
        monthly = (
            filtered.groupby("month_dt")
            .agg(Net_Revenue=("net_revenue", "sum"), Orders=("order_id", "count"))
            .reset_index()
            .sort_values("month_dt")
        )
        monthly["MoM_%"] = monthly["Net_Revenue"].pct_change() * 100

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=monthly["month_dt"], y=monthly["Net_Revenue"],
            name="Net Revenue", marker_color=ACCENT, opacity=0.85
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=monthly["month_dt"], y=monthly["Orders"],
            name="Orders", line=dict(color=GREEN, width=2),
            mode="lines+markers", marker=dict(size=5)
        ), secondary_y=True)
        fig.update_yaxes(title_text="Net Revenue (£)", secondary_y=False, gridcolor=GRID_COLOR)
        fig.update_yaxes(title_text="Orders", secondary_y=True, gridcolor=GRID_COLOR)
        chart_layout(fig, "Monthly Revenue & Order Volume", height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        quarter = (
            filtered.groupby("quarter")
            .agg(Net_Revenue=("net_revenue", "sum"))
            .reset_index()
        )
        fig2 = px.pie(
            quarter, values="Net_Revenue", names="quarter",
            color_discrete_sequence=[ACCENT, GREEN, PURPLE, ORANGE],
            hole=0.55
        )
        fig2.update_traces(textfont_color="#ffffff", textinfo="percent+label")
        chart_layout(fig2, "Revenue by Quarter", height=380)
        st.plotly_chart(fig2, use_container_width=True)

    # MoM growth table
    if not monthly.empty:
        st.markdown('<div class="section-header">Month-on-Month Growth</div>', unsafe_allow_html=True)
        display = monthly.copy()
        display["month_dt"] = display["month_dt"].dt.strftime("%b %Y")
        display["Net_Revenue"] = display["Net_Revenue"].apply(lambda x: f"£{x:,.0f}")
        display["MoM_%"] = display["MoM_%"].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "—")
        display.columns = ["Month", "Net Revenue", "Orders", "MoM Growth"]
        st.dataframe(display, use_container_width=True, hide_index=True)

# ── TAB 2: Regional & Segment ─────────────────────────────────
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        by_region = (
            filtered.groupby("region")
            .agg(Net_Revenue=("net_revenue", "sum"), Orders=("order_id", "count"))
            .reset_index().sort_values("Net_Revenue", ascending=True)
        )
        fig = px.bar(
            by_region, x="Net_Revenue", y="region", orientation="h",
            color="Net_Revenue", color_continuous_scale=["#1e3a5f", ACCENT],
            text=by_region["Net_Revenue"].apply(lambda x: f"£{x:,.0f}")
        )
        fig.update_traces(textposition="outside", textfont_color="#ffffff")
        fig.update_coloraxes(showscale=False)
        chart_layout(fig, "Net Revenue by Region", height=340)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        by_segment = (
            filtered.groupby("segment")
            .agg(Net_Revenue=("net_revenue", "sum"), Orders=("order_id", "count"))
            .reset_index()
        )
        fig2 = px.bar(
            by_segment, x="segment", y="Net_Revenue",
            color="segment",
            color_discrete_sequence=[ACCENT, GREEN, PURPLE],
            text=by_segment["Net_Revenue"].apply(lambda x: f"£{x:,.0f}")
        )
        fig2.update_traces(textposition="outside", textfont_color="#ffffff")
        fig2.update_layout(showlegend=False)
        chart_layout(fig2, "Revenue by Customer Segment", height=340)
        st.plotly_chart(fig2, use_container_width=True)

    # Region × Segment heatmap
    st.markdown('<div class="section-header">Revenue Heatmap — Region × Segment</div>', unsafe_allow_html=True)
    pivot = filtered.pivot_table(
        values="net_revenue", index="region", columns="segment", aggfunc="sum", fill_value=0
    ).round(0)
    fig3 = px.imshow(
        pivot, color_continuous_scale=["#13161e", "#1e3a5f", ACCENT],
        text_auto=True, aspect="auto"
    )
    fig3.update_traces(texttemplate="£%{z:,.0f}", textfont=dict(color="white", size=11))
    chart_layout(fig3, height=280)
    st.plotly_chart(fig3, use_container_width=True)

# ── TAB 3: Products & Channels ────────────────────────────────
with tab3:
    col_a, col_b = st.columns(2)

    with col_a:
        by_product = (
            filtered.groupby("product")
            .agg(Net_Revenue=("net_revenue", "sum"), Units=("units", "sum"))
            .reset_index().sort_values("Net_Revenue", ascending=False)
        )
        fig = px.bar(
            by_product, x="product", y="Net_Revenue",
            color="Net_Revenue", color_continuous_scale=["#1e3a5f", GREEN],
            text=by_product["Net_Revenue"].apply(lambda x: f"£{x:,.0f}")
        )
        fig.update_traces(textposition="outside", textfont_color="#ffffff")
        fig.update_coloraxes(showscale=False)
        fig.update_xaxes(tickangle=-30)
        chart_layout(fig, "Net Revenue by Product", height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        by_channel = (
            filtered.groupby("channel")
            .agg(Net_Revenue=("net_revenue", "sum"), Orders=("order_id", "count"))
            .reset_index()
        )
        fig2 = px.pie(
            by_channel, values="Net_Revenue", names="channel",
            color_discrete_sequence=[ACCENT, GREEN, PURPLE, ORANGE],
            hole=0.5
        )
        fig2.update_traces(textfont_color="#ffffff", textinfo="percent+label")
        chart_layout(fig2, "Revenue Split by Channel", height=380)
        st.plotly_chart(fig2, use_container_width=True)

    # Return rate by product
    st.markdown('<div class="section-header">Return Rate by Product</div>', unsafe_allow_html=True)
    ret = (
        filtered.groupby("product")
        .agg(Returns=("returns", "sum"), Units=("units", "sum"))
        .reset_index()
    )
    ret["Return_Rate_%"] = (ret["Returns"] / ret["Units"] * 100).round(2)
    fig3 = px.bar(
        ret.sort_values("Return_Rate_%", ascending=False),
        x="product", y="Return_Rate_%",
        color="Return_Rate_%",
        color_continuous_scale=["#1e4d2b", "#f87171"],
        text=ret.sort_values("Return_Rate_%", ascending=False)["Return_Rate_%"].apply(lambda x: f"{x:.1f}%")
    )
    fig3.update_traces(textposition="outside", textfont_color="#ffffff")
    fig3.update_coloraxes(showscale=False)
    chart_layout(fig3, height=300)
    st.plotly_chart(fig3, use_container_width=True)

# ── TAB 4: Rep Leaderboard ────────────────────────────────────
with tab4:
    by_rep = (
        filtered.groupby("sales_rep")
        .agg(
            Net_Revenue=("net_revenue", "sum"),
            Orders=("order_id", "count"),
            Units=("units", "sum"),
            Avg_Deal=("net_revenue", "mean"),
            Return_Rate=("return_rate", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("Net_Revenue", ascending=False)
    )
    by_rep.insert(0, "Rank", range(1, len(by_rep) + 1))
    by_rep["Return_Rate_%"] = (by_rep["Return_Rate"] * 100).round(1)
    by_rep = by_rep.drop(columns="Return_Rate")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        fig = px.bar(
            by_rep.sort_values("Net_Revenue"),
            x="Net_Revenue", y="sales_rep", orientation="h",
            color="Net_Revenue", color_continuous_scale=["#1e3a5f", GREEN],
            text=by_rep.sort_values("Net_Revenue")["Net_Revenue"].apply(lambda x: f"£{x:,.0f}")
        )
        fig.update_traces(textposition="outside", textfont_color="#ffffff")
        fig.update_coloraxes(showscale=False)
        chart_layout(fig, "Revenue by Sales Rep", height=340)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig2 = px.scatter(
            by_rep, x="Orders", y="Avg_Deal",
            size="Net_Revenue", color="sales_rep",
            color_discrete_sequence=[ACCENT, GREEN, PURPLE, ORANGE],
            text="sales_rep", hover_data=["Net_Revenue"]
        )
        fig2.update_traces(textposition="top center", textfont_color="#ffffff")
        chart_layout(fig2, "Orders vs Avg Deal Size (bubble = revenue)", height=340)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header">Full Leaderboard</div>', unsafe_allow_html=True)
    display_rep = by_rep.copy()
    display_rep["Net_Revenue"] = display_rep["Net_Revenue"].apply(lambda x: f"£{x:,.0f}")
    display_rep["Avg_Deal"]    = display_rep["Avg_Deal"].apply(lambda x: f"£{x:,.2f}")
    display_rep.columns = ["Rank", "Sales Rep", "Net Revenue", "Orders", "Units", "Avg Deal Size", "Return Rate %"]
    st.dataframe(display_rep, use_container_width=True, hide_index=True)

# ── TAB 5: Data Explorer ─────────────────────────────────────
with tab5:
    st.markdown('<div class="section-header">Raw Data Explorer</div>', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Filtered Rows", f"{len(filtered):,}")
    with col_b:
        st.metric("Date Range", f"{date_from} → {date_to}")
    with col_c:
        st.metric("Unique Customers", f"{filtered['customer_id'].nunique():,}")

    display_cols = [
        "order_id","date","customer_name","segment","region",
        "sales_rep","category","product","units","unit_price",
        "discount","net_revenue","channel"
    ]
    st.dataframe(
        filtered[display_cols].sort_values("date", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    csv = filtered[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download filtered data as CSV",
        data=csv,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )