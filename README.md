# mySpace

A personal tech blog and developer platform built with a decoupled architecture: a FastAPI backend serving a REST API and an Astro frontend with TypeScript and Tailwind CSS.

## Architecture

- **Backend**: FastAPI, SQLAlchemy 2.0, SQLite, Pydantic v2, managed with `uv`.
- **Frontend**: Astro, TypeScript, Tailwind CSS, SSR mode via `@astrojs/node`.

```
mySpace/
├── backend/       # FastAPI application and SQLite database
│   ├── app/
│   │   ├── database.py
│   │   ├── enums.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   └── pyproject.toml
│
└── frontend/      # Astro blog application
    ├── src/
    │   ├── pages/
    │   │   ├── index.astro
    │   │   └── posts/
    │   │       ├── index.astro
    │   │       └── [id].astro
    │   └── ...
    └── package.json
```

## Features

- Full CRUD REST API with typed Pydantic request and response schemas.
- SQLite persistence via SQLAlchemy ORM with automatic schema initialization.
- Server-side offset pagination (`page`, `limit`).
- Multiple tag support stored as JSON in SQLite and rendered as badges.
- Cross-Origin Resource Sharing (CORS) configured for frontend communication.
- Dynamic page routing in Astro (`/posts/[id]`) with live data fetching from FastAPI.

## Getting Started

### Prerequisites

- Python 3.12+ (tested with Python 3.15)
- uv package manager
- Node.js 20+ and npm

### 1. Run the Backend

```bash
cd backend
uv sync
uv run fastapi dev
```

The API will start at `http://127.0.0.1:8000`.
Interactive OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.

### 2. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will start at `http://localhost:4321`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/posts` | List posts with pagination (`?page=1&limit=5`) |
| `POST` | `/posts` | Create a new post |
| `GET` | `/posts/{id}` | Retrieve a post by ID |
| `PATCH` | `/posts/{id}` | Partially update an existing post |
| `DELETE` | `/posts/{id}` | Remove a post (204 No Content) |
