# E-Commerce Sales & Customer Analytics | Olist

## 📊 Live Interactive Dashboard

**[Explore the Live Dashboard](https://prernasingh-analytics.github.io/ecommerce-sales-analytics/dashboard/index.html)**

## Project Overview

An end-to-end e-commerce analytics portfolio project based on the **Olist Brazilian E-Commerce Dataset**, containing historical transactions from 2016–2018.

The project includes Python data preparation, SQL analysis queries, processed datasets, sales visualizations, and an interactive web dashboard.

**Objective:** Explore sales performance, customer purchasing patterns, product category contributions, and geographic trends to support business decision-making.

## Technologies Used

- **Python:** Pandas for data loading, cleaning, joining, aggregation, and validation.
- **SQL:** Queries for revenue analysis, order counts, and category performance.
- **HTML, CSS, JavaScript:** Interactive dashboard development.
- **CSV and JSON:** Processed data and metric outputs.
- **GitHub Pages:** Dashboard hosting and deployment.

## Business Questions

1. How many orders were placed and successfully delivered?
2. How much delivered item-price revenue was generated?
3. Which product categories contributed the most revenue?
4. How does sales performance vary across Brazilian states?
5. How do monthly sales and revenue change over time?

## Key Findings

| Metric | Result |
|---|---|
| Total Orders | 99,441 |
| Delivered Orders | 96,478 |
| Delivered Order-Item Records | 110,197 |
| Delivered Item-Price Revenue | R$13,221,498.11 |
| Top Revenue Category | Health & Beauty |

*Revenue is calculated from item prices on delivered orders, excluding freight. It does not represent profit or net company revenue.*

## Project Workflow

**1. Data Preparation — Python**

The `build.py` script is designed to load the original Olist dataset from a ZIP archive, combine orders, items, customers, products, and category translations, filter delivered transactions, and generate aggregated datasets.

**2. Data Analysis — SQL**

The `sql/analysis.sql` file contains SQL queries for analyzing delivered-order revenue, monthly sales, and product category performance.

**3. Analytical Outputs**

The `data/` and `outputs/` folders contain processed CSV datasets, metrics, and exported sales visualizations.

**4. Interactive Dashboard**

The browser-based dashboard provides KPI cards, charts, and interactive filters for exploring sales, customer states, and product categories.

## Project Structure

```text
ecommerce-sales-analytics/
├── build.py
├── requirements.txt
├── LICENSE
├── README.md
├── sql/
│   └── analysis.sql
├── data/
│   ├── monthly_state_category.csv
│   └── monthly_state_orders.csv
├── outputs/
│   ├── category_sales.csv
│   ├── metrics.json
│   ├── monthly_revenue.png
│   ├── monthly_sales.csv
│   ├── state_sales.csv
│   └── top_categories.png
└── dashboard/
    └── index.html
```

## Running the Project

**View the dashboard:** Open the live dashboard link at the top of this README.

**Run locally:** Download the repository and open `dashboard/index.html` in a browser.

**Rebuild the data:** Download the original Olist dataset ZIP from Kaggle, place it alongside `build.py` as `archive.zip`, install dependencies using `pip install -r requirements.txt`, and run `python3 build.py`.

The full rebuild procedure has not yet been independently verified in this repository.

## Dataset

**Source:** [Olist Brazilian E-Commerce Public Dataset — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The dataset contains historical Brazilian e-commerce transactions. Original raw data is not redistributed in this repository.

## Limitations

- The dataset is historical, not real-time.
- Revenue excludes freight charges and is not profit.
- Orders may contain multiple items and categories, so category-level distinct order counts should not be summed.
- Results are descriptive and do not establish causality.

## Project Outcome

Published an interactive analytics dashboard alongside Python processing code, SQL queries, and supporting analytical outputs to demonstrate an e-commerce business intelligence workflow.
