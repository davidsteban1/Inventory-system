from fastapi import FastAPI, status, HTTPException, Depends
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import Item, ItemUpdate
from datetime import datetime
from typing import List, Optional
from auth import get_current_user


app = FastAPI(
    title="Inventory Management System",
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# See full products list

@app.get("/items", response_model=List[Item])
async def list_items(
    limit: int = 50,
    offset: int = 0,
    q: Optional[str] = None, 
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    statement = select(Item)
    if q:
        statement = statement.where(Item.name.contains(q))

    statement = statement.offset(offset).limit(limit)
    items = session.exec(statement).all()
    return items


# Create an item

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: Item, 
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    session.add(item)
    session.commit()
    session.refresh(item)
    return item


# Get item by ID

@app.get("/items/{item_id}", response_model=Item)
async def get_item(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return item


# Update product by ID 

@app.put("/items/{item_id}", response_model=Item)
async def update_item(
    item_id: int, 
    updated: ItemUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    item.name = updated.name
    item.brand = updated.brand
    item.sku = updated.sku
    item.qty = updated.qty
    item.cost = updated.cost
    item.price = updated.price

    session.add(item)
    session.commit()
    session.refresh(item)
    return item



# Delete product by ID 

@app.delete("/items/{item_id}")
async def delete_item(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):
    
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    session.delete(item)
    session.commit()
    return {"message": f"The {item.name} has been deleted successfully"}