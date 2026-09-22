# Cloud Computing HW1 API

FastAPI backend starter for the responsive personal introduction project.

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs> to view the interactive API documentation.

## Endpoints

- `GET /` — basic server message
- `GET /health` — service health check
- `GET /docs` — Swagger UI

## Render

Create a Render Web Service connected to this repository with:

- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

The app entry point is `app.main:app`.
