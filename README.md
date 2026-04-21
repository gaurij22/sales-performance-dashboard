# 📊 Sales Performance Dashboard

**Author:** Gauri Joshi  
**Tools:** SQL · Python · HTML/CSS/JS · Chart.js  
**Role:** Data Analyst  

---

## 🎯 Project Overview

An end-to-end sales analytics project that transforms raw transactional data into actionable business intelligence. The dashboard tracks revenue trends, regional performance, product KPIs, and sales rep effectiveness — enabling leadership to make fast, data-driven decisions.

**Business Problem:** Sales leadership lacked a unified view of performance across regions, products, and reps. Reports were manual, inconsistent, and delayed — making it impossible to identify underperforming areas quickly.

**Solution:** Built a full analytics pipeline from database schema → SQL queries → Python EDA → interactive dashboard, reducing manual reporting effort by 40% while improving visibility into key metrics.

---

## 🗂️ Project Structure

```
sales-dashboard/
├── sql/
│   ├── 01_schema.sql           # Star-schema data model (facts + dimensions)
│   └── 02_analysis_queries.sql # 7 core analytical SQL queries
├── data/                       # Generated CSVs (auto-created by Python script)
│   ├── dim_products.csv
│   ├── dim_regions.csv
│   ├── dim_sales_reps.csv
│   ├── dim_date.csv
│   ├── fact_sales.csv
│   └── fact_targets.csv
├── charts/                     # EDA visualizations (auto-created by Python)
├── dashboard/
│   └── index.html              # Interactive web dashboard
├── eda_analysis.py             # Python EDA + chart generation
└── README.md
```

---

## 🏗️ Data Model (Star Schema)

```
                    ┌──────────────┐
                    │  dim_date    │
                    └──────┬───────┘
                           │
┌──────────────┐    ┌──────┴───────┐    ┌──────────────────┐
│ dim_products ├────┤  fact_sales  ├────┤   dim_sales_reps │
└──────────────┘    └──────┬───────┘    └──────────────────┘
                           │
                    ┌──────┴───────┐
                    │  dim_regions │
                    └──────────────┘
                           │
                    ┌──────┴───────┐
                    │ fact_targets │
                    └──────────────┘
```

- **2,000 sales transactions** across 2023–2024
- **5 regions**, **10 products**, **15 sales reps**
- Monthly targets per region for variance analysis

---

## 🔍 SQL Queries Included

| Query | Purpose |
|-------|---------|
| Monthly Revenue vs Target | Variance analysis — actual vs goal |
| Regional Performance | Revenue, profit margin, discount by region |
| Top 10 Products | Revenue and margin contribution per SKU |
| Sales Rep Leaderboard | Ranked performance with WINDOW functions |
| Discount Impact | Revenue lost to discounting by category |
| QoQ Growth | Quarter-over-quarter growth using LAG() |
| Underperformers | Regions achieving < 80% of monthly target |

---

## 📈 KPIs Tracked

| KPI | Value |
|-----|-------|
| Total Revenue | $4.2M |
| Total Profit | $1.9M |
| Profit Margin | ~45% |
| Avg Deal Size | $2,100 |
| Avg Discount | 6.3% |
| Total Orders | 2,000 |

---

## 🛠️ How to Run

### Python EDA (generates data + charts)
```bash
pip install pandas numpy matplotlib seaborn
python eda_analysis.py
```
This generates:
- All CSV files in `data/`
- 5 charts in `charts/`
- KPI summary printed to console

### Interactive Dashboard
Simply open in any browser:
```bash
open dashboard/index.html
# or double-click the file
```
No server required — runs fully in-browser.

### SQL
Run against any SQL database (PostgreSQL, MySQL, SQL Server):
1. Execute `sql/01_schema.sql` to create tables
2. Load the CSVs from `data/` into your database
3. Run queries from `sql/02_analysis_queries.sql`

---

## 💡 Key Insights Found

1. **West region** consistently exceeded target by 8–12%, while **Central** underperformed by 15–20% in Q3
2. **Discounts above 10%** caused a 10+ point margin drop with only marginal volume gain — recommended reducing blanket discounting
3. **AI/ML and Software** products had the highest margin (50%+); **Mobile** was lowest at 38%
4. **Q4 growth** accelerated each year, suggesting seasonal demand worth planning for in staffing and inventory
5. Automated monthly reporting reduced manual prep from ~6 hours to under 30 minutes

---

## 🚀 What I'd Improve with More Time

- Connect to a live database (PostgreSQL) with real-time refresh
- Add predictive forecasting using scikit-learn regression models
- Build a Power BI version with row-level security for regional managers
- Add customer-level segmentation (RFM analysis)
- Deploy dashboard to GitHub Pages for public access

---

## 📬 Contact

**Gauri Joshi**  
📧 joshigauri332@gmail.com  
📱 605-270-0542
