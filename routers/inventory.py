from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlmodel import Session
from database import get_session
from models import Item, InventoryMovement
from routers.auth import get_current_user


app = FastAPI(
    title="Inven Inventory Management System"
)

router = APIRouter(prefix="/inventory", tags=["Inventory"])


# Add stock

@router.post("/add-stock", response_model=InventoryMovement, status_code=status.HTTP_202_ACCEPTED)
async def add_stock(
    item_id: int,
    qty: float,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item does not exist")


    item.qty += qty
    movement = InventoryMovement(item_id=item_id,
                                qty=qty,
                                type="input")

    session.add(item)
    session.add(movement)
    session.commit()
    session.refresh(movement)
    
    return movement 


# Reduce stock 

@router.post("/reduce-stock", response_model=InventoryMovement, status_code=status.HTTP_202_ACCEPTED)
async def reduce_stock(
    item_id: int,
    qty: float,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item does not exist")
        
    item_reduce = qty
    if qty > item.qty:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't reduce inventory not available")
    else:    
        item.qty -= qty

    movement = InventoryMovement(item_id=item_id, 
                                qty=qty,
                                type="output")

    session.add(item)
    session.add(movement)
    session.commit()
    session.refresh(movement)
    
    return movement