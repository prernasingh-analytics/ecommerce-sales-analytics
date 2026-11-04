## 📊 Live Interactive Dashboard

[Click here to explore my E-Commerce Sales Dashboard](https://prernasingh-analytics.github.io/ecommerce-sales-analytics/dashboard/index.html)# E-Commerce Sales & Customer Analytics | Olist

An **offline, interactive HTML dashboard** and reproducible Python/SQL analytics project built using the public [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Historical 2016–2018 transactions; no live data.

## Dashboard
Open **`dashboard/index.html`** in Chrome, Safari, or another browser. No server, internet, or Power BI license required. Select a customer state or product category to update KPIs and charts.

## Key results (all states and categories)
- 99,441 orders in source orders table; 96,478 have delivered status.
- 110,197 delivered order-item rows; **R$13,221,498.11** delivered item-price total (freight excluded).
- Top category by delivered item-price total: **health_beauty** (R$1,233,131.72, category labels in dashboard are translated).

## Contents
- `dashboard/index.html` — self-contained Plotly dashboard (offline, interactive)
- `data/monthly_state_category.csv` — derived aggregates (not raw customer-level records)
- `data/monthly_state_orders.csv` — monthly delivered-order counts by customer state
- `outputs/` — exported charts, CSV summaries, metric JSON
- `sql/analysis.sql` — example SQLite analysis queries; import source tables before running
- `build.py` — rebuild from Olist source ZIP (see setup note)
- `requirements.txt` — Python dependencies

## Rebuild from original source
1. Download the dataset ZIP from Kaggle and save it as `archive.zip` in the project folder.
2. Install dependencies: `python3 -m pip install -r requirements.txt`.
3. Run `python3 build.py` from the project folder. The script reads `archive.zip` from that folder and recreates the dashboard and aggregates.
4. Open `dashboard/index.html`.

## Definitions and limitations
- Item revenue is the sum of `order_items.price` on orders marked `delivered`, **not** net revenue, GMV, profit or payment total. Freight is excluded.
- Monthly trend uses **purchase month**. Partial months at the dataset boundaries should not be compared to complete months.
- One order can contain multiple items/categories, so distinct orders across categories **must not be added** together. Dashboard order KPI is deduplicated at each filter combination.
- Dataset is historical, anonymized, and cannot establish causality.
- Dashboard is HTML/Plotly, **not** a Power BI `.pbix` file.

## Interview explanation
I joined orders to items to measure delivered item-price revenue, joined customer geography and product category labels, grouped results by month/state/category, and made an interactive dashboard. I used distinct order IDs for order counts to avoid double-counting multi-item orders.

## Suggested resume line (after you run and understand the project)
> Built an interactive e-commerce analytics dashboard using Python, SQL, and Plotly to explore 96K+ delivered orders, R$13.22M in item-price revenue, product category performance, and geographic sales trends.

## Attribution
Dataset: Olist, via Kaggle. Original data not redistributed in this repository. Project code: MIT License.


### Offline dashboard
Open `dashboard/index.html` directly in a browser. This version uses inline data and native SVG charts, requiring no server or external libraries.
