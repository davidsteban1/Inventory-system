# Inventory Management System

![FastAPI](https://img.shields.io/badge/FastAPI-0.1.0-009688?logo=fastapi&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-Pydantic%20v2-7B42BC)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791?logo=postgresql&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-111827)

A lightweight, high-performance inventory API built with FastAPI for universal inventory management.  
It provides full CRUD operations, automatic ID generation via PostgreSQL primary keys, pagination, and global search functionality.

## Tech Stack

| Layer | Technology | Usage |
|---|---|---|
| **Web Framework** | FastAPI | High-performance Python REST API framework. |
| **ORM & Validation** | SQLModel (Pydantic v2) | Database mapping and strict type validation. |
| **Database** | PostgreSQL (Neon on AWS) | Serverless cloud relational data store. |
| **Configuration** | python-dotenv | Secure local environment variable isolation. |
| **ASGI Server** | Uvicorn | Fast production-ready server gateway. |

## Project Structure

```text
Inventory-system/
├── .env                 # Private environment variables & database credentials
├── .gitignore           # Specifies intentionally untracked files to ignore (e.g., .env, venv)
├── database.py          # Neon engine connection, session lifetime & startup table schema migration
├── main.py              # FastAPI application definitions, configuration, and CRUD HTTP endpoints
├── models.py            # SQLModel schema definition for the Item entity mapped to PostgreSQL
├── requirements.txt     # List of project dependencies for easy environment replication
└── venv/                # Isolated local Python virtual environment (hidden via .gitignore)
```

## Database Configuration

Database tables are initialized automatically at application startup.  
The startup event calls `create_db_and_tables()`, which executes `SQLModel.metadata.create_all(engine)` to deploy and map missing structures automatically.

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/items` | List items with optional query parameters: `limit` (default `50`), `offset` (default `0`), and `q` (partial name search). |
| POST | `/items` | Create a new item. |
| GET | `/items/{item_id}` | Get a single item by ID. |
| PUT | `/items/{item_id}` | Update an existing item by ID. |
| DELETE | `/items/{item_id}` | Delete an item by ID. |

## API Preview (Swagger UI)
<img width="1154" height="369" alt="Inventory management system" src="https://github.com/user-attachments/assets/013f56f2-765e-4d4f-873a-aaa4cf4fa804" />

## How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/davidsteban1/Inventory-system.git
   cd Inventory-system
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi sqlmodel uvicorn psycopg2-binary
   ```

3. **Configure the database URL**
   ```bash
   export DATABASE_URL="postgresql://<user>:<password>@<host>/<db>?sslmode=require"
   ```
   Use your Neon PostgreSQL connection string as the `DATABASE_URL` value.

4. **Run the API**
   ```bash
   uvicorn main:app --reload
   ```

5. **Open Swagger UI**
   - `http://127.0.0.1:8000/docs`
