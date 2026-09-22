# From .NET to Python

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-FastMCP-6E56CF)
![License](https://img.shields.io/badge/license-MIT-black)

A full-stack learning project designed for .NET developers transitioning to Python. It brings the familiar concepts of ASP.NET Core, EF Core, and layered architecture into a FastAPI + SQLAlchemy backend, with a Vue 3 frontend and MCP integrations.

## Why this project exists

This repository is a guided migration path from the .NET mindset to Python. Instead of jumping directly into framework-specific conventions, it mirrors the mental model many .NET developers already know:

- controllers vs. route handlers
- DTOs vs. Pydantic schemas
- repository patterns vs. SQLAlchemy session access
- service layer vs. application services
- unit of work vs. transactional boundaries
- modular monolith vs. organized feature packages

The project is intentionally small but production-minded: clear abstractions, validation at the boundary, async persistence, modular organization, and support for agent-driven interfaces through Model Context Protocol (MCP).

## What is included

- Async FastAPI application with a clear API entry point
- SQLAlchemy 2.0 async ORM with PostgreSQL
- Pydantic validation and typed DTOs
- Layered architecture based on modules and shared infrastructure
- User CRUD and query use cases
- Pagination contract patterns
- MCP server for business-domain tools
- MCP server powered by FastAPI OpenAPI export
- JWT authentication with hashed passwords
- Vue 3 frontend with Vite, TypeScript, Pinia, Vue Router, and Tailwind CSS
- Protected frontend routes for login and user management
- Local database setup with Docker

## Architecture overview

This project follows a modular monolith approach in the backend: each business module owns its HTTP layer, DTO contracts, business logic, repositories, and model definitions, while shared infrastructure stays centralized. The frontend consumes the backend through its REST API.

```text
HTTP request
    |
    v
FastAPI API --> Pydantic schemas --> Service --> Repository --> SQLAlchemy / PostgreSQL
                                 (validation)      (rules)       (session + SQL)
```

### Module responsibilities

| Layer | Responsibility | .NET equivalent |
| --- | --- | --- |
| `backend/src/modules/users/api.py` | Route definitions and HTTP responses | Controller / Minimal API |
| `backend/src/modules/users/schemas.py` | Request/response models | DTOs / model binding |
| `backend/src/modules/users/services.py` | Business rules and orchestration | Application service |
| `backend/src/modules/users/repositories.py` | Persistence and queries | Repository |
| `backend/src/modules/users/models.py` | Database entities | EF Core entities |
| `backend/src/shared/database.py` | Session factory and engine setup | DbContext configuration |
| `backend/src/shared/schemas.py` | Shared pagination contracts | Shared DTOs |
| `backend/src/shared/uow.py` | Transaction boundaries | Unit of Work |
| `frontend/src/modules/auth` | Login view and authentication flow | Client-side auth UI |
| `frontend/src/modules/users` | User management views | Client-side feature module |
| `frontend/src/services/api.ts` | Axios client and JWT handling | HTTP client |
| `frontend/src/stores/auth.ts` | Authentication state and token persistence | Client-side state |

### .NET mental model in Python

- FastAPI dependency injection is the lightweight counterpart to ASP.NET Core DI.
- `AsyncSession` is the closest analogue to a scoped EF Core `DbContext`.
- `select()` replaces LINQ-style query composition, and `await session.execute()` executes the statement.
- Pydantic models validate external input and enforce boundary contracts.
- SQLAlchemy models represent persistence structure instead of application-level models.
- `flush()` stages changes inside the transaction, while the service layer decides when to commit or rollback.
- Read operations use the request-scoped session and write operations control the transaction boundary explicitly.

## Tech stack

- Python 3.12
- FastAPI
- SQLAlchemy 2.0 with async support
- Pydantic v2
- PostgreSQL 16
- asyncpg
- Docker
- Ruff
- MyPy
- MCP / FastMCP
- Node.js and npm
- Vue 3, Vite, TypeScript, Pinia, Vue Router, and Tailwind CSS

## Project structure

```text
.
├── LICENSE
├── README.md
├── backend
│   ├── .env.example
│   ├── alembic.ini
│   ├── main.py
│   ├── migrations
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── src
│       ├── mcp
│       ├── modules
│       │   ├── auth
│       │   └── users
│       └── shared
└── frontend
  ├── .env.example
  ├── package.json
  └── src
    ├── modules
    │   ├── auth
    │   └── users
    ├── router
    ├── services
    └── stores
```

## Prerequisites

Before running the project locally, make sure you have:

- Python 3.12+
- PostgreSQL or Docker available
- `pip` and a virtual environment tool
- Optional: access to an MCP client for testing the protocol servers

## Quick start

### 1. Set up the backend

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

Update the database connection string and `SECRET_KEY` in `backend/.env` if needed. The application reads `DATABASE_URL` from the environment:

```text
postgresql+asyncpg://usuario:password@localhost:5432/database_name
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
cd backend
uvicorn main:app --reload
```

The API will be available at:

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

The application creates its mapped tables during startup using the configured `DATABASE_URL`. The API enables CORS for the default Vite development origins (`localhost:5173` and `127.0.0.1:5173`).

### 4. Set up and run the frontend

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

`VITE_API_URL` defaults to `http://localhost:8000/api`. Change it in `frontend/.env` when the API uses another URL.

The frontend is available at http://localhost:5173. The `/users` route requires a valid JWT and unauthenticated users are redirected to `/login`.

### 5. Run project checks

```bash
cd backend
ruff check .
mypy --explicit-package-bases main.py src
```

For frontend checks and a production build:

```bash
cd frontend
npm run build
```

Keep both `.env.example` files versioned and use local `.env` files only for machine-specific configuration.

## MCP integration

This project includes two MCP server patterns built with FastMCP, each serving a different purpose.

### 1. MCP domain server

File: `backend/src/mcp/server.py`

This server exposes business-oriented tools directly against the application service and repository layer. It is useful when an agent should work with the system's actual business rules.

Run it with:

```bash
python -m src.mcp.server
```

Available tools:

- `list_users(page: int = 1, size: int = 10)`
- `find_user_by_email(email: str)`
- `register_new_user(name: str, email: str, password: str)`

This is the ideal option for use cases where the agent should operate close to the domain logic instead of through HTTP calls.

### 2. MCP OpenAPI server

File: `backend/src/mcp/openapi.py`

This server reads the FastAPI OpenAPI document and creates MCP tools automatically for each API operation. It converts the public HTTP contract into tool-accessible actions without manually writing one tool per route.

Typical startup flow:

```bash
cd backend
uvicorn main:app --reload
python -m src.mcp.openapi
```

It expects the API to be running at:

- http://127.0.0.1:8000/openapi.json
- http://127.0.0.1:8000

This approach is ideal when the agent must consume the application through the public REST interface as a standard MCP client.

### Recommended usage

- Use the domain MCP server when you want direct access to business logic and persistence behavior.
- Use the OpenAPI MCP server when you want a thin wrapper over the public API surface.

## User API

The sample module exposes operations under `/api/users`:

- `POST /api/users` - register a user
- `GET /api/users/by-email?email=...` - find a user by email
- `GET /api/users?page=1&size=10` - list users with pagination
- `GET /api/users/{user_id}` - find a user by ID
- `GET /api/users/all` - list all users
- `GET /api/users/all/without-inactive` - list active users
- `PUT /api/users` - update a user
- `PATCH /api/users/{user_id}` - activate a user
- `DELETE /api/users/{user_id}` - deactivate a user

### Pagination contract

The paginated response format is:

```json
{
  "items": [],
  "page": 1,
  "size": 10,
  "total_items": 0,
  "total_pages": 0
}
```

Supported query parameters:

| Parameter | Default | Constraints | Description |
| --- | ---: | --- | --- |
| `page` | `1` | Minimum `1` | Page number |
| `size` | `10` | Between `1` and `100` | Number of items per page |

User lookup operations return `404 Not Found` if the requested record does not exist.

## Authentication

Authentication is provided by the backend at `POST /api/auth/token`. It accepts OAuth2 form data (`username` is the user's email and `password` is the user's password) and returns a JWT access token:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

Protected user endpoints require the token in the request header:

```text
Authorization: Bearer <jwt>
```

The frontend login view submits these credentials, stores the token in `localStorage`, adds it to API requests, and redirects to `/login` after a `401 Unauthorized` response.

## Development workflow

### Git strategy

```text
feature/*  ->  dev  ->  main
```

- `feature/*`: focused work on isolated improvements
- `dev`: integration branch for validated changes
- `main`: release branch for stable production-ready code

### Contribution guidelines

- Keep changes focused and aligned with the current module structure
- Add or update documentation when behavior or onboarding changes
- Prefer explicit validation and clear service boundaries
- Avoid committing secrets, credentials, or generated local files
- Keep the project consistent with the established .NET-to-Python mental model

## Roadmap

Possible next steps for the project include:

- additional business modules beyond users
- Docker Compose for full local environment orchestration
- observability and structured logging
- tests for repositories, services, API endpoints, and frontend flows
- complete user management operations in the frontend
- more advanced MCP integrations and tool chaining

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## About the project

This repository is a learning and reference project for developers who already understand layered architecture from the .NET world and want to see the same patterns applied in Python with modern tools and best practices.
