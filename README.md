# Breathe ESG Prototype

Operational ESG ingestion and analyst review prototype for the Breathe ESG tech intern assignment.

The app is organized as a Django REST backend and a React frontend. It ingests three realistic source shapes:

- SAP fuel/procurement flat-file exports
- Utility electricity portal CSV exports
- Corporate travel platform CSV exports

The backend preserves raw uploads, parses source-native rows, normalizes them into a canonical record model, flags suspicious operational data, and exposes review/audit APIs. The frontend gives analysts an upload flow, queue-first dashboard, suspicious review table, and audit visibility.

## Local Setup

Backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

If npm is not available globally on this machine, use the local wrapper:

```powershell
cd C:\Users\Dell\Downloads\Breathe_esg\frontend
..\scripts\npm.ps1 install
..\scripts\npm.ps1 run dev
```

Default production frontend API base URL is same-domain `/api`. For local Vite development, copy `frontend/.env.example` to `frontend/.env` so Vite calls `http://localhost:8000/api`.

## One-Link Deployment

The production Dockerfile builds the React frontend and serves it from Django:

- App UI: `/`
- React routes: `/dashboard`, `/upload`, `/review`, `/audit`
- Backend API: `/api/...`

On Railway, deploy the root project using the included `Dockerfile` and set the Django/Postgres environment variables.

## Assignment Docs

- [MODEL.md](MODEL.md)
- [DECISIONS.md](DECISIONS.md)
- [TRADEOFFS.md](TRADEOFFS.md)
- [SOURCES.md](SOURCES.md)
