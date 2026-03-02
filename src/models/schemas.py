from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date, SmallInteger, BigInteger
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class DimDate(Base):
    __tablename__ = 'dim_date'
    __table_args__ = {'schema': 'olap'}
    date_key = Column(Integer, primary_key=True)
    full_date = Column(Date)
    day = Column(SmallInteger)
    month = Column(SmallInteger)
    month_name = Column(String)
    quarter = Column(SmallInteger)
    year = Column(SmallInteger)
    week_of_year = Column(SmallInteger)
    day_of_week = Column(SmallInteger)
    day_name = Column(String)
    is_weekend = Column(Boolean)
    year_month = Column(String)

class DimCustomer(Base):
    __tablename__ = 'dim_customer'
    __table_args__ = {'schema': 'olap'}
    customer_key = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    full_name = Column(String)
    email = Column(String)
    customer_type = Column(String)
    store_name = Column(String)
    territory = Column(String)
    country = Column(String)
    first_purchase_date = Column(Date)
    cohort_year_month = Column(String)

class DimProduct(Base):
    __tablename__ = 'dim_product'
    __table_args__ = {'schema': 'olap'}
    product_key = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    product_name = Column(String)
    product_number = Column(String)
    category = Column(String)
    subcategory = Column(String)
    model = Column(String)
    color = Column(String)
    size = Column(String)
    weight = Column(Numeric)
    list_price = Column(Numeric)
    standard_cost = Column(Numeric)

class DimTerritory(Base):
    __tablename__ = 'dim_territory'
    __table_args__ = {'schema': 'olap'}
    territory_key = Column(Integer, primary_key=True)
    territory_id = Column(Integer)
    territory_name = Column(String)
    country_region = Column(String)
    territory_group = Column(String)

class FactSales(Base):
    __tablename__ = 'fact_sales'
    __table_args__ = {'schema': 'olap'}
    sale_key = Column(BigInteger, primary_key=True)
    order_id = Column(Integer)
    order_detail_id = Column(Integer)
    date_key = Column(Integer)
    customer_key = Column(Integer)
    product_key = Column(Integer)
    territory_key = Column(Integer)
    order_quantity = Column(SmallInteger)
    unit_price = Column(Numeric)
    unit_cost = Column(Numeric)
    discount_amount = Column(Numeric)
    line_total = Column(Numeric)
    line_cost = Column(Numeric)
    line_margin = Column(Numeric)
    margin_pct = Column(Numeric)
    order_date = Column(Date)
    due_date = Column(Date)
    ship_date = Column(Date)
    is_online_order = Column(Boolean)