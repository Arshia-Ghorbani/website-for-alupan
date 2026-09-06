"""
Base settings shared by every environment.

Environment-specific modules (development.py / production.py) import from here
and override only what differs.  Nothing secret is ever hard-coded: every value
that changes between machines comes from the environment via django-environ.
"""

from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# config/settings/base.py  ->  config/settings  ->  config  ->  <project root>
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "apps"

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
env = environ.Env()

# Inside Docker the variables are injected by compose; locally we read .env.
if env.bool("DJANGO_READ_DOT_ENV_FILE", default=True):
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        env.read_env(str(env_file))

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
DJANGO_APPS = [
    # modeltranslation MUST be listed before django.contrib.admin so that it can
    # patch the admin classes that render translated fields.
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    # Required because FORM_RENDERER is set to TemplatesSetting.
    "django.forms",
]

THIRD_PARTY_APPS: list[str] = [
    # e.g. "django_celery_beat", "storages", "axes"
]

LOCAL_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.systems.apps.SystemsConfig",
    "apps.projects.apps.ProjectsConfig",
    "apps.news.apps.NewsConfig",
    "apps.contact.apps.ContactConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise serves hashed static files directly from Gunicorn.  Nginx still
    # fronts /static/ in production; WhiteNoise is the safety net and makes the
    # dev image behave like production.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # LocaleMiddleware must sit after Session and before Common.
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
# DATABASE_URL = postgres://user:password@host:5432/dbname
DATABASES = {
    "default": {
        **env.db("DATABASE_URL"),
        # Persistent connections: expensive to reopen a PG connection per request.
        "CONN_MAX_AGE": env.int("CONN_MAX_AGE", default=60),
        "CONN_HEALTH_CHECKS": True,
        # Every request runs inside a transaction; a 500 rolls the whole thing back.
        "ATOMIC_REQUESTS": True,
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Cache (Redis)
# ---------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://redis:6379/1"),
        "KEY_PREFIX": "alupan",
    }
}

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
# Swapping the user model AFTER the first migration is painful, so we do it now
# even though the corporate site only needs staff accounts today.
AUTH_USER_MODEL = "core.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 10},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

LOGIN_URL = "admin:login"
LOGIN_REDIRECT_URL = "/"

# ---------------------------------------------------------------------------
# Internationalisation  (Persian primary, English secondary)
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "fa"
LANGUAGES = [
    ("fa", _("Persian")),
    ("en", _("English")),
]
LOCALE_PATHS = [BASE_DIR / "locale"]

TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

# django-modeltranslation: translated model fields are generated per language.
MODELTRANSLATION_DEFAULT_LANGUAGE = "fa"
MODELTRANSLATION_LANGUAGES = ("fa", "en")
MODELTRANSLATION_FALLBACK_LANGUAGES = ("fa", "en")

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_settings",
            ],
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# ---------------------------------------------------------------------------
# Static & media
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"          # collectstatic target (shared volume)
STATICFILES_DIRS = [BASE_DIR / "static"]        # hand-written CSS/JS/GSAP bundles

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"                 # editor uploads (shared volume)

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        # Overridden to the hashed/compressed backend in production.py
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}

FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024    # 5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# ---------------------------------------------------------------------------
# Security baseline (hardened further in production.py)
# ---------------------------------------------------------------------------
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = False        # templates read the token via JS on AJAX forms
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_TIMEOUT = 10
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="Alupan <noreply@alupan.com>")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = "[Alupan] "

# Where contact / RFQ notifications are delivered.
SALES_NOTIFICATION_EMAILS = env.list("SALES_NOTIFICATION_EMAILS", default=[])
ADMINS = [("Alupan Web", env("ADMIN_EMAIL", default="webmaster@alupan.com"))]
MANAGERS = ADMINS

# ---------------------------------------------------------------------------
# Celery
# ---------------------------------------------------------------------------
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://redis:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# ---------------------------------------------------------------------------
# Logging — structured to stdout so Docker/observability tooling collects it
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(name)s %(process)d "
            "%(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": env("DJANGO_LOG_LEVEL", default="INFO"), "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "apps": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
    },
}

# ---------------------------------------------------------------------------
# Project-specific
# ---------------------------------------------------------------------------
# Obscuring the admin path removes 99% of automated login noise.
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")

SITE_NAME = "Alupan"
SITE_DOMAIN = env("SITE_DOMAIN", default="alupan.com")
