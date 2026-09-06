# Alupan — Corporate Platform

Django 5.2 / PostgreSQL 16 / Redis 7 / Celery 5 / Docker, bilingual (فارسی + English).
This repository is the **backend foundation**: infrastructure, settings, data model and
admin. The public-facing templates, CSS and GSAP layer are built on top of it.

---

## 1. Quick start (Docker — the only supported way to run this)

```bash
git clone <your-remote> alupan && cd alupan

cp .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(64))"   # paste into DJANGO_SECRET_KEY
# also set POSTGRES_PASSWORD and mirror it inside DATABASE_URL

docker compose build
docker compose up -d

docker compose run --rm web python manage.py makemigrations
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser
```

Site: <http://localhost:8000/fa/> · Admin: <http://localhost:8000/fa/admin/>
Health: `/health/live/` (liveness) and `/health/ready/` (DB reachable).

`make help` lists every shortcut.

---

## 2. Bootstrap commands (how this tree was generated)

Run these only if you are recreating the skeleton from an empty directory.

```bash
mkdir alupan && cd alupan
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install "Django==5.2.6" django-environ "psycopg[binary]" Pillow django-modeltranslation

# 'config' as the settings package — never name it after the company, so the
# project can be renamed without touching a single import.
django-admin startproject config .

mkdir apps && touch apps/__init__.py

for app in core systems projects news contact; do
    mkdir -p "apps/$app"
    python manage.py startapp "$app" "apps/$app"
done
```

`startapp` writes `name = "core"` into each `apps.py`; it must become the dotted
path, which is why every config in this repo reads:

```python
name = "apps.core"
label = "core"
```

Then split the settings module:

```bash
mkdir config/settings
touch config/settings/__init__.py
git mv config/settings.py config/settings/base.py     # or plain mv
# create development.py / production.py / test.py importing from base
```

Freeze it:

```bash
mkdir requirements && pip freeze > requirements/base.txt   # then curate by hand
```

---

## 3. Directory layout

```
alupan/
├── config/                     # project package — settings, urls, wsgi/asgi, celery
│   ├── settings/
│   │   ├── base.py             # everything shared
│   │   ├── development.py      # DEBUG, console email, locmem cache
│   │   ├── production.py       # HSTS, SSL redirect, manifest static storage
│   │   └── test.py             # eager Celery, locmem email
│   ├── celery.py               # Celery app, autodiscovers apps/*/tasks.py
│   ├── urls.py                 # i18n_patterns + sitemap + health + error handlers
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                       # every business app lives under one namespace
│   ├── core/                   # User, SiteSettings, abstract bases, sitemaps, errors
│   ├── systems/                # aluminium system catalogue (the product spine)
│   ├── projects/               # built references / portfolio
│   ├── news/                   # articles & announcements
│   └── contact/                # RFQ + enquiry capture (Celery-backed email)
│
├── docker/
│   ├── django/                 # Dockerfile, entrypoint, start-web/worker/beat
│   ├── nginx/                  # nginx.conf, alupan.conf, proxy_params, certs/
│   └── postgres/init/          # pg_trgm / unaccent extensions, run once
│
├── requirements/               # base.txt · development.txt · production.txt
├── templates/                  # base.html, partials, per-app dirs, errors, emails
├── static/                     # source CSS/JS/GSAP bundles (hand-written)
├── staticfiles/                # collectstatic output — volume, git-ignored
├── media/                      # editor uploads — volume, git-ignored
├── locale/                     # fa/ and en/ .po catalogues
├── backups/                    # pg_dump target
│
├── docker-compose.yml          # dev: web, db, redis, worker, beat
├── docker-compose.prod.yml     # prod: + nginx, gunicorn, limits, no bind-mounts
 -> docker/django/Dockerfile$# -> docker/django/Dockerfile
├── manage.py
├── Makefile
├── pyproject.toml              # ruff, black, mypy, pytest, coverage
└── .env.example
```

### Why `apps/` and `config/`

* One import prefix (`apps.*`) makes it impossible to shadow a third-party package.
* `config` is generic, so renaming the product never touches `DJANGO_SETTINGS_MODULE`.
* Each app owns its `models / views / urls / admin / translation / sitemaps / tasks`,
  so a new section of the site is a new folder, not an edit to a 2000-line module.

---

## 4. Architectural decisions worth knowing

| Decision | Reason |
|---|---|
| Custom `core.User` from day one | Swapping `AUTH_USER_MODEL` after the first migration is a multi-day data migration. Now it is free. |
| Abstract `TimeStampedModel` / `PublishableModel` / `SEOModel` / `OrderedModel` | Draft→publish workflow, meta tags and manual ordering are defined once and inherited by every content model. |
| `django-modeltranslation` | Adds `name_fa` / `name_en` columns instead of a parallel translation table — no join, no N+1, and the admin renders tabbed language fields. |
| `i18n_patterns(prefix_default_language=True)` | Both `/fa/` and `/en/` are explicit URLs; nothing lives at an ambiguous root, which keeps `hreflang` and the sitemap honest. |
| `ATOMIC_REQUESTS = True` | A failed request leaves no half-written rows. |
| Celery for outbound mail | The RFQ form returns instantly even when the SMTP relay is slow or down; failures retry three times. |
| Multi-stage Dockerfile, non-root user | Compilers stay in the builder stage; the runtime image is small and the process cannot write to system paths. |
| WhiteNoise *and* Nginx | Nginx serves `/static/` in production; WhiteNoise means the dev image behaves identically and a bare `gunicorn` still works. |
| `pg_trgm` + `unaccent` preinstalled | Site search over Persian and English content can use trigram matching without a later migration. |

---

## 5. Everyday commands

```bash
make up                 # start the stack
make logs               # follow logs
make migrations         # makemigrations
make migrate
make superuser
make messages           # extract fa/en strings
make compile-messages
make test               # pytest
make lint               # ruff + mypy
make check              # manage.py check --deploy against production settings
make backup             # gzip pg_dump into ./backups
```

---

---

## 7. Frontend layer (homepage)

| File | Role |
|---|---|
| `templates/base.html` | `<html dir>` / `lang` from Django's i18n, font preload, GSAP tags |
| `templates/core/home.html` | the homepage — hero, tech scrollytelling, project, parts grid, CTA |
| `templates/partials/_header.html` `_footer.html` `_icon-sprite.html` | chrome + inline SVG sprite |
| `static/css/main.css` | the whole design system, written with CSS **logical properties** |
| `static/js/main.js` | GSAP + ScrollTrigger motion layer |
| `apps/core/views.py` | `HomeView` context (placeholder copy — see the banner in that file) |

**Palette.** `#FFFFFF` is the page. `#0047AB` appears only as accent — eyebrows,
buttons, stat figures, icons, the hover inversion, the CTA band. Neutrals are
cool-shifted (`--ink #0A0D12`, `--alu #C9CFD6`) so white beside cobalt reads
architectural rather than warm.

**RTL.** One stylesheet serves both directions: every offset uses
`padding-inline`, `inset-inline-start`, `transform-origin: inline-end` and so
on, so the English build needs no mirrored CSS. `main.js` reads
`document.documentElement.dir` and flips the sign of horizontal motion.

**Motion.**

* *Cinematic hero load* — `.hero__mask` animates `clip-path: inset(100% 0 0 0)`
  → `inset(0)` while `.hero__art` counter-moves from `yPercent: 14, scale: 1.12`.
  Opening the mask upward while the artwork settles downward reads as a camera
  tilt instead of a wipe. `body.is-loading` locks scroll until it finishes.
* *Headline stagger* — `splitWords()` wraps each word in an `overflow: hidden`
  mask, then GSAP lifts them from `yPercent: 115` with a 0.075s stagger. Words
  slide out from behind their own baseline. It refuses to split a heading that
  contains markup, so `<span class="ltr">AluK</span>` is never destroyed.
* *Scrollytelling* — the AluK visual column is `position: sticky`; one
  ScrollTrigger per step swaps the active SVG layer and the 01/03 counter.
* *Parallax* — `[data-parallax]` scrubs `yPercent -12 → 12` against its parent's
  scroll range (Atlas Mall band).
* *Counters* — animate a proxy value, then print Persian digits with the
  U+066C thousands separator (`۱۲۰٬۰۰۰`).

**Hover micro-interactions.** Buttons and part cards share one idea: a cobalt
(or ink) panel `scaleY(0) → scaleY(1)` from `transform-origin: bottom` behind
the content, with the label, icon and index transitioning to white on the same
curve. Nav links and text links draw a rule from the trailing edge inward.

**Degradation.** If the GSAP CDN is blocked — a real risk in Iran — `main.js`
logs once and calls `releasePage()`: every reveal state resolves, the hero mask
opens, scroll unlocks. `prefers-reduced-motion: reduce` takes the same path.
Self-host GSAP next to Vazirmatn if you want to remove the dependency entirely.

**Before launch:** replace the placeholder figures in `apps/core/views.py` and
the Atlas Mall facts in `home.html` with numbers you can evidence, and drop real
photography into `static/images/` (the hero and project blocks already accept it
through the `--facade-image` / `--project-image` custom properties).

## 8. Before the first production deploy

- [ ] `DJANGO_SECRET_KEY` is a fresh 64-char random value, stored in your secret manager
- [ ] `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS` set (keep `localhost` for the healthcheck)
- [ ] `DJANGO_ADMIN_URL` changed from `admin/` to something unguessable
- [ ] `docker compose run --rm web python manage.py check --deploy` is clean
- [ ] TLS certificates mounted at `docker/nginx/certs/{fullchain,privkey}.pem`
- [ ] `make backup` scheduled off-host (cron or the `beat` service)
- [ ] `SENTRY_DSN` set and `sentry_sdk.init(...)` uncommented in `production.py`
