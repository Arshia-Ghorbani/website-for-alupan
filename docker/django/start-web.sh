#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate --noinput

if [ "${DJANGO_ENV:-production}" = "development" ]; then
    exec python manage.py runserver 0.0.0.0:8000
else
    python manage.py collectstatic --noinput
    python manage.py compilemessages --ignore=.venv || true
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers "${GUNICORN_WORKERS:-3}" \
        --threads "${GUNICORN_THREADS:-2}" \
        --worker-class gthread \
        --timeout 60 \
        --graceful-timeout 30 \
        --max-requests 1000 \
        --max-requests-jitter 100 \
        --access-logfile - \
        --error-logfile - \
        --log-level info
fi
