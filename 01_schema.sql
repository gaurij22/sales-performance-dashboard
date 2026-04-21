-- ============================================================
-- Sales Performance Dashboard - Database Schema
-- Author: Gauri Joshi
-- Description: Schema for sales analytics data warehouse
-- ============================================================

-- Dimension: Products
CREATE TABLE dim_products (
    product_id      INT PRIMARY KEY,
    product_name    VARCHAR(100),
    category        VARCHAR(50),
    subcategory     VARCHAR(50),
    unit_price      DECIMAL(10,2)
);

-- Dimension: Regions
CREATE TABLE dim_regions (
    region_id       INT PRIMARY KEY,
    region_name     VARCHAR(50),
    state           VARCHAR(50),
    country         VARCHAR(50)
);

-- Dimension: Sales Reps
CREATE TABLE dim_sales_reps (
    rep_id          INT PRIMARY KEY,
    rep_name        VARCHAR(100),
    department      VARCHAR(50),
    region_id       INT REFERENCES dim_regions(region_id)
);

-- Dimension: Date
CREATE TABLE dim_date (
    date_id         INT PRIMARY KEY,
    full_date       DATE,
    year            INT,
    quarter         INT,
    month           INT,
    month_name      VARCHAR(20),
    week            INT,
    day_of_week     VARCHAR(20)
);

-- Fact: Sales Transactions
CREATE TABLE fact_sales (
    sale_id         INT PRIMARY KEY,
    date_id         INT REFERENCES dim_date(date_id),
    product_id      INT REFERENCES dim_products(product_id),
    region_id       INT REFERENCES dim_regions(region_id),
    rep_id          INT REFERENCES dim_sales_reps(rep_id),
    quantity        INT,
    unit_price      DECIMAL(10,2),
    discount_pct    DECIMAL(5,2),
    revenue         DECIMAL(12,2),
    cost            DECIMAL(12,2),
    profit          DECIMAL(12,2)
);

-- Fact: Sales Targets
CREATE TABLE fact_targets (
    target_id       INT PRIMARY KEY,
    region_id       INT REFERENCES dim_regions(region_id),
    product_id      INT REFERENCES dim_products(product_id),
    year            INT,
    month           INT,
    target_revenue  DECIMAL(12,2)
);
