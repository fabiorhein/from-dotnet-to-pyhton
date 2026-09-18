# From .NET to Python

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-black)

An opinionated backend learning project for a .NET developer with 20+ years of experience moving to Python. It translates familiar ASP.NET Core and EF Core concepts into a small, production-oriented FastAPI service.

## Stack

- **Python 3.12** with type hints and `async`/`await`
- **FastAPI** for HTTP endpoints, dependency injection, and OpenAPI
- **SQLAlchemy 2.0** with the async ORM and `asyncpg`
- **Pydantic** DTOs with strict validation as the API boundary
- **PostgreSQL** as the relational database
- **Docker** for local infrastructure

## Architecture

This is a **modular monolith**: each business module owns its API, DTOs, services, repositories, and models while sharing only infrastructure concerns.

```text
HTTP request
		|
		v
FastAPI API  -->  Pydantic DTOs  -->  Service  -->  Repository  -->  SQLAlchemy / PostgreSQL
									 (validation)      (rules)       (SQL/session)
```

The current `users` module demonstrates the separation:

| Layer | Responsibility | .NET equivalent |
| --- | --- | --- |
| `api.py` | Routes, HTTP status codes, dependency wiring | Controller / Minimal API |
| `schemas.py` | Request and response contracts | DTOs / model binding |
| `services.py` | Business rules and use cases | Application service |
| `repositories.py` | Queries, persistence, and session operations | Repository over `DbContext` |
| `models.py` | Database entities and domain behavior | EF Core entities |
| `shared/database.py` | Async engine, session factory, and transaction lifecycle | `DbContextOptions` + scoped `DbContext` |

### .NET mental model

- FastAPI dependency injection is the lightweight counterpart to ASP.NET Core DI.
- `AsyncSession` is the closest equivalent to an EF Core `DbContext`.
- SQLAlchemy `select()` replaces LINQ query expressions; `await session.execute()` executes them.
- Pydantic models handle boundary validation and serialization; SQLAlchemy models represent persistence.
- `flush()` makes changes available within the transaction; the request-scoped dependency commits or rolls back.

## Quick start

### 1. Create the environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn sqlalchemy asyncpg pydantic[email]
```

### 2. Start PostgreSQL with Docker

```bash
docker run --name from-dotnet-postgres \
	-e POSTGRES_USER=app_user \
	-e POSTGRES_PASSWORD=app_password \
	-e POSTGRES_DB=app_db \
	-p 5432:5432 \
	-d postgres:16
```

### 3. Run the API

```bash
uvicorn main:app --reload
```

Open the interactive API documentation at <http://127.0.0.1:8000/docs>.

The application creates the mapped tables during startup. The database connection currently defaults to:

```text
postgresql+asyncpg://app_user:app_password@localhost:5432/app_db
```

## User API

The sample module is available under `/api/users`:

- `POST /api/users` - register a user
- `GET /api/users?email=...` - find a user by email
- `GET /api/users/{user_id}` - find a user by ID
- `GET /api/users/all` - list users
- `GET /api/users/all/without-inactive` - list active users
- `PUT /api/users` - update a user
- `PATCH /api/users/{user_id}` - activate a user
- `DELETE /api/users/{user_id}` - deactivate a user

## Git strategy

```text
feature/*  ->  dev  ->  main
```

- `feature/*`: focused development branches.
- `dev`: integration branch for completed work and verification.
- `main`: production release branch; merge only from validated `dev` changes.

## Project layout

```text
.
├── main.py
└── src
		├── modules
		│   └── users
		│       ├── api.py
		│       ├── models.py
		│       ├── repositories.py
		│       ├── schemas.py
		│       └── services.py
		└── shared
				└── database.py

```