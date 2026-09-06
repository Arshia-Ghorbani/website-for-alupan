#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

# Stale schedule file from a crashed container would block startup.
rm -f './celerybeat.pid'

exec celery -A config.celery:app beat \
    --loglevel="${CELERY_LOG_LEVEL:-INFO}"
