-- AdventureWorks OLAP Schema - Star Schema
-- Diseñado para responder las 4 preguntas de negocio

CREATE SCHEMA IF NOT EXISTS olap;

-- ============================================================
-- DIMENSIÓN FECHA
-- ============================================================
CREATE TABLE IF NOT EXISTS olap.dim_date (
    date_key        INTEGER NOT NULL PRIMARY KEY,
    full_date       DATE NOT NULL,
    day             SMALLINT NOT NULL,
    month           SMALLINT NOT NULL,
    month_name      VARCHAR(20) NOT NULL,
    quarter         SMALLINT NOT NULL,
    year            SMALLINT NOT NULL,
    week_of_year    SMALLINT NOT NULL,
    day_of_week     SMALLINT NOT NULL,
    day_name        VARCHAR(20) NOT NULL,
    is_weekend      BOOLEAN NOT NULL,
    year_month      VARCHAR(7) NOT NULL  -- formato YYYY-MM para cohortes
);

-- ============================================================
-- DIMENSIÓN CLIENTE
-- ============================================================
CREATE TABLE IF NOT EXISTS olap.dim_customer (
    customer_key        INTEGER NOT NULL PRIMARY KEY,
    customer_id         INTEGER NOT NULL,
    first_name          VARCHAR(100) NULL,
    last_name           VARCHAR(100) NULL,
    full_name           VARCHAR(200) NULL,
    email               VARCHAR(100) NULL,
    customer_type       VARCHAR(20) NOT NULL,  -- 'Individual' o 'Store'
    store_name          VARCHAR(100) NULL,
    territory           VARCHAR(100) NULL,
    country             VARCHAR(100) NULL,
    first_purchase_date DATE NULL,             -- para análisis de cohortes
    cohort_year_month   VARCHAR(7) NULL        -- formato YYYY-MM
);

-- ============================================================
-- DIMENSIÓN PRODUCTO
-- ============================================================
CREATE TABLE IF NOT EXISTS olap.dim_product (
    product_key         INTEGER NOT NULL PRIMARY KEY,
    product_id          INTEGER NOT NULL,
    product_name        VARCHAR(200) NOT NULL,
    product_number      VARCHAR(50) NOT NULL,
    category            VARCHAR(100) NULL,
    subcategory         VARCHAR(100) NULL,
    model               VARCHAR(100) NULL,
    color               VARCHAR(50) NULL,
    size                VARCHAR(50) NULL,
    weight              NUMERIC(8,2) NULL,
    list_price          NUMERIC(19,4) NULL,
    standard_cost       NUMERIC(19,4) NULL
);

-- ============================================================
-- DIMENSIÓN TERRITORIO
-- ============================================================
CREATE TABLE IF NOT EXISTS olap.dim_territory (
    territory_key       INTEGER NOT NULL PRIMARY KEY,
    territory_id        INTEGER NOT NULL,
    territory_name      VARCHAR(100) NOT NULL,
    country_region      VARCHAR(100) NOT NULL,
    territory_group     VARCHAR(100) NOT NULL
);

-- ============================================================
-- TABLA DE HECHOS - VENTAS
-- ============================================================
CREATE TABLE IF NOT EXISTS olap.fact_sales (
    sale_key            BIGSERIAL NOT NULL PRIMARY KEY,
    order_id            INTEGER NOT NULL,
    order_detail_id     INTEGER NOT NULL,
    date_key            INTEGER NOT NULL REFERENCES olap.dim_date(date_key),
    customer_key        INTEGER NOT NULL REFERENCES olap.dim_customer(customer_key),
    product_key         INTEGER NOT NULL REFERENCES olap.dim_product(product_key),
    territory_key       INTEGER NOT NULL REFERENCES olap.dim_territory(territory_key),
    order_quantity      SMALLINT NOT NULL,
    unit_price          NUMERIC(19,4) NOT NULL,
    unit_cost           NUMERIC(19,4) NOT NULL,
    discount_amount     NUMERIC(19,4) NOT NULL,
    line_total          NUMERIC(19,4) NOT NULL,
    line_cost           NUMERIC(19,4) NOT NULL,
    line_margin         NUMERIC(19,4) NOT NULL,
    margin_pct          NUMERIC(8,4) NULL,
    order_date          DATE NOT NULL,
    due_date            DATE NULL,
    ship_date           DATE NULL,
    is_online_order     BOOLEAN NOT NULL
);