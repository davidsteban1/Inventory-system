from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers import items, categories, inventory, transactions

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
    except Exception:
        pass  
    yield

app = FastAPI(
    title="Inventory Management System",
    lifespan=lifespan
)

# Routers
app.include_router(categories.router)
app.include_router(items.router)
app.include_router(inventory.router)
app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management System"}