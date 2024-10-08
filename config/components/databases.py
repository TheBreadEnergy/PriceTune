from config.config import settings

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.DB_NAME,
        "USER": settings.DB_USER,
        "PASSWORD": settings.DB_PASSWORD,
        "HOST": settings.DB_HOST,
        "PORT": settings.DB_PORT,
    },
}
