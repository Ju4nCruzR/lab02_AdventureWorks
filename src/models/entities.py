from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class SaleEntity:
    order_id: int
    order_detail_id: int
    order_date: date
    customer_id: int
    product_id: int
    territory_id: int
    quantity: int
    unit_price: float
    unit_cost: float
    discount: float
    line_total: float
    is_online: bool

@dataclass
class CustomerEntity:
    customer_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    customer_type: str
    store_name: Optional[str]
    territory: Optional[str]
    country: Optional[str]
    first_purchase_date: Optional[date]

@dataclass
class ProductEntity:
    product_id: int
    product_name: str
    product_number: str
    category: Optional[str]
    subcategory: Optional[str]
    model: Optional[str]
    list_price: float
    standard_cost: float