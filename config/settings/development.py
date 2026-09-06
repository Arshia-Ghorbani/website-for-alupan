"""Local development settings.  Never used on a server."""

from .base import *  # noqa: F403
from .base import BASE_DIR, env  # noqa: F401

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-local-only-do-not-use-in-production-000000000",
)

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "web", ".localhost"]
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# Emails are printed to the console instead of being sent.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Passwords hash instantly so tests and fixtures stay fast.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# No cache surprises while developing.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# Uncomment once django-debug-toolbar is added to requirements/development.txt:
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
