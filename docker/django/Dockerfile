# syntax=docker/dockerfile:1.7
###############################################################################
# Stage 1 — builder: compile wheels with the toolchain, then throw it away.
###############################################################################
ARG PYTHON_VERSION=3.12-slim-bookworm

FROM python:${PYTHON_VERSION} AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Build-only dependencies: gcc for argon2/psycopg C extensions, libpq for pg.
RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /wheels
COPY requirements/ /requirements/

# BUILD_ENV=development|production selects the requirements file.
ARG BUILD_ENV=production
RUN pip wheel --wheel-dir /wheels -r /requirements/${BUILD_ENV}.txt


###############################################################################
# Stage 2 — runtime: slim image, no compilers, non-root user.
###############################################################################
FROM python:${PYTHON_VERSION} AS runtime

ARG BUILD_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_ENV=${BUILD_ENV}

# Runtime-only libraries.  gettext is required by makemessages/compilemessages
# for the fa/en translation catalogues.
RUN apt-get update && apt-get install --no-install-recommends -y \
        libpq5 \
        gettext \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install the pre-built wheels — no network, no compiler in the final image.
COPY --from=builder /wheels /wheels
COPY requirements/ /requirements/
RUN pip install --no-index --find-links=/wheels -r /requirements/${BUILD_ENV}.txt \
    && rm -rf /wheels /requirements

# Unprivileged user: a container escape should not land on root.
RUN groupadd --gid 1000 django \
    && useradd --uid 1000 --gid django --shell /bin/bash --create-home django

WORKDIR /app

COPY --chown=django:django docker/django/entrypoint.sh   /entrypoint.sh
COPY --chown=django:django docker/django/start-web.sh    /start-web.sh
COPY --chown=django:django docker/django/start-worker.sh /start-worker.sh
COPY --chown=django:django docker/django/start-beat.sh   /start-beat.sh
RUN sed -i 's/\r$//g' /entrypoint.sh /start-*.sh && chmod +x /entrypoint.sh /start-*.sh

COPY --chown=django:django . /app

# Static and media are bind-mounted volumes in compose; create them owned by django.
RUN mkdir -p /app/staticfiles /app/media && chown -R django:django /app

USER django

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD curl -fsS http://localhost:8000/health/live/ || exit 1

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start-web.sh"]
