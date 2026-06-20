# Inventory Management System

![FastAPI](https://img.shields.io/badge/FastAPI-0.1.0-009688?logo=fastapi&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-Pydantic%20v2-7B42BC)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791?logo=postgresql&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-111827)

A lightweight, high-performance inventory API built with FastAPI for universal inventory management.  
It now includes category management, inventory movements (stock in/out), sales transactions, revenue and best-seller reports, and JWT-protected endpoints.

## Tech Stack

| Layer | Technology | Usage |
|---|---|---|
| **Web Framework** | FastAPI | High-performance Python REST API framework. |
| **ORM & Validation** | SQLModel (Pydantic v2) | Database mapping and strict type validation. |
| **Database** | PostgreSQL (Neon on AWS) | Serverless cloud relational data store. |
| **Configuration** | python-dotenv | Secure local environment variable isolation. |
| **ASGI Server** | Uvicorn | Fast production-ready server gateway. |
| **Authentication** | OAuth2 + JWT (python-jose) | Protects all business endpoints using bearer tokens. |

## Project Structure

```text
Inventory-system/
├── database.py          # Engine/session setup and startup table creation
├── main.py              # FastAPI app + router registration
├── models.py            # SQLModel entities: Category, Item, InventoryMovement, Sale, SaleInfo
├── requirements.txt     # Project dependencies
└── routers/
    ├── auth.py          # JWT validation dependency
    ├── categories.py    # Category endpoints
    ├── items.py         # Item endpoints
    ├── inventory.py     # Stock movement endpoints
    └── transactions.py  # Sales + reporting endpoints
```

## Database Configuration

Database tables are initialized automatically at application startup.  
The startup event calls `create_db_and_tables()`, which executes `SQLModel.metadata.create_all(engine)` to deploy and map missing structures automatically.

## API Endpoints

| Method | Route | Description |
|---|---|---|
| POST | `/categories/create-category` | Create a category. |
| GET | `/categories/categories-list` | List categories with pagination and optional `q` filter. |
| POST | `/items/create-item` | Create an item linked to a category. |
| GET | `/items/items-list` | List active items with pagination and optional `q` and `category_id` filters. |
| GET | `/items/item-by_id/{item_id}` | Get one active item by ID. |
| PUT | `/items/item-update/{item_id}` | Update an item by ID. |
| PATCH | `/items/delete-item/{item_id}` | Toggle item availability (soft delete/restore). |
| GET | `/items/inactive-items` | List inactive (soft deleted) items. |
| POST | `/inventory/add-stock` | Increase item quantity and record an input movement. |
| POST | `/inventory/reduce-stock` | Decrease item quantity and record an output movement. |
| POST | `/transactions/sales` | Create a sale from a cart, reduce stock, and register movements. |
| GET | `/transactions/sales/revenue` | Get sales count and total revenue (optional `start_date`, `end_date`). |
| GET | `/transactions/sales/report` | Best-seller report by quantity sold (optional date range). |
| GET | `/transactions/sales/{id}` | Fetch a sale by ID. |

## Authentication

All business routes above require a bearer token.  
`routers/auth.py` validates JWTs with:

- `SECRET`
- `ALGORITHM`
- `AUTH_SERVICE_URL` (used as `tokenUrl` in OAuth2PasswordBearer)

## API Preview (Swagger UI)
<img width="1154" height="369" alt="Inventory management system" src="https://github.com/user-attachments/assets/b7d1556a-c206-4ba4-91a9-b4607824f11d" />

## How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/davidsteban1/Inventory-system.git
   cd Inventory-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the database URL**
   ```bash
   export DATABASE_URL="postgresql://<user>:<password>@<host>/<db>?sslmode=require"
   ```
   Use your Neon PostgreSQL connection string as the `DATABASE_URL` value.

   Configure auth values too:
   ```bash
   export SECRET="<jwt-secret>"
   export ALGORITHM="HS256"
   export AUTH_SERVICE_URL="/auth/login"
   ```

4. **Run the API**
   ```bash
   uvicorn main:app --reload
   ```

5. **Open Swagger UI**
   - `http://127.0.0.1:8000/docs`
