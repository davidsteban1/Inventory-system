from fastapi import FastAPI, status, Depends, APIRouter
from sqlmodel import Session, select, col
from database import get_session
from models import Category
from typing import Optional
from routers.auth import get_current_user


app = FastAPI(
    title="Categories Inventory Management System"
)

router = APIRouter(prefix="/categories", tags=["Categories"])



# Create new category

@router.post("/create-category", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: Category, 
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    session.add(category)
    session.commit()
    session.refresh(category)
    return category


# See caterogies

@router.get("/categories-list", response_model=list[Category])
async def list_category(
    limit: int = 20,
    offset: int = 0,
    q: Optional[str] = None, 
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):

    statement = select(Category)
    if q:
        statement = statement.where(col.Category.name.contains(q))

    statement = statement.offset(offset).limit(limit)
    categories = session.exec(statement).all()
    return categories

