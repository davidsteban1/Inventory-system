from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlmodel import Session, select, col
from database import get_session
from models import Category, Item, ItemUpdate
from typing import Optional
from routers.auth import get_current_user


app = FastAPI(
    title="Items Inventory Management System"
)

router = APIRouter(prefix="/items", tags=["Items"])



# Create an item

@router.post("/create-item", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: Item, 
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    db_category = session.get(Category, item.category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist")

    session.add(item)
    session.commit()
    session.refresh(item)
    
    return {"message": f"The {item.name} has been created successfully"}


# See products list by category

@router.get("/items-list", response_model=list[Item])
async def list_items(
    limit: int = 50,
    offset: int = 0,
    q: Optional[str] = None, 
    category_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    statement = select(Item).where(Item.available == True)
    if q:
        statement = statement.where(col.Item.name.contains(q))
    if category_id:
        statement = statement.where(Item.category_id == category_id)
    
    statement = statement.offset(offset).limit(limit)
    items = session.exec(statement).all()
    
    return items


# Get item by ID

@router.get("/item-by_id/{item_id}", response_model=Item)
async def get_item(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    item = session.get(Item, item_id)
    if not item or item.available == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    return item


# Update product by ID 

@router.put("/item-update/{item_id}", response_model=Item)
async def update_item(
    item_id: int, 
    updated: ItemUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    item = session.get(Item, item_id)
    if not item or item.available == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    item.name = updated.name
    item.brand = updated.brand
    item.sku = updated.sku
    item.cost = updated.cost
    item.price = updated.price

    session.add(item)
    session.commit()
    session.refresh(item)
    
    return {"message": f"The {item.name} has been updated successfully"}


# "Delete" product by ID / T or F

@router.patch("/delete-item/{item_id}")
async def status_item(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):
    
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    item.available = not item.available
    if item.available == True:
        current_status = "activated"
    else:
        current_status = "deactivated"
        
    session.add(item)
    session.commit()
    session.refresh(item) 

    return {"message": f"The {item.name} has been {current_status} successfully"}


# See inactive (deleted) items

@router.get("/inactive-items", response_model=list[Item])
async def list_inactive_items(
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    statement = select(Item).where(Item.available == False)
    statement = statement.offset(offset).limit(limit)
    
    inactive_items = session.exec(statement).all()
    
    return inactive_items
