from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime


# Category

class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)


# Items

class Item(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    brand: Optional[str]
    sku: Optional[str]
    qty: float 
    cost: float       # Cost for the store
    price: float      # Price for the customer
    created_at: datetime = Field(default_factory=datetime.utcnow)
    available: bool = Field(default=True)
    category_id: int = Field(foreign_key="category.id")


class ItemUpdate(SQLModel):
    name: str
    brand: Optional[str]
    sku: Optional[str]
    cost: float
    price: float


# Inventory & Transactions

class InventoryMovement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    qty: float
    type: str 
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Sale(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    total_price: float 
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SaleInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    sale_id: int = Field(foreign_key="sale.id")
    qty: float
    unit_price: float


class SaleItemCreate(SQLModel):
    item_id: int
    qty: float


class SaleCreate(SQLModel):
    items: List[SaleItemCreate]