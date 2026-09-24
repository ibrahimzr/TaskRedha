# Task 2 — Book Store API

This is a single runnable code task that combines the three Task 2 stages:

1. Core API: users, login, JWT, roles, books and orders.
2. Database stage: PostgreSQL, Docker, authors, profiles, genres, relationships, joins and indexes.
3. Testing stage: pytest, TestClient, permissions, ownership, stock rules and relationship tests.

## Structure

```text
Task 2/
├── .env.example
├── .gitignore
├── requirements.txt
├── main.py
├── create_admin.py
├── database/
│   ├── schema.sql
│   └── create_test_db.sql
├── app/
│   ├── config.py
│   ├── database.py
│   ├── enums.py
│   ├── models.py
│   ├── security.py
│   ├── dependencies.py
│   ├── dtos/
│   │   ├── requests.py
│   │   └── responses.py
│   └── routers/
│       ├── auth.py
│       ├── users.py
│       ├── authors.py
│       ├── genres.py
│       ├── books.py
│       └── orders.py
└── tests/
    ├── conftest.py
    ├── test_dtos.py
    ├── test_security.py
    ├── test_auth.py
    ├── test_books.py
    ├── test_orders.py
    └── test_relationships.py
```

## 1. Create venv and install

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Start PostgreSQL in Docker

```powershell
docker run --name bookstore-db -e POSTGRES_PASSWORD=devpassword -e POSTGRES_DB=bookstore -p 5432:5432 -d postgres:16
```

If the container already exists:

```powershell
docker start bookstore-db
```

## 3. Create `.env`

Copy `.env.example` to `.env` and replace `SECRET_KEY` with a long random value.

Generate one with:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

## 4. Create the first admin

```powershell
python create_admin.py
```

## 5. Run the API

```powershell
python -m uvicorn main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## 6. Test database

Create it once:

```powershell
docker exec bookstore-db psql -U postgres -c "CREATE DATABASE bookstore_test;"
```

Then run:

```powershell
pytest -v
```

## Roles

- customer: browse, order, see own orders.
- staff: customer abilities + manage authors, genres, books and order status.
- admin: staff abilities + manage users and delete protected resources.

## Main relationships

- Author -> Books: one-to-many.
- Author -> AuthorProfile: one-to-one.
- Book <-> Genre: many-to-many through `book_genre`.
- User -> Orders: one-to-many.
- Book -> Orders: one-to-many.

## Note about the source guides

The testing guide starts from the earlier pre-relational book shape, while the database guide later changes books to use `author_id` and `genre_ids`. In this combined version, the tests were adapted to the final relational schema so the three stages work together as one project.
