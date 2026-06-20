from fastapi import FastAPI
from database import create_db_and_tables
from routers import items, categories, inventory, transactions

app = FastAPI(
    title="Inventory Management System"
)


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

# Routers

app.include_router(categories.router)
app.include_router(items.router)
app.include_router(inventory.router)
app.include_router(transactions.router)

