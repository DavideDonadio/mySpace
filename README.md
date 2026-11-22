# mySpace

A personal tech blog and developer platform built with a decoupled architecture: a FastAPI backend serving a REST API and an Astro frontend with TypeScript and Tailwind CSS, fully containerized with Docker Compose.

## Architecture

- **Backend**: FastAPI, SQLAlchemy 2.0, PostgreSQL 17, Pydantic v2, PyJWT, Argon2 (`pwdlib`), managed with `uv`.
- **Frontend**: Astro, TypeScript, Tailwind CSS, SSR mode via `@astrojs/node`.
- **Infrastructure**: Docker Compose multi-container setup with automated health checks, isolated networks, and persistent database volumes.

```
mySpace/
├── compose.yaml   # Multi-container orchestration (DB, Backend, Frontend)
├── .env.example   # Environment template
│
├── backend/       # FastAPI application & Dockerfile
│   ├── app/
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── enums.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── Dockerfile
│   └── pyproject.toml
│
└── frontend/      # Astro blog application & Dockerfile
    ├── src/
    │   ├── pages/
    │   │   ├── index.astro
    │   │   └── posts/
    │   │       ├── index.astro
    │   │       └── [id].astro
    │   └── ...
    ├── Dockerfile
    └── package.json
```

## Features

- Full CRUD REST API with typed Pydantic request and response schemas.
- JWT-based authentication using Argon2 password hashing and PyJWT tokens.
- Role-based route protection: public read endpoints, token-protected write endpoints (`POST`, `PATCH`, `DELETE`).
- PostgreSQL 17 persistence via SQLAlchemy 2.0 ORM with automatic schema initialization.
- Server-side offset pagination (`page`, `limit`).
- Multiple tag support stored as JSON in PostgreSQL and rendered as badges.
- Cross-Origin Resource Sharing (CORS) configured for frontend communication.
- Dynamic page routing in Astro (`/posts/[id]`) with live data fetching from FastAPI.
- 1-command startup via Docker Compose with health checks and volume persistence.

## Getting Started

### Prerequisites

- Docker and Docker Compose

### 1. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

*(Optionally update passwords or secrets inside `.env`)*

### 2. Start the Stack

Run one command at the root of the project:

```bash
docker compose up --build
```

- **Frontend**: `http://localhost:4321`
- **Backend API**: `http://localhost:8000`
- **Interactive API Documentation (Swagger)**: `http://localhost:8000/docs`
- **PostgreSQL**: `localhost:5432`

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/posts` | List posts with pagination (`?page=1&limit=5`) | No |
| `POST` | `/posts` | Create a new post | Yes (Bearer JWT) |
| `GET` | `/posts/{id}` | Retrieve a post by ID | No |
| `PATCH` | `/posts/{id}` | Partially update an existing post | Yes (Bearer JWT) |
| `DELETE` | `/posts/{id}` | Remove a post (204 No Content) | Yes (Bearer JWT) |
| `POST` | `/auth/register` | Register a new user | No |
| `POST` | `/token` | Authenticate user and receive access token | No |
