from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, exclude=True)
    name: str
    brand: Optional[str]
    sku: Optional[str]
    qty: float = 0.0
    cost: float = 0.0       # Cost for the store
    price: float = 0.0      # Price for the customer
    created_at: Optional[str] = str(datetime.now())
    updated_at: Optional[str] = str(datetime.now())
