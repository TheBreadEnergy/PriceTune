from pathlib import Path

from split_settings.tools import include

from .config import settings

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = settings.SECRET_KEY

DEBUG = settings.DEBUG

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

CSRF_TRUSTED_ORIGINS = settings.CSRF_TRUSTED_ORIGINS

include(
    "components/*.py",
)

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
