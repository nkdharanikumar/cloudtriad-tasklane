# Tasklane — Task Management App

A 3-tier task management application:

```
React (Vite)  →  Flask REST API  →  PostgreSQL
```

This README only covers running the app locally. Docker, Kubernetes, EKS,
GitOps, CI/CD, and monitoring are intentionally **not** included here — that's
the next stage you'll build yourself on top of this.

---

## 1. Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- PostgreSQL 14+ (running locally, or accessible over the network)

---

## 2. Set up PostgreSQL locally

Create a database and a user for the app (adjust names/password as you like —
just make sure they match your `.env` files in step 3).

```bash
sudo -u postgres psql
```

```sql
CREATE USER taskuser WITH PASSWORD 'taskpassword';
CREATE DATABASE taskdb OWNER taskuser;
\q
```

---

## 3. Configure environment variables

**Backend** — copy the example file and adjust if needed:

```bash
cd backend
cp .env.example .env
```

`backend/.env`:

| Variable       | Default                                                   | Description                              |
|----------------|------------------------------------------------------------|-------------------------------------------|
| `DB_HOST`      | `localhost`                                                | PostgreSQL host                          |
| `DB_PORT`      | `5432`                                                      | PostgreSQL port                          |
| `DB_NAME`      | `taskdb`                                                    | Database name                            |
| `DB_USER`      | `taskuser`                                                  | Database user                            |
| `DB_PASSWORD`  | `taskpassword`                                              | Database password                        |
| `FLASK_ENV`    | `development`                                               | Flask environment                        |
| `FLASK_DEBUG`  | `true`                                                      | Enable Flask debug/reload                |
| `SECRET_KEY`   | `dev-secret-key-change-me`                                  | Flask secret key                         |
| `FLASK_RUN_HOST` | `0.0.0.0`                                                 | Bind host                                |
| `FLASK_RUN_PORT` | `5000`                                                    | Bind port                                |
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173`               | Comma-separated allowed frontend origins |

**Frontend** — copy the example file:

```bash
cd frontend
cp .env.example .env
```

`frontend/.env`:

| Variable            | Default                 | Description                     |
|---------------------|--------------------------|----------------------------------|
| `VITE_API_BASE_URL` | `http://localhost:5000`  | Base URL the frontend calls the API on |

Change `VITE_API_BASE_URL` later when you deploy the backend somewhere else
(behind an ALB, a Kubernetes Service, etc.) — no code changes needed.

---

## 4. Initialize the database

From the `backend` directory (so its virtualenv has `psycopg2` installed —
see step 5 first), run one of:

**Option A — Python script (recommended, uses the same env vars as the app):**

```bash
cd database
python init_db.py            # schema only
python init_db.py --seed     # schema + sample tasks
```

**Option B — plain SQL with psql:**

```bash
psql -h localhost -U taskuser -d taskdb -f database/init.sql
psql -h localhost -U taskuser -d taskdb -f database/seed.sql   # optional sample data
```

The sample data is just a starting point — edit or delete `database/seed.sql`,
or delete the rows from the UI, at any time.

---

## 5. Start the Flask backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

The API starts on `http://localhost:5000` by default. Check it's healthy:

```bash
curl http://localhost:5000/health
# {"status": "healthy", "database": "connected"}
```

---

## 6. Start the React frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser. You should see the dashboard
with stats, filters, and your tasks (or an empty state if you skipped
seeding).

---

## 7. Test the application

- Open the dashboard and create, edit, and delete a few tasks.
- Change a task's status directly from its card and watch the stats update.
- Use the search box and status/priority filters.
- Stop PostgreSQL and reload — the app should show a clear "couldn't load
  tasks" error instead of crashing, and `/health` should report `degraded`.

Backend unit tests (validation logic + health check):

```bash
cd backend
pytest tests/ -v
```

---

## 8. API reference

Base URL: `http://localhost:5000` (configurable via `frontend/.env`)

### Health

| Method | Path      | Description                              |
|--------|-----------|-------------------------------------------|
| GET    | `/health` | Returns `{"status": "healthy"}` (or `"degraded"` if the DB is unreachable) |

### Tasks

| Method | Path              | Description                                  |
|--------|-------------------|------------------------------------------------|
| GET    | `/api/tasks`      | List tasks. Supports query params: `status`, `priority`, `search`, `sort_by`, `order` |
| GET    | `/api/tasks/<id>` | Get a single task                             |
| POST   | `/api/tasks`      | Create a task                                 |
| PUT    | `/api/tasks/<id>` | Update a task (partial updates supported)     |
| DELETE | `/api/tasks/<id>` | Delete a task                                 |

**Task object:**

```json
{
  "id": 1,
  "title": "Set up Kubernetes cluster",
  "description": "Provision a local or cloud cluster.",
  "status": "IN_PROGRESS",
  "priority": "HIGH",
  "due_date": "2026-08-20",
  "created_at": "2026-08-15T06:00:00Z",
  "updated_at": "2026-08-15T06:00:00Z"
}
```

Valid `status` values: `TODO`, `IN_PROGRESS`, `COMPLETED`
Valid `priority` values: `LOW`, `MEDIUM`, `HIGH`

**Example — create a task:**

```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Write API docs", "priority": "LOW"}'
```

**Example — filter and search:**

```bash
curl "http://localhost:5000/api/tasks?status=TODO&search=kubernetes"
```

### Stats

| Method | Path         | Description                                    |
|--------|--------------|--------------------------------------------------|
| GET    | `/api/stats` | Returns `total_tasks`, `pending_tasks`, `in_progress_tasks`, `completed_tasks`, `completion_rate` |

### Error responses

All errors return JSON with an `error` field and an appropriate status code:

```json
{ "error": "Task with id 42 not found." }
```

| Code | Meaning                                             |
|------|-------------------------------------------------------|
| 200  | Success                                                |
| 201  | Created                                                |
| 400  | Bad request (missing title, invalid status/priority, malformed JSON) |
| 404  | Task not found                                         |
| 500  | Server error (e.g. database unavailable)               |

---

## Project structure

```
backend/
├── app/
│   ├── __init__.py       # Flask app factory, CORS, blueprint registration
│   ├── config.py         # Env-var based configuration
│   ├── routes/           # tasks.py, stats.py, health.py
│   ├── models/           # task.py — validation + SQL queries
│   └── database/         # db.py — connection pool + cursor context manager
├── tests/
├── requirements.txt
├── .env.example
└── run.py

frontend/
├── src/
│   ├── components/       # StatsBar, FilterBar, TaskList, TaskCard, modals, toast
│   ├── pages/             # Dashboard.jsx
│   ├── services/api.js    # Fetch wrapper for the Flask API
│   ├── App.jsx
│   └── main.jsx
├── package.json
├── vite.config.js
└── .env.example

database/
├── init.sql               # Schema (tasks table, indexes, updated_at trigger)
├── seed.sql                # Optional sample data
└── init_db.py               # Python helper to run the above
```

---

That's the whole application — everything above `React → Flask → PostgreSQL`
(Docker, Compose, Kubernetes, EKS, GitOps, CI/CD, monitoring) is intentionally
left for you to build next.
