FROM node:20-bookworm-slim AS frontend

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY --from=frontend /app/backend/static_src ./backend/static_src

WORKDIR /app/backend

RUN python manage.py collectstatic --noinput

CMD python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT}
