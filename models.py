from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    brand: Optional[str]
    sku: Optional[str]
    qty: float 
    cost: float       # Cost for the store
    price: float      # Price for the customer
    created_at: Optional[str] = str(datetime.now())


class ItemUpdate(SQLModel):
    name: str
    brand: Optional[str]
    sku: Optional[str]
    qty: float
    cost: float
    price: float