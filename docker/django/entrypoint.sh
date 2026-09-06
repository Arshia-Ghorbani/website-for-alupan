#!/bin/bash
# Runs before every container command: block until Postgres and Redis answer.
set -o errexit
set -o pipefail
set -o nounset

python << 'PYCODE'
import os
import sys
import time
from urllib.parse import urlparse

import psycopg

url = urlparse(os.environ["DATABASE_URL"])
deadline = time.time() + 60

while True:
    try:
        psycopg.connect(
            dbname=url.path.lstrip("/"),
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port or 5432,
            connect_timeout=3,
        ).close()
        break
    except psycopg.OperationalError as exc:
        if time.time() > deadline:
            sys.stderr.write(f"PostgreSQL unreachable after 60s: {exc}\n")
            sys.exit(1)
        sys.stderr.write("Waiting for PostgreSQL...\n")
        time.sleep(2)

sys.stderr.write("PostgreSQL is up.\n")
PYCODE

exec "$@"
