import os
import sys
import time

from django.core.management import call_command


def run_migrations():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    last_error = None
    for attempt in range(1, 11):
        try:
            print(f"Running database migrations, attempt {attempt}/10...", flush=True)
            call_command("migrate", interactive=False, verbosity=1)
            print("Database migrations finished.", flush=True)
            return
        except Exception as exc:
            last_error = exc
            print(f"Migration attempt {attempt}/10 failed: {exc}", flush=True)
            time.sleep(3)
    raise last_error


def main():
    run_migrations()
    port = os.getenv("PORT", "8000")
    print(f"Starting gunicorn on 0.0.0.0:{port}...", flush=True)
    os.execvp(
        "gunicorn",
        [
            "gunicorn",
            "config.wsgi:application",
            "--bind",
            f"0.0.0.0:{port}",
        ],
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Startup failed: {exc}", file=sys.stderr, flush=True)
        raise
