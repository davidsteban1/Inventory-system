from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlmodel import Session, select, func
from database import get_session
from models import Item, Sale, SaleCreate, SaleInfo, InventoryMovement
from routers.auth import get_current_user
from datetime import datetime
from typing import Optional

app = FastAPI(
    title="Categories Inventory Management System"
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


# Sale generator


@router.post("/sales", response_model=Sale, status_code=status.HTTP_201_CREATED)
async def create_sale(
    cart: SaleCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    total_price = 0

    for cart_item in cart.items:
        item = session.get(Item, cart_item.item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
        if cart_item.qty > item.qty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough items available")

        total_price = total_price + (item.price * cart_item.qty)

    db_sale = Sale(total_price=total_price)

    session.add(db_sale)
    session.flush()

    for cart_item in cart.items:
        item = session.get(Item, cart_item.item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        
        item.qty = item.qty - cart_item.qty

        session.add(item)

        sold_items = SaleInfo(sale_id=db_sale.id, 
                            item_id=cart_item.item_id, 
                            qty=cart_item.qty, 
                            unit_price=item.price)

        session.add(sold_items)

        movement = InventoryMovement(item_id=cart_item.item_id,
                                    qty=cart_item.qty,
                                    type="sale")
        
        session.add(movement)
        
    session.commit()
    session.refresh(db_sale)

    return db_sale


# Sales revenue


@router.get("/sales/revenue", status_code=status.HTTP_200_OK)
async def get_sales_revenue(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):

    statement = select(Sale)

    if start_date:
        statement = statement.where(Sale.created_at >= start_date)
    if end_date:
        statement = statement.where(Sale.created_at <= end_date)
    
    sales = session.exec(statement).all()
    total_revenue = sum(sale.total_price for sale in sales)

    return {
        "total_sales_count": len(sales),
        "total_revenue": total_revenue
    }


# Reports 

@router.get("/sales/report", status_code=status.HTTP_200_OK)
async def get_sale_report(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):

    statement = (
        select(SaleInfo.item_id, func.sum(SaleInfo.qty).label("total_qty"))
        .join(Sale)
    )

    if start_date:
        statement = statement.where(Sale.created_at >= start_date)
    if end_date:
        statement = statement.where(Sale.created_at <= end_date)

    statement = statement.group_by(SaleInfo.item_id)
    statement = statement.order_by(func.sum(SaleInfo.qty).desc())

    sales = session.exec(statement).all()
    
    report = [
        {"item_id": item_id, "total_qty_sold": total_qty}
        for item_id, total_qty in sales
    ]
    
    return {"Best sellers": report}


# Find old sale 

@router.get("/sales/{id}", response_model=Sale, status_code=status.HTTP_200_OK)
async def get_sale(
    id: int, 
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    db_sale = session.get(Sale, id)
    if not db_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail=f"Sale with ID {id} not found")
    
    return db_sale


