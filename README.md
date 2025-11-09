# Library API (FastAPI) — Book Library Management

Simple REST API to manage books, authors and borrowing records built with FastAPI and SQLite.

## Features
- User registration & JWT authentication
- CRUD for Authors and Books
- Borrow / Return workflows and borrowing history
- Search, pagination and basic filtering
- SQLite storage (default) and simple project layout

## Quick start (Windows)
1. Create and activate a venv:
   - PowerShell:
     ```
     python -m venv env
     .\env\Scripts\Activate.ps1
     ```
   - CMD:
     ```
     python -m venv env
     .\env\Scripts\activate.bat
     ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the app:
   ```
   .\env\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

4. Open docs:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc:       http://127.0.0.1:8000/redoc

## Run tests (smoke)
```
.\env\Scripts\python.exe -m unittest discover -v
```
Or run the specific smoke test:
```
.\env\Scripts\python.exe -m unittest tests.test_smoke -v
```

## API (summary)
Authentication
- POST /api/v1/auth/register
- POST /api/v1/auth/login

Authors (protected)
- POST /api/v1/authors
- GET /api/v1/authors?page=&size=
- GET /api/v1/authors/{author_id}

Books (protected)
- POST /api/v1/books
- GET /api/v1/books?search=&available=&page=&size=
- GET /api/v1/books/{book_id}
- PATCH /api/v1/books/{book_id}
- DELETE /api/v1/books/{book_id}

Borrowing (protected)
- POST /api/v1/borrow
- POST /api/v1/return/{record_id}
- GET /api/v1/borrow/history

Include the access token in Authorization header:
```
Authorization: Bearer <access_token>
```

## Configuration / Environment
Set environment variables (optional — defaults available in config):
- SECRET_KEY — JWT secret
- ACCESS_TOKEN_EXPIRE_MINUTES — token lifetime
- DATABASE_URL — e.g. sqlite:///./library.db

Default DB file: `library.db` in project root. To reset DB remove that file and restart.

## Postman
A Postman collection JSON was prepared (smoke flow). Save the JSON and import into Postman, then set environment variable `baseUrl` (default `http://127.0.0.1:8000`) and run requests.

## Notes
- Tests currently use the project DB. For isolated tests, switch to an in-memory DB and override DB dependency.
- For production, replace default SECRET_KEY and use a production-ready DB and HTTPS.
- Consider migrations (Alembic) and stronger password hashing (`bcrypt`) in production.

```
## Quick start (Windows)
1. Create and activate a venv:
   - PowerShell:
     ```
     python -m venv env
     .\env\Scripts\Activate.ps1
     ```
   - CMD:
     ```
     python -m venv env
     .\env\Scripts\activate.bat
     ```

    2. Install dependencies:
   
   pip install -r requirements.txt
   
    3. Run the app:
    
   .\env\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

## Run tests (smoke)
.\env\Scripts\python.exe -m unittest discover -

Or run the specific smoke test:

.\env\Scripts\python.exe -m unittest tests.test_smoke -v

## API (summary)
Authentication
- POST /api/v1/auth/register
- POST /api/v1/auth/login

Authors (protected)
- POST /api/v1/authors
- GET /api/v1/authors?page=&size=
- GET /api/v1/authors/{author_id}

Books (protected)
- POST /api/v1/books
- GET /api/v1/books?search=&available=&page=&size=
- GET /api/v1/books/{book_id}
- PATCH /api/v1/books/{book_id}
- DELETE /api/v1/books/{book_id}

Borrowing (protected)
- POST /api/v1/borrow
- POST /api/v1/return/{record_id}
- GET /api/v1/borrow/history

Include the access token in Authorization header:

Authorization: Bearer <access_token>
```

## Configuration / Environment
Set environment variables (optional — defaults available in config):
- SECRET_KEY — JWT secret
- ACCESS_TOKEN_EXPIRE_MINUTES — token lifetime
- DATABASE_URL — e.g. sqlite:///./library.db

Default DB file: `library.db` in project root. To reset DB remove that file and restart.

## Postman
A Postman collection JSON is present for testing.
