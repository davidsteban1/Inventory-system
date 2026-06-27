# Inventory Management System

![FastAPI](https://img.shields.io/badge/FastAPI-0.1.0-009688?logo=fastapi&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-Pydantic%20v2-7B42BC)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791?logo=postgresql&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-111827)

A modular FastAPI inventory API for categories, items, stock movements, and sales transactions.

## Tech Stack

| Layer | Technology | Usage |
|---|---|---|
| **Web Framework** | FastAPI | REST API framework and dependency injection |
| **ORM & Validation** | SQLModel | Table models, request schemas, and query execution |
| **Database** | PostgreSQL | Relational persistence via SQLAlchemy engine |
| **Auth** | OAuth2 ****** JWT (`python-jose`) | Protected endpoints with token decoding |
| **ASGI Server** | Uvicorn | Local/production app server |

## Project Structure

```text
Inventory-system/
├── .gitignore
├── README.md
├── database.py
├── main.py
├── models.py
├── requirements.txt
├── verce,json
└── routers/
    ├── auth.py
    ├── categories.py
    ├── inventory.py
    ├── items.py
    └── transactions.py
```

## Architecture

- **Entrypoint and startup lifecycle**: `main.py` creates the FastAPI app and uses a lifespan handler to call `create_db_and_tables()` on startup.
- **Router composition**: app includes `categories`, `items`, `inventory`, and `transactions` routers.
- **Persistence layer**: `database.py` builds the SQLModel engine from `DATABASE_URL`, exposes `get_session()`, and creates tables with `SQLModel.metadata.create_all(engine)`.
- **Authentication dependency**: `routers/auth.py` defines `get_current_user()` using OAuth2 ****** extraction and JWT decoding (`SECRET`, `ALGORITHM`).

## Data Model

### Database tables

- `Category`: category catalog (`id`, `name`)
- `Item`: product record (`id`, `name`, `brand`, `sku`, `qty`, `cost`, `price`, `created_at`, `available`, `category_id`)
- `InventoryMovement`: stock movement log (`id`, `item_id`, `qty`, `type`, `created_at`)
- `Sale`: sale header (`id`, `total_price`, `created_at`)
- `SaleInfo`: sale line (`id`, `item_id`, `sale_id`, `qty`, `unit_price`)

### Request/update schemas

- `ItemUpdate`
- `SaleItemCreate`
- `SaleCreate`

### Foreign keys

- `Item.category_id -> category.id`
- `InventoryMovement.item_id -> item.id`
- `SaleInfo.item_id -> item.id`
- `SaleInfo.sale_id -> sale.id`

## API Endpoints

### Public

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/` | No | Health/welcome message |

### Categories

| Method | Route | Auth | Description |
|---|---|---|---|
| POST | `/categories/create-category` | Yes | Create category |
| GET | `/categories/categories-list` | Yes | List categories (supports `limit`, `offset`, `q`) |

### Items

| Method | Route | Auth | Description |
|---|---|---|---|
| POST | `/items/create-item` | Yes | Create item |
| GET | `/items/items-list` | Yes | List active items (supports `limit`, `offset`, `q`, `category_id`) |
| GET | `/items/item-by_id/{item_id}` | Yes | Get active item by ID |
| PUT | `/items/item-update/{item_id}` | Yes | Update item by ID |
| PATCH | `/items/delete-item/{item_id}` | Yes | Toggle active/inactive status |
| GET | `/items/inactive-items` | Yes | List inactive items |

### Inventory

| Method | Route | Auth | Description |
|---|---|---|---|
| POST | `/inventory/add-stock` | Yes | Increase item quantity |
| POST | `/inventory/reduce-stock` | Yes | Decrease item quantity |

### Transactions

| Method | Route | Auth | Description |
|---|---|---|---|
| POST | `/transactions/sales` | Yes | Create sale, reduce stock, create movement entries |
| GET | `/transactions/sales/revenue` | Yes | Revenue summary by optional date range |
| GET | `/transactions/sales/report` | Yes | Best-seller report by optional date range |
| GET | `/transactions/sales/{id}` | Yes | Get sale by ID |

## Authentication Flow

- Protected endpoints require `Authorization: ******
- Token is decoded with `python-jose` using `SECRET` and `ALGORITHM`.
- The JWT must include a `sub` claim (used as user email identity).
- `OAuth2PasswordBearer` points to an external login service URL:
  - Default: `https://authentication-and-login-system.vercel.app/userdb/login`
  - Override with `AUTH_SERVICE_URL`.
- This repository does **not** expose login/auth routes.

## Configuration

Set these environment variables before running:

- `DATABASE_URL` (required)
- `SECRET` (required)
- `ALGORITHM` (required)
- `AUTH_SERVICE_URL` (optional; defaults to external auth service)

Example:

```bash
export DATABASE_URL="postgresql://<user>:<password>@<host>/<db>?sslmode=require"
export SECRET="your-jwt-secret"
export ALGORITHM="HS256"
# Optional:
export AUTH_SERVICE_URL="https://authentication-and-login-system.vercel.app/userdb/login"
```

## How to Run

1. **Clone and enter the repository**
   ```bash
   git clone https://github.com/davidsteban1/Inventory-system.git
   cd Inventory-system
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Export required environment variables**
   ```bash
   export DATABASE_URL="postgresql://<user>:<password>@<host>/<db>?sslmode=require"
   export SECRET="your-jwt-secret"
   export ALGORITHM="HS256"
   ```

5. **Run the API**
   ```bash
   uvicorn main:app --reload
   ```

6. **Open API docs**
   - `http://127.0.0.1:8000/docs`

## Testing

Run:

```bash
python -m pytest
```

Current repository state may report `collected 0 items` because no test files are present.

## Deployment Note

The repository includes `verce,json` with a Vercel Python build route to `main.py`.

## Known Gaps / Notes

- `database.py` and `routers/auth.py` import `python-dotenv`; the app depends on it at runtime.
- Most business endpoints are protected and require a valid external JWT.
- Startup DB initialization errors are currently swallowed in `main.py` lifespan (`try/except` with `pass`), which can hide connection/setup failures at boot.
