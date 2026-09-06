#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

exec celery -A config.celery:app worker \
    --loglevel="${CELERY_LOG_LEVEL:-INFO}" \
    --concurrency="${CELERY_CONCURRENCY:-2}"
