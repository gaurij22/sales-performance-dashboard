"""
Sales Performance Dashboard - Data Generation & EDA
Author: Gauri Joshi
Description: Generates realistic synthetic sales data and performs
             exploratory data analysis with visualizations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import date, timedelta
import random
import os

# ── Reproducibility ───────────────────────────────────────────────────────────
np.random.seed(42)
random.seed(42)

# ── Output directory ──────────────────────────────────────────────────────────
os.makedirs("data",   exist_ok=True)
os.makedirs("charts", exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# 1. DIMENSION TABLES
# ─────────────────────────────────────────────────────────────────────────────

products = pd.DataFrame({
    "product_id":   range(1, 11),
    "product_name": [
        "Enterprise Suite", "Analytics Pro", "Cloud Connector",
        "Data Bridge", "AutoReport", "PipelineX", "InsightML",
        "SecureVault", "TeamSync", "MobileEdge"
    ],
    "category": [
        "Software", "Analytics", "Cloud", "Integration", "Reporting",
        "ETL", "AI/ML", "Security", "Collaboration", "Mobile"
    ],
    "unit_price": [4999, 2499, 1299, 1799, 899, 1599, 3299, 999, 699, 499]
})

regions = pd.DataFrame({
    "region_id":   range(1, 6),
    "region_name": ["North", "South", "East", "West", "Central"],
    "state":       ["New York", "Texas", "Florida", "California", "Illinois"]
})

reps = pd.DataFrame({
    "rep_id":   range(1, 16),
    "rep_name": [
        "Alice Chen", "Bob Martinez", "Carol White", "David Kim", "Eva Brown",
        "Frank Lee", "Grace Patel", "Henry Zhou", "Iris Singh", "James Wilson",
        "Karen Liu", "Leo Nguyen", "Maya Jones", "Nate Park", "Olivia Davis"
    ],
    "region_id": [1,1,1, 2,2,2, 3,3, 4,4,4, 5,5,5,5]
})

# Date dimension: 2023-01-01 → 2024-12-31
date_range = pd.date_range("2023-01-01", "2024-12-31")
dim_date = pd.DataFrame({
    "date_id":     range(len(date_range)),
    "full_date":   date_range,
    "year":        date_range.year,
    "quarter":     date_range.quarter,
    "month":       date_range.month,
    "month_name":  date_range.strftime("%B"),
    "week":        date_range.isocalendar().week.values,
    "day_of_week": date_range.strftime("%A")
})

# ─────────────────────────────────────────────────────────────────────────────
# 2. FACT: SALES  (2 000 transactions)
# ─────────────────────────────────────────────────────────────────────────────
N = 2000

date_ids   = np.random.choice(dim_date["date_id"], N)
product_ids= np.random.choice(products["product_id"], N,
                              p=[.15,.12,.10,.10,.08,.10,.12,.08,.08,.07])
region_ids = np.random.choice(regions["region_id"], N,
                              p=[.25,.20,.20,.25,.10])
rep_ids    = []
for r in region_ids:
    pool = reps[reps["region_id"] == r]["rep_id"].tolist()
    rep_ids.append(random.choice(pool))

quantities   = np.random.randint(1, 10, N)
prices       = products.set_index("product_id").loc[product_ids, "unit_price"].values
discount_pct = np.round(np.random.choice([0, 5, 10, 15, 20], N,
                                          p=[.40,.25,.20,.10,.05]), 2)
revenue      = np.round(quantities * prices * (1 - discount_pct / 100), 2)
cost         = np.round(revenue * np.random.uniform(0.4, 0.65, N), 2)
profit       = np.round(revenue - cost, 2)

fact_sales = pd.DataFrame({
    "sale_id":     range(1, N + 1),
    "date_id":     date_ids,
    "product_id":  product_ids,
    "region_id":   region_ids,
    "rep_id":      rep_ids,
    "quantity":    quantities,
    "unit_price":  prices,
    "discount_pct":discount_pct,
    "revenue":     revenue,
    "cost":        cost,
    "profit":      profit
})

# ─────────────────────────────────────────────────────────────────────────────
# 3. FACT: TARGETS
# ─────────────────────────────────────────────────────────────────────────────
targets = []
for _, row in regions.iterrows():
    for year in [2023, 2024]:
        for month in range(1, 13):
            targets.append({
                "region_id":     row["region_id"],
                "year":          year,
                "month":         month,
                "target_revenue": round(random.uniform(80000, 150000), 2)
            })
fact_targets = pd.DataFrame(targets).reset_index(drop=True)
fact_targets.insert(0, "target_id", range(1, len(fact_targets) + 1))

# ─────────────────────────────────────────────────────────────────────────────
# 4. SAVE CSVs
# ─────────────────────────────────────────────────────────────────────────────
products.to_csv("data/dim_products.csv",  index=False)
regions.to_csv("data/dim_regions.csv",   index=False)
reps.to_csv("data/dim_sales_reps.csv",   index=False)
dim_date.to_csv("data/dim_date.csv",     index=False)
fact_sales.to_csv("data/fact_sales.csv", index=False)
fact_targets.to_csv("data/fact_targets.csv", index=False)
print("✅  CSVs saved to data/")

# ─────────────────────────────────────────────────────────────────────────────
# 5. MERGE FOR ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
df = (fact_sales
      .merge(dim_date,    on="date_id")
      .merge(products,    on="product_id")
      .merge(regions,     on="region_id")
      .merge(reps,        on="rep_id"))

# ─────────────────────────────────────────────────────────────────────────────
# 6. KPI SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
print("\n📊 KPI SUMMARY")
print("=" * 45)
print(f"  Total Revenue   : ${df['revenue'].sum():>15,.2f}")
print(f"  Total Profit    : ${df['profit'].sum():>15,.2f}")
print(f"  Profit Margin   : {df['profit'].sum()/df['revenue'].sum()*100:>14.1f}%")
print(f"  Total Units Sold: {df['quantity'].sum():>15,}")
print(f"  Avg Deal Size   : ${df['revenue'].mean():>15,.2f}")
print(f"  Avg Discount    : {df['discount_pct'].mean():>14.1f}%")
print(f"  Total Orders    : {len(df):>15,}")

# ─────────────────────────────────────────────────────────────────────────────
# 7. CHARTS
# ─────────────────────────────────────────────────────────────────────────────
STYLE  = "#0F172A"   # dark bg
ACCENT = "#38BDF8"   # sky blue
GREEN  = "#34D399"
RED    = "#F87171"
GOLD   = "#FBBF24"
plt.rcParams.update({
    "figure.facecolor": STYLE, "axes.facecolor": "#1E293B",
    "text.color": "white", "axes.labelcolor": "white",
    "xtick.color": "#94A3B8", "ytick.color": "#94A3B8",
    "axes.edgecolor": "#334155", "grid.color": "#1E293B",
    "font.family": "DejaVu Sans"
})

# --- 7a. Monthly Revenue vs Target ----------------------------------------
monthly = (df.groupby(["year", "month"])["revenue"].sum()
             .reset_index().sort_values(["year","month"]))
monthly["period"] = monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2)

monthly_target = (fact_targets.groupby(["year","month"])["target_revenue"].sum()
                   .reset_index().sort_values(["year","month"]))
monthly_target["period"] = (monthly_target["year"].astype(str) + "-"
                             + monthly_target["month"].astype(str).str.zfill(2))

merged_m = monthly.merge(monthly_target, on="period")

fig, ax = plt.subplots(figsize=(14, 5))
ax.fill_between(range(len(merged_m)), merged_m["revenue"], alpha=0.3, color=ACCENT)
ax.plot(range(len(merged_m)), merged_m["revenue"],    color=ACCENT, lw=2.5, label="Actual Revenue")
ax.plot(range(len(merged_m)), merged_m["target_revenue"], color=GOLD, lw=2, ls="--", label="Target")
ax.set_xticks(range(len(merged_m)))
ax.set_xticklabels(merged_m["period"], rotation=45, ha="right", fontsize=8)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
ax.set_title("Monthly Revenue vs Target", fontsize=16, fontweight="bold", pad=14)
ax.legend(); ax.grid(axis="y", alpha=0.2)
plt.tight_layout()
plt.savefig("charts/01_monthly_revenue_vs_target.png", dpi=150)
plt.close()

# --- 7b. Regional Revenue Bar Chart ----------------------------------------
reg_rev = df.groupby("region_name")["revenue"].sum().sort_values(ascending=False).reset_index()
colors  = [GREEN if v == reg_rev["revenue"].max() else
           RED   if v == reg_rev["revenue"].min() else ACCENT
           for v in reg_rev["revenue"]]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(reg_rev["region_name"], reg_rev["revenue"], color=colors, width=0.55, zorder=2)
for bar, val in zip(bars, reg_rev["revenue"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3000,
            f"${val/1e3:.0f}K", ha="center", va="bottom", fontsize=11, color="white")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
ax.set_title("Revenue by Region", fontsize=16, fontweight="bold", pad=14)
ax.grid(axis="y", alpha=0.2, zorder=0); ax.set_ylim(0, reg_rev["revenue"].max() * 1.15)
plt.tight_layout()
plt.savefig("charts/02_revenue_by_region.png", dpi=150)
plt.close()

# --- 7c. Product Category Breakdown (Donut) ---------------------------------
cat_rev  = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
cat_cols = [ACCENT, GREEN, GOLD, RED, "#C084FC", "#FB923C",
            "#E879F9", "#34D399", "#60A5FA", "#A78BFA"]

fig, ax = plt.subplots(figsize=(8, 7))
wedges, texts, autotexts = ax.pie(
    cat_rev, labels=cat_rev.index, autopct="%1.1f%%",
    colors=cat_cols[:len(cat_rev)], startangle=140,
    pctdistance=0.8, wedgeprops=dict(width=0.55)
)
for t in texts:    t.set_color("white"); t.set_fontsize(10)
for t in autotexts: t.set_color("white"); t.set_fontsize(9)
ax.set_title("Revenue by Product Category", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/03_category_breakdown.png", dpi=150)
plt.close()

# --- 7d. Discount vs Profit Margin Scatter ----------------------------------
rep_stats = df.groupby("rep_name").agg(
    avg_discount=("discount_pct", "mean"),
    margin=("profit",  lambda x: x.sum() / df.loc[x.index, "revenue"].sum() * 100),
    revenue=("revenue", "sum")
).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sc = ax.scatter(rep_stats["avg_discount"], rep_stats["margin"],
                s=rep_stats["revenue"]/500, c=rep_stats["revenue"],
                cmap="cool", alpha=0.85, edgecolors="white", lw=0.5)
for _, row in rep_stats.iterrows():
    ax.annotate(row["rep_name"].split()[0],
                (row["avg_discount"], row["margin"]),
                textcoords="offset points", xytext=(5,5), fontsize=8, color="#CBD5E1")
plt.colorbar(sc, ax=ax, label="Total Revenue ($)")
ax.set_xlabel("Avg Discount %"); ax.set_ylabel("Profit Margin %")
ax.set_title("Discount Rate vs Profit Margin by Sales Rep", fontsize=14, fontweight="bold")
ax.grid(alpha=0.15)
plt.tight_layout()
plt.savefig("charts/04_discount_vs_margin.png", dpi=150)
plt.close()

# --- 7e. Top 10 Products Horizontal Bar ------------------------------------
top10 = df.groupby("product_name")["revenue"].sum().nlargest(10).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top10["product_name"], top10["revenue"],
               color=ACCENT, height=0.6)
for bar, val in zip(bars, top10["revenue"]):
    ax.text(val + 2000, bar.get_y() + bar.get_height()/2,
            f"${val/1e3:.0f}K", va="center", fontsize=10, color="white")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
ax.set_title("Top 10 Products by Revenue", fontsize=16, fontweight="bold")
ax.grid(axis="x", alpha=0.2); ax.invert_yaxis()
plt.tight_layout()
plt.savefig("charts/05_top10_products.png", dpi=150)
plt.close()

print("\n✅  Charts saved to charts/")
print("\n🎉  EDA complete! Open the charts/ folder to view all visualizations.")
