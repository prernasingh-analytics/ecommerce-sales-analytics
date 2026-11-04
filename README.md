# E-Commerce Sales & Customer Analytics Dashboard

### Python | SQL | Pandas | Plotly | Data Analytics

An end-to-end data analytics project using the Brazilian E-Commerce Public Dataset by Olist. The project analyzes sales performance, customer purchasing behaviour, and customer segments to identify business trends and opportunities.

**[View Live Interactive Dashboard](https://prernasingh-analytics.github.io/ecommerce-sales-analytics/dashboard/index.html)**

## Project Objectives

- Analyze e-commerce revenue and order trends.
- Identify top-performing product categories and customer states.
- Understand customer purchasing frequency and repeat purchases.
- Segment customers using recency and purchase frequency.
- Translate analytical findings into actionable business insights.

## Tools & Technologies

- **Python:** Data processing and analysis
- **Pandas:** Data cleaning, merging, aggregation, and customer-level analysis
- **SQL:** Analytical queries
- **Plotly:** Interactive data visualizations
- **HTML/CSS:** Dashboard presentation
- **GitHub Pages:** Dashboard deployment

## Key Performance Indicators

| Metric | Value |
|---|---|
| Total Orders | 99,441 |
| Delivered Orders | 96,478 |
| Delivered Product Revenue | R$13.22 million |
| Unique Delivered Customers | 93,358 |
| Repeat Customers | 2,801 |
| Repeat Customer Rate | 3.00% |
| Average Delivered Order Value | R$137.04 |
| Top Product Category | Health & Beauty |

Revenue and order value are based on delivered order-item prices, excluding freight.

## Sales Analysis

The dashboard includes:

- Monthly revenue and order trends
- Revenue by product category
- Sales performance across customer states
- Interactive state and category filters
- Key sales performance indicators

## Customer Behaviour Analysis

Customer analysis uses `customer_unique_id` to identify individual customers across orders.

**Key findings:**

- Approximately 97% of customers placed only one delivered order.
- Only 3% of customers made repeat purchases.
- The median customer purchase frequency was one order.
- Customer retention represents an important opportunity for further investigation.

## Customer Segmentation

Customers were grouped into four exploratory segments using their most recent delivered purchase and total delivered purchase frequency.

| Customer Segment | Customers | Share |
|---|---:|---:|
| Older One-Time Buyers | 72,712 | 77.89% |
| Recent One-Time Buyers | 17,845 | 19.11% |
| Other Repeat Buyers | 2,187 | 2.34% |
| Recent Repeat Buyers | 614 | 0.66% |

**Segmentation rules:**

- Recent customers: Last delivered purchase within 90 days of the analysis snapshot (August 30, 2018).
- Repeat customers: Two or more delivered orders.
- Older customers: Last delivered purchase more than 90 days before the snapshot.

These are descriptive, exploratory segments rather than predictive customer classifications.

## Business Insights

1. **Customer retention:** The low observed repeat-purchase rate suggests an opportunity to investigate repeat purchasing and customer engagement.
2. **One-time customer dominance:** Most delivered customers purchased only once during the dataset period.
3. **Revenue concentration:** Older one-time buyers account for a large share of historical delivered product revenue.
4. **Customer targeting:** Recent one-time buyers could be evaluated for follow-up campaigns, while repeat customers could be studied for loyalty patterns.

These findings describe historical customer behaviour and do not establish the effectiveness of any proposed marketing intervention.

## Data Source

Brazilian E-Commerce Public Dataset by Olist, available on Kaggle.

The dataset contains historical e-commerce transactions from Brazil, primarily covering 2016–2018.

## Methodology & Limitations

- Sales metrics focus on delivered orders.
- Revenue is calculated from delivered order-item prices, excluding freight.
- Customers are identified using `customer_unique_id`.
- Customer segments are based on a fixed historical snapshot.
- Sales filters apply to the sales visualizations; customer KPIs and segmentation charts reflect the full delivered-customer dataset.
- The dataset does not support conclusions about current customer behaviour or future campaign outcomes.

## Project Outputs

- `build.py` — Python analysis and dashboard generation
- `dashboard/index.html` — Interactive dashboard
- `outputs/customer_metrics.json` — Customer KPI results
- `outputs/customer_segments.csv` — Customer segmentation results

## Live Dashboard

**[Explore the E-Commerce Sales & Customer Analytics Dashboard](https://prernasingh-analytics.github.io/ecommerce-sales-analytics/dashboard/index.html)**
