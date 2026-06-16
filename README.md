# E-Commerce Sales Intelligence Dashboard

An interactive BI dashboard built with Streamlit and Plotly. Filters sales data in real-time across regions, segments, products, and reps — with KPI cards, trend charts, a rep leaderboard, and a live data explorer.

**[→ Live Dashboard](https://favour-sales-dashboard.streamlit.app)**

---

## What it does

- **KPI Cards** — Net revenue, orders, avg order value, units sold, return rate, estimated profit
- **Revenue Trends** — Monthly bar + line combo chart, MoM growth table, quarterly pie
- **Regional & Segment Analysis** — Horizontal bar charts, segment comparison, region × segment heatmap
- **Product & Channel Breakdown** — Revenue by product, channel split, return rate by product
- **Rep Leaderboard** — Revenue ranking, orders vs deal size scatter, full sortable table
- **Data Explorer** — Filter and download the underlying dataset as CSV

## Stack

| Tool | Purpose |
|------|---------|
| Python | Core logic and data processing |
| Streamlit | Web app framework |
| Plotly | Interactive charts |
| Pandas | Data transformation and aggregation |

## Run locally

```bash
git clone https://github.com/Favourson/streamlit-sales-dashboard
cd streamlit-sales-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Folder structure

```
streamlit-sales-dashboard/
├── app.py                # Full dashboard application
├── data/
│   └── ecommerce_data.csv
├── requirements.txt
└── README.md
```

## About

Built by [Favour Osborn Emmanson](https://favourson.github.io) — Data & Automation Analyst based in London.