"""Production settings.  Assumes TLS is terminated by Nginx in front of Gunicorn."""

from .base import *  # noqa: F403
from .base import env  # noqa: F401

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY")                 # must be set — fails loudly
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")      # must be set — fails loudly

# --- HTTPS ----------------------------------------------------------------
# Nginx sets X-Forwarded-Proto; without this Django cannot tell it is on HTTPS
# and SECURE_SSL_REDIRECT would loop forever.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)

SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=60 * 60 * 24 * 365)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 60 * 60 * 8
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# --- Static files ---------------------------------------------------------
# Hashed filenames + pre-compressed variants, so Nginx can serve them with a
# one-year immutable cache header.
STORAGES["staticfiles"] = {  # noqa: F405
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
}

# --- Error reporting ------------------------------------------------------
LOGGING["handlers"]["mail_admins"] = {  # noqa: F405
    "level": "ERROR",
    "class": "django.utils.log.AdminEmailHandler",
}
LOGGING["loggers"]["django.request"] = {  # noqa: F405
    "level": "ERROR",
    "handlers": ["console", "mail_admins"],
    "propagate": False,
}

# Plug Sentry in here when you are ready:
# import sentry_sdk
# sentry_sdk.init(dsn=env("SENTRY_DSN"), traces_sample_rate=0.1, send_default_pii=False)
