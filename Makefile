# Thin wrappers so nobody has to remember the compose incantations.
COMPOSE      := docker compose
COMPOSE_PROD := docker compose -f docker-compose.prod.yml
RUN          := $(COMPOSE) run --rm web

.PHONY: help build up down logs shell dbshell migrate migrations superuser \
        static test lint format messages compile-messages backup prod-up prod-down

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS=":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

build:            ## Build all images
	$(COMPOSE) build

up:               ## Start the dev stack (foreground)
	$(COMPOSE) up

down:             ## Stop the stack (keeps volumes)
	$(COMPOSE) down

reset:            ## Stop the stack and DESTROY the database volume
	$(COMPOSE) down -v

logs:             ## Tail logs
	$(COMPOSE) logs -f --tail=100

shell:            ## Django shell
	$(RUN) python manage.py shell

bash:             ## Bash inside the web container
	$(COMPOSE) exec web bash

dbshell:          ## psql prompt
	$(COMPOSE) exec db psql -U $${POSTGRES_USER:-alupan} -d $${POSTGRES_DB:-alupan}

migrations:       ## Generate migrations
	$(RUN) python manage.py makemigrations

migrate:          ## Apply migrations
	$(RUN) python manage.py migrate

superuser:        ## Create an admin account
	$(RUN) python manage.py createsuperuser

static:           ## Collect static files
	$(RUN) python manage.py collectstatic --noinput

check:            ## Django system checks, production profile
	$(RUN) python manage.py check --deploy --settings=config.settings.production

test:             ## Run the test suite
	$(RUN) pytest

lint:             ## Ruff + mypy
	$(RUN) ruff check .
	$(RUN) mypy .

format:           ## Auto-format
	$(RUN) ruff check --fix .
	$(RUN) black .

messages:         ## Extract translatable strings (fa/en)
	$(RUN) python manage.py makemessages -l fa -l en --ignore=.venv

compile-messages: ## Compile .po -> .mo
	$(RUN) python manage.py compilemessages

backup:           ## Dump the database to ./backups
	$(COMPOSE) exec db pg_dump -U $${POSTGRES_USER:-alupan} $${POSTGRES_DB:-alupan} \
		| gzip > backups/alupan_$$(date +%Y%m%d_%H%M%S).sql.gz

prod-up:          ## Start the production stack
	$(COMPOSE_PROD) up -d --build

prod-down:        ## Stop the production stack
	$(COMPOSE_PROD) down
